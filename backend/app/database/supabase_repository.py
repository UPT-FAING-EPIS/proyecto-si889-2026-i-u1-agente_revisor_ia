import re
from collections import Counter
from collections.abc import Sequence
import logging

from supabase import Client, create_client

from app.core.config import get_settings


LOGGER = logging.getLogger(__name__)
TOKEN_PATTERN = re.compile(r"[\w\-]+", re.UNICODE)


class SupabaseRepositoryError(Exception):
    """Error de operaciones en Supabase."""


class SupabaseRepository:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client: Client | None = None
        self._storage_bucket_ready = False

    def _get_client(self) -> Client:
        if self._client:
            return self._client

        if not self.settings.supabase_url:
            raise SupabaseRepositoryError(
                "Debes configurar SUPABASE_URL en las variables de entorno del backend."
            )

        if not self.settings.supabase_service_role_key:
            raise SupabaseRepositoryError(
                "Debes configurar SUPABASE_SERVICE_ROLE_KEY para operaciones backend con RLS."
            )

        self._client = create_client(
            self.settings.supabase_url,
            self.settings.supabase_service_role_key,
        )
        return self._client

    @staticmethod
    def _to_pgvector(embedding: Sequence[float]) -> str:
        return "[" + ",".join(f"{value:.8f}" for value in embedding) + "]"

    @staticmethod
    def _tokenize_for_search(text: str) -> list[str]:
        return [
            token
            for token in TOKEN_PATTERN.findall((text or "").lower())
            if len(token) >= 3
        ]

    @staticmethod
    def _is_vector_dimension_mismatch(error: Exception) -> bool:
        message = str(error).lower()
        return (
            "different vector dimensions" in message
            or ("vector" in message and "dimension" in message)
        )

    def _fallback_match_document_chunks_text(
        self,
        document_id: str,
        query_text: str | None,
        match_count: int,
    ) -> list[dict]:
        client = self._get_client()

        response = (
            client.table("document_chunks")
            .select("id, document_id, content")
            .eq("document_id", document_id)
            .order("id")
            .limit(1000)
            .execute()
        )

        chunks = response.data or []
        if not chunks:
            return []

        query_tokens = self._tokenize_for_search(query_text or "")
        if not query_tokens:
            return [
                {
                    "id": chunk.get("id"),
                    "document_id": chunk.get("document_id"),
                    "content": chunk.get("content"),
                    "similarity": 0.0,
                }
                for chunk in chunks[:match_count]
            ]

        scored_chunks: list[tuple[float, dict]] = []
        for chunk in chunks:
            content = chunk.get("content") or ""
            content_tokens = self._tokenize_for_search(content)
            if not content_tokens:
                scored_chunks.append((0.0, chunk))
                continue

            frequency = Counter(content_tokens)
            score = 0.0
            for token in query_tokens:
                hits = frequency.get(token, 0)
                if hits:
                    score += 1.0 + min(hits, 4) * 0.25

            scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda item: item[0], reverse=True)
        top_chunks = scored_chunks[:match_count]

        if top_chunks and top_chunks[0][0] == 0.0:
            top_chunks = [(0.0, chunk) for chunk in chunks[:match_count]]

        return [
            {
                "id": chunk.get("id"),
                "document_id": chunk.get("document_id"),
                "content": chunk.get("content"),
                "similarity": score,
            }
            for score, chunk in top_chunks
        ]

    @staticmethod
    def _normalize_filename(filename: str) -> str:
        clean = re.sub(r"[^A-Za-z0-9._-]+", "_", (filename or "").strip())
        if not clean:
            clean = "documento.pdf"
        if not clean.lower().endswith(".pdf"):
            clean = f"{clean}.pdf"
        return clean

    def _build_pdf_storage_path(self, user_id: str, document_id: str, filename: str) -> str:
        normalized_filename = self._normalize_filename(filename)
        return f"{user_id}/{document_id}/{normalized_filename}"

    @staticmethod
    def _extract_signed_url(payload: object) -> str | None:
        if isinstance(payload, dict):
            url = (
                payload.get("signedURL")
                or payload.get("signedUrl")
                or payload.get("signed_url")
            )
            if isinstance(url, str) and url.strip():
                return url

        url_attr = getattr(payload, "signedURL", None) or getattr(payload, "signed_url", None)
        if isinstance(url_attr, str) and url_attr.strip():
            return url_attr

        return None

    def _ensure_storage_bucket(self) -> None:
        if self._storage_bucket_ready:
            return

        client = self._get_client()
        bucket_name = self.settings.supabase_storage_bucket

        bucket_exists = False
        try:
            buckets = client.storage.list_buckets() or []
            for bucket in buckets:
                name = bucket.get("name") if isinstance(bucket, dict) else getattr(bucket, "name", None)
                if name == bucket_name:
                    bucket_exists = True
                    break
        except Exception:
            bucket_exists = False

        if not bucket_exists:
            try:
                client.storage.create_bucket(bucket_name, options={"public": False})
            except TypeError:
                client.storage.create_bucket(bucket_name)
            except Exception as error:
                message = str(error).lower()
                if "exists" not in message and "duplicate" not in message and "already" not in message:
                    raise SupabaseRepositoryError(
                        f"No se pudo crear bucket de storage '{bucket_name}'."
                    ) from error

        self._storage_bucket_ready = True

    def upload_document_pdf(
        self,
        user_id: str,
        document_id: str,
        filename: str,
        file_bytes: bytes,
    ) -> str:
        if not file_bytes:
            raise SupabaseRepositoryError("No se puede subir un PDF vacio.")

        client = self._get_client()
        self._ensure_storage_bucket()

        bucket_name = self.settings.supabase_storage_bucket
        storage_path = self._build_pdf_storage_path(user_id, document_id, filename)
        bucket = client.storage.from_(bucket_name)

        try:
            bucket.upload(
                path=storage_path,
                file=file_bytes,
                file_options={
                    "content-type": "application/pdf",
                    "upsert": "true",
                },
            )
        except TypeError:
            bucket.upload(
                storage_path,
                file_bytes,
                {"content-type": "application/pdf", "upsert": "true"},
            )
        except Exception as error:
            raise SupabaseRepositoryError("No se pudo almacenar el PDF en Supabase Storage.") from error

        return storage_path

    def get_document_pdf_url(self, user_id: str, document_id: str, filename: str) -> str | None:
        client = self._get_client()
        self._ensure_storage_bucket()

        bucket_name = self.settings.supabase_storage_bucket
        storage_path = self._build_pdf_storage_path(user_id, document_id, filename)
        bucket = client.storage.from_(bucket_name)

        try:
            result = bucket.create_signed_url(
                storage_path,
                self.settings.supabase_storage_signed_url_expires_seconds,
            )
        except TypeError:
            result = bucket.create_signed_url(
                path=storage_path,
                expires_in=self.settings.supabase_storage_signed_url_expires_seconds,
            )
        except Exception:
            return None

        signed_url = self._extract_signed_url(result)
        if not signed_url:
            return None

        if signed_url.startswith("http"):
            return signed_url

        base_url = self.settings.supabase_url.rstrip("/")
        if signed_url.startswith("/"):
            return f"{base_url}{signed_url}"

        return f"{base_url}/{signed_url}"

    def create_document(self, user_id: str, filename: str) -> dict:
        client = self._get_client()
        response = (
            client.table("documents")
            .insert(
                {
                    "user_id": user_id,
                    "filename": filename,
                }
            )
            .execute()
        )

        if not response.data:
            raise SupabaseRepositoryError("No se pudo registrar el documento en Supabase.")

        return response.data[0]

    def delete_document(self, document_id: str) -> None:
        client = self._get_client()
        client.table("documents").delete().eq("id", document_id).execute()

    def list_documents(self, user_id: str) -> list[dict]:
        client = self._get_client()
        response = (
            client.table("documents")
            .select("id, filename, created_at")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        items = response.data or []
        for item in items:
            try:
                item["pdf_url"] = self.get_document_pdf_url(
                    user_id=user_id,
                    document_id=item["id"],
                    filename=item["filename"],
                )
            except SupabaseRepositoryError:
                item["pdf_url"] = None

        return items

    def get_document_by_id(self, document_id: str) -> dict | None:
        client = self._get_client()
        response = (
            client.table("documents")
            .select("id, user_id, filename, created_at")
            .eq("id", document_id)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        item = response.data[0]
        try:
            item["pdf_url"] = self.get_document_pdf_url(
                user_id=item["user_id"],
                document_id=item["id"],
                filename=item["filename"],
            )
        except SupabaseRepositoryError:
            item["pdf_url"] = None
        return item

    def insert_document_chunks(
        self,
        document_id: str,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> int:
        if len(chunks) != len(embeddings):
            raise SupabaseRepositoryError(
                "La cantidad de chunks no coincide con la cantidad de embeddings."
            )

        client = self._get_client()

        rows = [
            {
                "document_id": document_id,
                "content": chunk,
                "embedding": self._to_pgvector(embedding),
            }
            for chunk, embedding in zip(chunks, embeddings, strict=True)
        ]

        batch_size = 100
        for index in range(0, len(rows), batch_size):
            batch = rows[index : index + batch_size]
            client.table("document_chunks").insert(batch).execute()

        return len(rows)

    def match_document_chunks(
        self,
        document_id: str,
        query_embedding: list[float],
        match_count: int = 5,
        query_text: str | None = None,
    ) -> list[dict]:
        client = self._get_client()
        try:
            response = client.rpc(
                "match_document_chunks",
                {
                    "match_document_id": document_id,
                    "query_embedding": self._to_pgvector(query_embedding),
                    "match_count": match_count,
                },
            ).execute()
            return response.data or []
        except Exception as error:
            if self._is_vector_dimension_mismatch(error):
                LOGGER.warning(
                    "Fallo match vectorial por dimensiones incompatibles. "
                    "Activando fallback por texto para document_id=%s",
                    document_id,
                )
                return self._fallback_match_document_chunks_text(
                    document_id=document_id,
                    query_text=query_text,
                    match_count=match_count,
                )

            raise SupabaseRepositoryError(
                "No se pudo recuperar contexto del documento desde Supabase."
            ) from error


supabase_repository = SupabaseRepository()
