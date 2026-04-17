import hashlib
import logging
import math
import re
from collections.abc import Generator

from google import genai
from google.genai import types

from app.core.config import get_settings


SYSTEM_PROMPT = """
Eres un asesor de tesis estricto pero util.
Reglas:
1) Responde en espanol claro y profesional.
2) Basa tu respuesta en los fragmentos de tesis proporcionados.
3) Si no hay suficiente evidencia, dilo explicitamente.
4) Da recomendaciones accionables para mejorar redaccion, metodo y rigor academico.
5) Evita inventar datos.
""".strip()

THESIS_REVIEW_SYSTEM_PROMPT = """
Eres un evaluador academico de tesis universitarias.
Reglas:
1) Responde en espanol formal, claro y accionable.
2) Evalua estructura, problema, objetivos, metodologia, resultados, conclusiones y redaccion.
3) Indica claramente fortalezas y debilidades con ejemplos concretos.
4) Prioriza recomendaciones realistas y ordenadas por impacto.
5) No inventes informacion que no aparezca en el documento.
""".strip()

DEFAULT_EMBEDDING_DIM = 3072
DEFAULT_EMBEDDING_MODEL_FALLBACKS = (
    "text-embedding-004",
    "models/text-embedding-004",
    "gemini-embedding-001",
    "models/gemini-embedding-001",
    "models/embedding-001",
    "embedding-001",
)
DEFAULT_CHAT_MODEL_FALLBACKS = (
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
)
TOKEN_PATTERN = re.compile(r"[\w\-]+", re.UNICODE)
LOGGER = logging.getLogger(__name__)


class GeminiServiceError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class GeminiService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client: genai.Client | None = None
        self._discovered_generation_models: list[str] | None = None
        self._discovered_embedding_models: list[str] | None = None

    @staticmethod
    def _extract_embedding(payload: object) -> list[float] | None:
        if isinstance(payload, dict):
            embeddings = payload.get("embeddings")
            if isinstance(embeddings, list) and embeddings:
                first_embedding = embeddings[0]
                if isinstance(first_embedding, dict):
                    values = first_embedding.get("values")
                    if isinstance(values, list):
                        return [float(value) for value in values]
                values_attr = getattr(first_embedding, "values", None)
                if isinstance(values_attr, list):
                    return [float(value) for value in values_attr]

            embedding = payload.get("embedding")
            if isinstance(embedding, list):
                return [float(value) for value in embedding]
            if isinstance(embedding, dict):
                values = embedding.get("values")
                if isinstance(values, list):
                    return [float(value) for value in values]

        embedding_attr = getattr(payload, "embedding", None)
        if isinstance(embedding_attr, list):
            return [float(value) for value in embedding_attr]

        values_attr = getattr(embedding_attr, "values", None)
        if isinstance(values_attr, list):
            return [float(value) for value in values_attr]

        embeddings_attr = getattr(payload, "embeddings", None)
        if isinstance(embeddings_attr, list) and embeddings_attr:
            first_embedding = embeddings_attr[0]
            values_attr = getattr(first_embedding, "values", None)
            if isinstance(values_attr, list):
                return [float(value) for value in values_attr]

        return None

    @staticmethod
    def _model_aliases(model_name: str) -> list[str]:
        clean_name = (model_name or "").strip()
        if not clean_name:
            return []

        aliases = [clean_name]
        if clean_name.startswith("models/"):
            aliases.append(clean_name[len("models/") :])
        else:
            aliases.append(f"models/{clean_name}")

        seen: set[str] = set()
        ordered: list[str] = []
        for alias in aliases:
            if alias not in seen:
                seen.add(alias)
                ordered.append(alias)
        return ordered

    @staticmethod
    def _dedupe_models(models: list[str]) -> list[str]:
        seen: set[str] = set()
        ordered: list[str] = []
        for model_name in models:
            for alias in GeminiService._model_aliases(model_name):
                if alias not in seen:
                    seen.add(alias)
                    ordered.append(alias)
        return ordered

    def _discover_models_for_method(self, method: str) -> list[str]:
        client = self._get_client()

        try:
            discovered = list(client.models.list())
        except Exception as error:  # pragma: no cover - llamada externa
            LOGGER.warning("No se pudieron listar modelos de Gemini: %s", error)
            return []

        model_names: list[str] = []
        for model in discovered:
            methods = getattr(model, "supported_generation_methods", None) or []
            if method in methods:
                name = getattr(model, "name", "")
                if name:
                    model_names.append(name)

        return self._dedupe_models(model_names)

    def _candidate_embedding_models(self) -> list[str]:
        candidates: list[str] = []
        configured = (self.settings.gemini_embedding_model or "").strip()
        if configured:
            candidates.extend(self._model_aliases(configured))

        for fallback_model in DEFAULT_EMBEDDING_MODEL_FALLBACKS:
            candidates.extend(self._model_aliases(fallback_model))

        if self._discovered_embedding_models is None:
            self._discovered_embedding_models = self._discover_models_for_method(
                "embedContent"
            )

        candidates.extend(self._discovered_embedding_models)

        return self._dedupe_models(candidates)

    def _candidate_chat_models(self) -> list[str]:
        candidates: list[str] = []
        configured = (self.settings.gemini_chat_model or "").strip()
        if configured:
            candidates.extend(self._model_aliases(configured))

        for fallback_model in DEFAULT_CHAT_MODEL_FALLBACKS:
            candidates.extend(self._model_aliases(fallback_model))

        if self._discovered_generation_models is None:
            self._discovered_generation_models = self._discover_models_for_method(
                "generateContent"
            )

        candidates.extend(self._discovered_generation_models)

        return self._dedupe_models(candidates)

    @staticmethod
    def _local_embedding(content: str, dimensions: int = DEFAULT_EMBEDDING_DIM) -> list[float]:
        vector = [0.0] * dimensions
        tokens = TOKEN_PATTERN.findall(content.lower())

        if not tokens:
            tokens = [content.lower().strip() or "vacio"]

        for token in tokens:
            digest = hashlib.blake2b(token.encode("utf-8"), digest_size=16).digest()
            index = int.from_bytes(digest[:4], "big") % dimensions
            sign = 1.0 if (digest[4] % 2 == 0) else -1.0
            weight = 1.0 + (digest[5] / 255.0) * 0.2
            vector[index] += sign * weight

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            vector[0] = 1.0
            return vector

        return [value / norm for value in vector]

    def _coerce_embedding_dimension(self, embedding: list[float]) -> list[float]:
        target_dimension = self.settings.gemini_embedding_output_dimensionality
        if target_dimension <= 0:
            target_dimension = DEFAULT_EMBEDDING_DIM

        if len(embedding) == target_dimension:
            return embedding

        if len(embedding) > target_dimension:
            return embedding[:target_dimension]

        return embedding + [0.0] * (target_dimension - len(embedding))

    def _get_client(self) -> genai.Client:
        self._ensure_ready()
        if self._client is None:
            raise GeminiServiceError("No se pudo inicializar el cliente de Gemini.")
        return self._client

    def _embed_with_gemini(self, content: str, task_type: str) -> list[float]:
        client = self._get_client()
        errors: list[str] = []

        for model_name in self._candidate_embedding_models():
            try:
                response = client.models.embed_content(
                    model=model_name,
                    contents=content,
                    config=types.EmbedContentConfig(
                        task_type=task_type,
                        output_dimensionality=self.settings.gemini_embedding_output_dimensionality,
                    ),
                )
            except Exception as error:  # pragma: no cover - llamada externa
                errors.append(f"{model_name}: {error}")
                continue

            embedding = self._extract_embedding(response)
            if embedding:
                return embedding

            errors.append(f"{model_name}: embedding vacio")

        errors_preview = "; ".join(errors[:2]) if errors else "sin detalles"
        raise GeminiServiceError(
            "No se pudieron generar embeddings con Gemini. "
            f"Detalles: {errors_preview}"
        )

    def _embed_text_with_fallback(self, content: str, task_type: str) -> list[float]:
        try:
            embedding = self._embed_with_gemini(content=content, task_type=task_type)
        except GeminiServiceError as error:
            LOGGER.warning(
                "Fallo embedding con Gemini, usando fallback local: %s",
                error.message,
            )
            embedding = self._local_embedding(
                content,
                dimensions=self.settings.gemini_embedding_output_dimensionality,
            )

        return self._coerce_embedding_dimension(embedding)

    def _ensure_ready(self) -> None:
        if self._client is not None:
            return

        if not self.settings.gemini_api_key:
            raise GeminiServiceError(
                "GEMINI_API_KEY (o API_GEMINI) no esta configurado en el backend."
            )

        self._client = genai.Client(api_key=self.settings.gemini_api_key)

    def embed_documents(self, chunks: list[str]) -> list[list[float]]:
        return [
            self._embed_text_with_fallback(chunk, task_type="RETRIEVAL_DOCUMENT")
            for chunk in chunks
        ]

    def embed_query(self, question: str) -> list[float]:
        return self._embed_text_with_fallback(
            question,
            task_type="RETRIEVAL_QUERY",
        )

    @staticmethod
    def _format_history(history: list[dict]) -> str:
        if not history:
            return "Sin historial previo."

        lines: list[str] = []
        for message in history[-10:]:
            role = message.get("role", "user")
            content = message.get("content", "")
            if not content:
                continue
            lines.append(f"{role.upper()}: {content}")

        return "\n".join(lines) if lines else "Sin historial previo."

    @staticmethod
    def _format_context(context_chunks: list[dict]) -> str:
        if not context_chunks:
            return "No se recuperaron fragmentos relevantes del documento."

        lines: list[str] = []
        for index, chunk in enumerate(context_chunks, start=1):
            content = (chunk.get("content") or "").strip()
            if not content:
                continue
            lines.append(f"[Fragmento {index}] {content}")

        return "\n\n".join(lines) if lines else "No se recuperaron fragmentos relevantes."

    def _build_prompt(
        self,
        question: str,
        context_chunks: list[dict],
        history: list[dict],
    ) -> str:
        context_block = self._format_context(context_chunks)
        history_block = self._format_history(history)

        return (
            "Contexto recuperado de la tesis:\n"
            f"{context_block}\n\n"
            "Historial de la conversacion:\n"
            f"{history_block}\n\n"
            "Pregunta del estudiante:\n"
            f"{question}\n\n"
            "Responde en formato:\n"
            "- Diagnostico breve\n"
            "- Hallazgos especificos\n"
            "- Recomendaciones accionables"
        )

    @staticmethod
    def _truncate_text(value: str, max_chars: int = 700) -> str:
        text = (value or "").strip()
        if len(text) <= max_chars:
            return text
        return text[: max_chars - 3].rstrip() + "..."

    @staticmethod
    def _extract_text_from_generation_response(response: object) -> str:
        if response is None:
            return ""

        direct_text = getattr(response, "text", None)
        if isinstance(direct_text, str) and direct_text.strip():
            return direct_text.strip()

        if isinstance(response, dict):
            text = response.get("text")
            if isinstance(text, str) and text.strip():
                return text.strip()

        candidates = getattr(response, "candidates", None)
        if candidates is None and isinstance(response, dict):
            candidates = response.get("candidates")

        if not isinstance(candidates, list):
            return ""

        parts_text: list[str] = []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            if isinstance(candidate, dict):
                content = candidate.get("content")

            parts = getattr(content, "parts", None)
            if isinstance(content, dict):
                parts = content.get("parts")

            if not isinstance(parts, list):
                continue

            for part in parts:
                text = getattr(part, "text", None)
                if isinstance(part, dict):
                    text = part.get("text")
                if isinstance(text, str) and text.strip():
                    parts_text.append(text.strip())

        return "\n".join(parts_text)

    @staticmethod
    def _prepare_document_for_review(
        chunks: list[str],
        max_chars: int = 420000,
    ) -> tuple[str, int]:
        formatted_chunks: list[str] = []
        total_chars = 0
        analyzed_chunks = 0

        for index, chunk in enumerate(chunks, start=1):
            content = (chunk or "").strip()
            if not content:
                continue

            block = f"[Fragmento {index}]\n{content}\n\n"
            if total_chars + len(block) > max_chars:
                break

            formatted_chunks.append(block)
            total_chars += len(block)
            analyzed_chunks += 1

        if not formatted_chunks:
            return "", 0

        return "".join(formatted_chunks).strip(), analyzed_chunks

    @staticmethod
    def _build_thesis_review_prompt(
        filename: str,
        total_chunks: int,
        analyzed_chunks: int,
        document_text: str,
    ) -> str:
        return (
            "Analiza integralmente la tesis y entrega retroalimentacion academica.\n"
            f"Archivo: {filename}\n"
            f"Fragmentos cargados para analisis: {analyzed_chunks} de {total_chunks}\n\n"
            "Contenido de la tesis:\n"
            f"{document_text}\n\n"
            "Responde con esta estructura exacta:\n"
            "1) Veredicto general (aprobable/no aprobable y por que)\n"
            "2) Fortalezas principales (3-6 puntos)\n"
            "3) Brechas o debilidades (3-8 puntos)\n"
            "4) Que le falta para mejorar (checklist accionable y priorizada)\n"
            "5) Recomendaciones concretas por capitulo o seccion"
        )

    @staticmethod
    def _build_local_thesis_review(
        thesis_text: str,
        analyzed_chunks: int,
        total_chunks: int,
    ) -> str:
        text = (thesis_text or "").lower()
        word_count = len(TOKEN_PATTERN.findall(text))

        expected_sections = [
            ("resumen", "Resumen"),
            ("introduccion", "Introduccion"),
            ("planteamiento", "Planteamiento del problema"),
            ("objetivos", "Objetivos"),
            ("justificacion", "Justificacion"),
            ("marco", "Marco teorico"),
            ("metodologia", "Metodologia"),
            ("resultados", "Resultados"),
            ("conclusiones", "Conclusiones"),
            ("referencias", "Referencias"),
        ]

        missing_sections = [
            label
            for token, label in expected_sections
            if token not in text
        ]

        strengths: list[str] = []
        if "objetiv" in text:
            strengths.append("Se detecta presencia de objetivos de investigacion.")
        if "metodolog" in text:
            strengths.append("Se identifica una seccion metodologica explicitada.")
        if "conclusion" in text:
            strengths.append("El documento incluye cierre con conclusiones.")
        if word_count >= 5000:
            strengths.append("La extension del contenido sugiere desarrollo suficiente para una tesis.")

        if not strengths:
            strengths.append("Se requiere mayor estructuracion para identificar fortalezas claras.")

        recommendations: list[str] = []
        for section in missing_sections[:5]:
            recommendations.append(f"Agregar o reforzar la seccion de {section}.")

        if word_count < 3500:
            recommendations.append(
                "Incrementar profundidad teorica y metodologica; el contenido parece breve para una tesis completa."
            )

        if not recommendations:
            recommendations.append(
                "Refinar la redaccion academica y sustentar mejor cada afirmacion con evidencia y citas."
            )

        verdict = "Aprobable con observaciones"
        if len(missing_sections) >= 5 or word_count < 2500:
            verdict = "No aprobable en su estado actual"

        missing_block = (
            "\n".join(f"- {section}" for section in missing_sections[:8])
            if missing_sections
            else "- No se detectan vacios estructurales evidentes a nivel de secciones base."
        )
        strengths_block = "\n".join(f"- {item}" for item in strengths)
        recommendations_block = "\n".join(f"- {item}" for item in recommendations)

        return (
            "Veredicto general:\n"
            f"{verdict}.\n\n"
            "Fortalezas principales:\n"
            f"{strengths_block}\n\n"
            "Brechas o debilidades:\n"
            f"{missing_block}\n\n"
            "Que le falta para mejorar:\n"
            f"{recommendations_block}\n\n"
            "Nota tecnica:\n"
            "Esta revision se genero con un analisis local de respaldo porque Gemini no estuvo disponible. "
            f"Fragmentos evaluados: {analyzed_chunks} de {total_chunks}."
        )

    def _build_contextual_fallback_response(
        self,
        question: str,
        context_chunks: list[dict],
    ) -> str:
        if not context_chunks:
            return (
                "No pude usar Gemini en este momento y tampoco se recupero contexto util "
                "de la tesis. Intenta nuevamente en unos minutos."
            )

        snippets: list[str] = []
        for chunk in context_chunks[:3]:
            content = self._truncate_text(chunk.get("content") or "")
            if content:
                snippets.append(f"- {content}")

        snippets_block = "\n".join(snippets) if snippets else "- Sin fragmentos legibles"
        return (
            "Gemini no estuvo disponible en este momento, pero aqui tienes una respuesta "
            "basada en los fragmentos recuperados de tu tesis.\n\n"
            "Diagnostico breve:\n"
            f"La pregunta fue: '{question}'. Con el contexto disponible, estos son los hallazgos mas cercanos.\n\n"
            "Hallazgos especificos (extractivos):\n"
            f"{snippets_block}\n\n"
            "Recomendaciones accionables:\n"
            "1. Vuelve a intentar la consulta para obtener respuesta generativa completa.\n"
            "2. Formula preguntas mas especificas (capitulo, variable, metodo).\n"
            "3. Verifica que tu API key de Gemini tenga cuota y acceso a modelos generativos."
        )

    def review_thesis(self, filename: str, chunks: list[str]) -> tuple[str, int, int]:
        if not chunks:
            raise GeminiServiceError("No hay contenido para evaluar en la tesis.")

        document_text, analyzed_chunks = self._prepare_document_for_review(chunks)
        if not document_text or analyzed_chunks == 0:
            raise GeminiServiceError("No se pudo preparar el texto de la tesis para evaluacion.")

        analyzed_characters = len(document_text)
        prompt = self._build_thesis_review_prompt(
            filename=filename,
            total_chunks=len(chunks),
            analyzed_chunks=analyzed_chunks,
            document_text=document_text,
        )

        try:
            self._ensure_ready()
        except GeminiServiceError as error:
            LOGGER.warning(
                "Gemini no disponible para revision de tesis, usando fallback local: %s",
                error.message,
            )
            fallback = self._build_local_thesis_review(
                thesis_text=document_text,
                analyzed_chunks=analyzed_chunks,
                total_chunks=len(chunks),
            )
            return fallback, analyzed_chunks, analyzed_characters

        client = self._get_client()
        model_errors: list[str] = []

        for model_name in self._candidate_chat_models():
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        max_output_tokens=2200,
                        system_instruction=THESIS_REVIEW_SYSTEM_PROMPT,
                    ),
                )
            except Exception as error:  # pragma: no cover - llamada externa
                model_errors.append(f"{model_name}: {error}")
                continue

            text = self._extract_text_from_generation_response(response)
            if text:
                return text, analyzed_chunks, analyzed_characters

            model_errors.append(f"{model_name}: sin texto util")

        LOGGER.warning(
            "No se pudo generar revision de tesis con Gemini. Fallback local activado. %s",
            "; ".join(model_errors[:3]) if model_errors else "sin detalles",
        )
        fallback = self._build_local_thesis_review(
            thesis_text=document_text,
            analyzed_chunks=analyzed_chunks,
            total_chunks=len(chunks),
        )
        return fallback, analyzed_chunks, analyzed_characters

    def stream_chat_response(
        self,
        question: str,
        context_chunks: list[dict],
        history: list[dict],
    ) -> Generator[str, None, None]:
        try:
            self._ensure_ready()
        except GeminiServiceError as error:
            LOGGER.warning(
                "Gemini no disponible para chat, usando fallback contextual: %s",
                error.message,
            )
            yield self._build_contextual_fallback_response(question, context_chunks)
            return

        prompt = self._build_prompt(
            question=question,
            context_chunks=context_chunks,
            history=history,
        )
        client = self._get_client()

        model_errors: list[str] = []

        for model_name in self._candidate_chat_models():
            try:
                response_stream = client.models.generate_content_stream(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.25,
                        max_output_tokens=1200,
                        system_instruction=SYSTEM_PROMPT,
                    ),
                )
            except Exception as error:  # pragma: no cover - llamada externa
                model_errors.append(f"{model_name}: {error}")
                continue

            yielded_text = False
            try:
                for chunk in response_stream:
                    text = getattr(chunk, "text", "")
                    if text:
                        yielded_text = True
                        yield text
            except Exception as error:  # pragma: no cover - llamada externa
                model_errors.append(f"{model_name}: {error}")
                continue

            if yielded_text:
                return

            model_errors.append(f"{model_name}: sin texto util")

        LOGGER.warning(
            "No se pudo generar respuesta con Gemini. Fallback contextual activado. %s",
            "; ".join(model_errors[:3]) if model_errors else "sin detalles",
        )
        yield self._build_contextual_fallback_response(question, context_chunks)


gemini_service = GeminiService()
