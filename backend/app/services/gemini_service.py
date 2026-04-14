from collections.abc import Generator

import google.generativeai as genai

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


class GeminiServiceError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class GeminiService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._configured = False
        self._chat_model = None

    def _ensure_ready(self) -> None:
        if self._configured:
            return

        if not self.settings.gemini_api_key:
            raise GeminiServiceError(
                "GEMINI_API_KEY (o API_GEMINI) no esta configurado en el backend."
            )

        genai.configure(api_key=self.settings.gemini_api_key)
        self._chat_model = genai.GenerativeModel(
            model_name=self.settings.gemini_chat_model,
            system_instruction=SYSTEM_PROMPT,
            generation_config={
                "temperature": 0.25,
                "max_output_tokens": 1200,
            },
        )
        self._configured = True

    def embed_documents(self, chunks: list[str]) -> list[list[float]]:
        self._ensure_ready()

        embeddings: list[list[float]] = []
        for chunk in chunks:
            try:
                response = genai.embed_content(
                    model=self.settings.gemini_embedding_model,
                    content=chunk,
                    task_type="retrieval_document",
                )
            except Exception as error:  # pragma: no cover - llamada externa
                raise GeminiServiceError(
                    "No se pudieron generar embeddings para el documento."
                ) from error

            embedding = response.get("embedding") if isinstance(response, dict) else None
            if not embedding:
                raise GeminiServiceError("Gemini devolvio un embedding vacio.")

            embeddings.append(embedding)

        return embeddings

    def embed_query(self, question: str) -> list[float]:
        self._ensure_ready()

        try:
            response = genai.embed_content(
                model=self.settings.gemini_embedding_model,
                content=question,
                task_type="retrieval_query",
            )
        except Exception as error:  # pragma: no cover - llamada externa
            raise GeminiServiceError(
                "No se pudo vectorizar la pregunta del estudiante."
            ) from error

        embedding = response.get("embedding") if isinstance(response, dict) else None
        if not embedding:
            raise GeminiServiceError("Gemini devolvio un embedding vacio para la consulta.")

        return embedding

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

    def stream_chat_response(
        self,
        question: str,
        context_chunks: list[dict],
        history: list[dict],
    ) -> Generator[str, None, None]:
        self._ensure_ready()

        prompt = self._build_prompt(
            question=question,
            context_chunks=context_chunks,
            history=history,
        )

        try:
            response_stream = self._chat_model.generate_content(prompt, stream=True)
        except Exception as error:  # pragma: no cover - llamada externa
            raise GeminiServiceError(
                "No se pudo iniciar la respuesta en streaming con Gemini."
            ) from error

        try:
            for chunk in response_stream:
                text = getattr(chunk, "text", "")
                if text:
                    yield text
        except Exception as error:  # pragma: no cover - llamada externa
            raise GeminiServiceError(
                "La respuesta de Gemini se interrumpio durante el streaming."
            ) from error


gemini_service = GeminiService()
