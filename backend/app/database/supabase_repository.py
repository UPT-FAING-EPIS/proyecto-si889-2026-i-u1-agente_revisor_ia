from collections.abc import Sequence

from supabase import Client, create_client

from app.core.config import get_settings


class SupabaseRepositoryError(Exception):
    """Error de operaciones en Supabase."""


class SupabaseRepository:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client: Client | None = None

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
        return response.data or []

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

        return response.data[0]

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
    ) -> list[dict]:
        client = self._get_client()

        response = client.rpc(
            "match_document_chunks",
            {
                "match_document_id": document_id,
                "query_embedding": self._to_pgvector(query_embedding),
                "match_count": match_count,
            },
        ).execute()

        return response.data or []


supabase_repository = SupabaseRepository()
