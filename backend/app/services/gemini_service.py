import hashlib
import logging
import math
import re
import time
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
6) No inicies con saludos, presentaciones personales ni frases de cortesia.
""".strip()

THESIS_REVIEW_SYSTEM_PROMPT = """
Asesor y Revisor de Tesis - FAING

Rol e Identidad:
Eres el "Asesor Virtual FAING", un agente de Inteligencia Artificial especializado en la revision,
correccion y asesoria metodologica de proyectos de investigacion, trabajos de bachiller,
tesis de titulacion y articulos de revision.

Tu marco de referencia estricto y absoluto es el "Manual para el desarrollo de trabajos de
investigacion (2022)" de la Facultad de Ingenieria de la Universidad Privada de Tacna (UPT).

No tienes emociones ni experiencias personales, pero tu tono debe ser empatico, alentador,
profesional y academicamente riguroso.

Tu objetivo no es escribir la tesis por el estudiante, sino guiarlo para que alcance la excelencia
metodologica y formal exigida por la universidad.

Directrices Generales de Interaccion:
1) Metodo Socratico:
- No redactes parrafos completos de la tesis para el estudiante.
- Senala el error.
- Explica por que es incorrecto segun el manual.
- Haz preguntas guia para que el estudiante mejore su propia redaccion.

2) Rigor Formativo:
- Se implacable con el plagio y la falta de coherencia logica.
- Exige siempre citas correctas.

3) Formatos de Graduacion:
- Adapta tu revision dependiendo de si el estudiante esta elaborando un Trabajo de
    Investigacion (Bachiller), un Articulo de Revision (Bachiller), una Tesis formato tradicional
    (Titulo) o una Tesis formato Articulo Cientifico (IMRD).

Reglas de Revision Estructural (Basadas en el Manual FAING):
1. Titulo y Matriz de Consistencia:
- El titulo debe ser informativo, especifico y tener menos de 20 palabras.
- Prohibe el uso de abreviaciones o jergas en el titulo.
- Evalua siempre la Matriz de Consistencia.
- Exige una alineacion perfecta entre el Problema General, el Objetivo General y la Hipotesis General.

2. Planteamiento del Problema:
- Exige que la descripcion del problema vaya de lo general a lo particular, sustentada con citas.
- Verifica que la formulacion termine en preguntas claras (una general y maximo tres especificas)
    que incluyan las variables de estudio.
- Los objetivos deben responder exactamente a las preguntas planteadas y estar redactados con
    verbos en infinitivo (ej. determinar, evaluar, analizar) a nivel de plan.

3. Marco Teorico y Referencias:
- Exige que los antecedentes provengan de revistas cientificas indexadas (articulos cientificos)
    y tengan una antiguedad recomendada de 5 a 10 anos.
- Supervisa estrictamente el uso de las Normas APA (edicion vigente) para todas las citas en
    el texto y la lista de referencias bibliograficas.
- Verifica que la Tesis final o Trabajo de Investigacion tenga un minimo de 25 a 35 referencias
    (o no menos de 30 para formato articulo cientifico).

4. Marco Metodologico:
- Asegurate de que el estudiante defina claramente el Tipo de Estudio (Basico o Aplicado),
    el Nivel de Investigacion (Exploratorio, Descriptivo, Correlacional, Explicativo,
    Predictivo o Aplicativo) y el Diseno (Experimental o No experimental).
- Exige una delimitacion clara de la poblacion y el metodo de calculo de la muestra
    para reducir la variabilidad.
- Evalua si las tecnicas estadisticas propuestas (ej. t de Student, ANOVA,
    pruebas no parametricas, regresion) son las correctas para el tipo de variables
    (cuantitativas/cualitativas) y las hipotesis planteadas.

5. Resultados y Discusiones (Para informes finales):
- Rechaza cualquier resultado que contenga opiniones, juicios de valor o justificaciones.
- Verifica que la informacion de Tablas y Figuras no se repita en el texto.
- Las Tablas deben seguir el formato APA (sin lineas horizontales divisorias internas)
    y las Figuras no deben estar saturadas.
- En la seccion de Discusion, exige que el estudiante contraste sus hallazgos con los
    antecedentes citados en el Marco Teorico y argumente el rechazo o no rechazo de las hipotesis.

6. Conclusiones y Recomendaciones:
- Asegurate de que no se presenten nuevos resultados en las conclusiones.
- Debe haber tantas conclusiones como objetivos formulados.
- Las recomendaciones deben ser factibles y sugerir futuras lineas de investigacion
    derivadas del estudio.

Reglas Operativas de Respuesta:
- Responde siempre en espanol.
- Basa tu evaluacion solo en evidencia disponible en el documento.
- Si falta informacion, declaralo explicitamente y pide evidencia puntual.
- Entrega observaciones concretas por seccion y prioriza mejoras por impacto.
- No inventes citas, datos, autores ni resultados.
- No inicies con saludos, presentaciones ni texto introductorio personal.
- Empieza directamente en la seccion "1) Veredicto general".
""".strip()

DEFAULT_EMBEDDING_DIM = 3072
DEFAULT_EMBEDDING_MODEL_FALLBACKS = (
    "text-embedding-005",
    "models/text-embedding-005",
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
RETRY_IN_SECONDS_PATTERN = re.compile(r"retry\s+in\s+([0-9]+(?:\.[0-9]+)?)s", re.IGNORECASE)
RETRY_DELAY_SECONDS_PATTERN = re.compile(r"retrydelay\s*'?:\s*'([0-9]+)s'", re.IGNORECASE)
MIN_STRUCTURED_REVIEW_CHARS = 900
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
        self._disable_remote_embeddings = False
        self._embedding_fallback_warned = False
        self._disable_remote_generation = False
        self._generation_retry_after_epoch = 0.0
        self._generation_unavailable_reason = ""
        self._generation_fallback_warned = False

    @staticmethod
    def _extract_retry_after_seconds(error_message: str) -> float | None:
        message = (error_message or "").strip()
        if not message:
            return None

        retry_in_match = RETRY_IN_SECONDS_PATTERN.search(message)
        if retry_in_match:
            try:
                return max(float(retry_in_match.group(1)), 0.0)
            except ValueError:
                pass

        retry_delay_match = RETRY_DELAY_SECONDS_PATTERN.search(message)
        if retry_delay_match:
            try:
                return max(float(retry_delay_match.group(1)), 0.0)
            except ValueError:
                pass

        return None

    def _clear_generation_unavailable(self) -> None:
        self._disable_remote_generation = False
        self._generation_retry_after_epoch = 0.0
        self._generation_unavailable_reason = ""
        self._generation_fallback_warned = False

    def _mark_generation_unavailable(
        self,
        reason: str,
        *,
        disable_remote: bool,
        retry_after_seconds: float | None = None,
    ) -> None:
        self._generation_unavailable_reason = (reason or "").strip()
        self._disable_remote_generation = disable_remote

        if retry_after_seconds and retry_after_seconds > 0:
            next_retry_epoch = time.time() + retry_after_seconds
            self._generation_retry_after_epoch = max(
                self._generation_retry_after_epoch,
                next_retry_epoch,
            )

    def _register_generation_failure(self, error_message: str) -> None:
        lower_message = (error_message or "").lower()
        retry_after_seconds = self._extract_retry_after_seconds(error_message)

        if "resource_exhausted" in lower_message or "quota exceeded" in lower_message:
            self._mark_generation_unavailable(
                "Gemini no disponible por cuota agotada (429).",
                disable_remote=True,
                retry_after_seconds=retry_after_seconds,
            )
            return

        if "unavailable" in lower_message and "high demand" in lower_message:
            self._mark_generation_unavailable(
                "Gemini no disponible temporalmente por alta demanda (503).",
                disable_remote=False,
                retry_after_seconds=retry_after_seconds or 60,
            )
            return

        if "not_found" in lower_message or "not found" in lower_message:
            self._mark_generation_unavailable(
                "Modelo Gemini no disponible para la API/configuracion actual.",
                disable_remote=False,
                retry_after_seconds=retry_after_seconds or 300,
            )

    def _should_skip_remote_generation(self) -> bool:
        if self._disable_remote_generation:
            return True

        if self._generation_retry_after_epoch <= 0:
            return False

        if time.time() < self._generation_retry_after_epoch:
            return True

        self._clear_generation_unavailable()
        return False

    def _get_generation_unavailability_reason(self) -> str | None:
        reason = self._generation_unavailable_reason.strip()
        return reason or None

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
        if self._disable_remote_embeddings:
            embedding = self._local_embedding(
                content,
                dimensions=self.settings.gemini_embedding_output_dimensionality,
            )
            return self._coerce_embedding_dimension(embedding)

        try:
            embedding = self._embed_with_gemini(content=content, task_type=task_type)
        except GeminiServiceError as error:
            error_message = (error.message or "").lower()
            is_unavailable_model = (
                "not found" in error_message
                or "not supported for embedcontent" in error_message
                or "unsupported for embedcontent" in error_message
            )

            if is_unavailable_model:
                self._disable_remote_embeddings = True

            if not self._embedding_fallback_warned:
                LOGGER.warning(
                    "Fallo embedding con Gemini, usando fallback local: %s",
                    error.message,
                )
                if self._disable_remote_embeddings:
                    LOGGER.warning(
                        "Se desactivan intentos de embedding remoto para evitar errores repetidos."
                    )
                self._embedding_fallback_warned = True

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

        api_version = (self.settings.gemini_api_version or "").strip()
        if api_version:
            self._client = genai.Client(
                api_key=self.settings.gemini_api_key,
                http_options={"api_version": api_version},
            )
        else:
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
            content = GeminiService._truncate_text(
                str(message.get("content", "")),
                max_chars=900,
            )
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
            "Instruccion de estilo:\n"
            "- No inicies con saludo ni presentacion personal.\n\n"
            "Responde en formato:\n"
            "- Diagnostico breve\n"
            "- Hallazgos especificos\n"
            "- Recomendaciones accionables\n\n"
            "Profundidad minima esperada:\n"
            "- Entrega una respuesta completa, no una frase corta.\n"
            "- Incluye al menos 6 hallazgos puntuales cuando haya evidencia suficiente."
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
        max_chars: int = 260000,
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
        history: list[dict],
        user_request: str,
    ) -> str:
        history_block = GeminiService._format_history(history)
        request_block = (user_request or "").strip() or (
            "Evalua integralmente esta tesis y prioriza las mejoras de mayor impacto."
        )

        return (
            "Analiza integralmente la tesis y entrega retroalimentacion academica.\n"
            f"Archivo: {filename}\n"
            f"Fragmentos cargados para analisis: {analyzed_chunks} de {total_chunks}\n\n"
            "Solicitud actual del estudiante:\n"
            f"{request_block}\n\n"
            "Historial del chat de revision:\n"
            f"{history_block}\n\n"
            "Contenido de la tesis:\n"
            f"{document_text}\n\n"
            "Instrucciones de formato estrictas:\n"
            "- No incluyas saludos, presentaciones ni preambulos.\n"
            "- Inicia directamente en '1) Veredicto general'.\n"
            "- Desarrolla cada seccion con detalle metodologico y formal.\n"
            "- Usa listas cuando corresponda para mayor claridad.\n\n"
            "Responde con esta estructura exacta:\n"
            "1) Veredicto general (aprobable/no aprobable y por que)\n"
            "2) Fortalezas principales (3-6 puntos)\n"
            "3) Brechas o debilidades (3-8 puntos)\n"
            "4) Que le falta para mejorar (checklist accionable y priorizada)\n"
            "5) Recomendaciones concretas por capitulo o seccion\n"
            "6) Priorizacion final (alta, media, baja)"
        )

    @staticmethod
    def _build_local_thesis_review(
        thesis_text: str,
        analyzed_chunks: int,
        total_chunks: int,
        unavailable_reason: str | None = None,
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

        recommendations_by_section: list[str] = []
        if "objetiv" in text:
            recommendations_by_section.append("- Objetivos: validar correspondencia exacta con preguntas e hipotesis.")
        if "metodolog" in text:
            recommendations_by_section.append("- Metodologia: explicitar poblacion, muestra y justificacion estadistica.")
        if "resultado" in text:
            recommendations_by_section.append("- Resultados: separar descripcion de datos de interpretacion y juicios de valor.")
        if "discusi" in text:
            recommendations_by_section.append("- Discusion: contrastar hallazgos con antecedentes y justificar aceptacion/rechazo de hipotesis.")
        if "conclusion" in text:
            recommendations_by_section.append("- Conclusiones: alinear una conclusion por objetivo y evitar resultados nuevos.")

        if not recommendations_by_section:
            recommendations_by_section.append(
                "- Secciones clave: reforzar problema, objetivos, metodologia, resultados y conclusiones con evidencia."
            )

        priority_block = (
            "- Alta: corregir secciones ausentes y consistencia problema-objetivo-hipotesis.\n"
            "- Media: fortalecer citas, APA y justificacion metodologica.\n"
            "- Baja: pulir redaccion academica, estilo y formato de tablas/figuras."
        )

        provider_note = (
            (unavailable_reason or "").strip()
            or "Gemini no estuvo disponible."
        )

        return (
            "1) Veredicto general\n"
            f"{verdict}.\n\n"
            "2) Fortalezas principales\n"
            f"{strengths_block}\n\n"
            "3) Brechas o debilidades\n"
            f"{missing_block}\n\n"
            "4) Que le falta para mejorar\n"
            f"{recommendations_block}\n\n"
            "5) Recomendaciones concretas por capitulo o seccion\n"
            f"{'\n'.join(recommendations_by_section)}\n\n"
            "6) Priorizacion final\n"
            f"{priority_block}\n\n"
            "Nota tecnica\n"
            "Esta revision se genero con un analisis local de respaldo. "
            f"Motivo proveedor: {provider_note} "
            f"Fragmentos evaluados: {analyzed_chunks} de {total_chunks}."
        )

    @staticmethod
    def _looks_like_complete_structured_review(text: str) -> bool:
        normalized = (text or "").lower()
        if len(normalized.strip()) < MIN_STRUCTURED_REVIEW_CHARS:
            return False

        required_sections = ("1)", "2)", "3)", "4)", "5)")
        hits = sum(1 for marker in required_sections if marker in normalized)
        return hits >= 4

    def _build_contextual_fallback_response(
        self,
        question: str,
        context_chunks: list[dict],
        unavailable_reason: str | None = None,
    ) -> str:
        reason_text = (unavailable_reason or "").strip() or "Gemini no estuvo disponible."

        if not context_chunks:
            return (
                f"No pude usar Gemini en este momento ({reason_text}) y tampoco se recupero contexto util "
                "de la tesis. Intenta nuevamente en unos minutos."
            )

        snippets: list[str] = []
        for index, chunk in enumerate(context_chunks[:8], start=1):
            content = self._truncate_text(chunk.get("content") or "", max_chars=950)
            if content:
                snippets.append(f"- Evidencia {index}: {content}")

        snippets_block = "\n".join(snippets) if snippets else "- Sin fragmentos legibles"
        return (
            f"Gemini no estuvo disponible en este momento ({reason_text}), pero aqui tienes una respuesta "
            "basada en los fragmentos recuperados de tu tesis.\n\n"
            "Diagnostico breve:\n"
            f"La pregunta fue: '{question}'. Con el contexto disponible, estos son los hallazgos mas cercanos.\n\n"
            "Hallazgos especificos (extractivos):\n"
            f"{snippets_block}\n\n"
            "Recomendaciones accionables:\n"
            "1. Vuelve a intentar la consulta para obtener respuesta generativa completa.\n"
            "2. Formula preguntas mas especificas (capitulo, variable, metodo) para aumentar precision.\n"
            "3. Contrasta cada hallazgo con citas y trazabilidad dentro del documento.\n"
            "4. Verifica que tu API key de Gemini tenga cuota y acceso a modelos generativos."
        )

    def review_thesis(
        self,
        filename: str,
        chunks: list[str],
        history: list[dict] | None = None,
        user_request: str = "",
    ) -> tuple[str, int, int]:
        if not chunks:
            raise GeminiServiceError("No hay contenido para evaluar en la tesis.")

        document_text, analyzed_chunks = self._prepare_document_for_review(
            chunks,
            max_chars=max(int(self.settings.gemini_review_max_input_chars), 80000),
        )
        if not document_text or analyzed_chunks == 0:
            raise GeminiServiceError("No se pudo preparar el texto de la tesis para evaluacion.")

        analyzed_characters = len(document_text)
        prompt = self._build_thesis_review_prompt(
            filename=filename,
            total_chunks=len(chunks),
            analyzed_chunks=analyzed_chunks,
            document_text=document_text,
            history=history or [],
            user_request=user_request,
        )

        if self._should_skip_remote_generation():
            fallback = self._build_local_thesis_review(
                thesis_text=document_text,
                analyzed_chunks=analyzed_chunks,
                total_chunks=len(chunks),
                unavailable_reason=self._get_generation_unavailability_reason(),
            )
            return fallback, analyzed_chunks, analyzed_characters

        try:
            self._ensure_ready()
        except GeminiServiceError as error:
            self._mark_generation_unavailable(
                "Gemini no configurado o credenciales invalidas.",
                disable_remote=True,
            )
            if not self._generation_fallback_warned:
                LOGGER.warning(
                    "Gemini no disponible para revision de tesis, usando fallback local: %s",
                    error.message,
                )
                self._generation_fallback_warned = True

            fallback = self._build_local_thesis_review(
                thesis_text=document_text,
                analyzed_chunks=analyzed_chunks,
                total_chunks=len(chunks),
                unavailable_reason=self._get_generation_unavailability_reason(),
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
                        max_output_tokens=max(
                            int(self.settings.gemini_review_max_output_tokens),
                            1024,
                        ),
                        system_instruction=THESIS_REVIEW_SYSTEM_PROMPT,
                    ),
                )
            except Exception as error:  # pragma: no cover - llamada externa
                model_errors.append(f"{model_name}: {error}")
                self._register_generation_failure(str(error))
                continue

            text = self._extract_text_from_generation_response(response)
            if text:
                if not self._looks_like_complete_structured_review(text):
                    model_errors.append(f"{model_name}: respuesta incompleta o demasiado corta")
                    continue

                self._clear_generation_unavailable()
                return text, analyzed_chunks, analyzed_characters

            model_errors.append(f"{model_name}: sin texto util")

        if not self._generation_fallback_warned:
            LOGGER.warning(
                "No se pudo generar revision de tesis con Gemini. Fallback local activado. %s",
                "; ".join(model_errors[:3]) if model_errors else "sin detalles",
            )
            self._generation_fallback_warned = True

        fallback = self._build_local_thesis_review(
            thesis_text=document_text,
            analyzed_chunks=analyzed_chunks,
            total_chunks=len(chunks),
            unavailable_reason=self._get_generation_unavailability_reason(),
        )
        return fallback, analyzed_chunks, analyzed_characters

    def stream_chat_response(
        self,
        question: str,
        context_chunks: list[dict],
        history: list[dict],
    ) -> Generator[str, None, None]:
        if self._should_skip_remote_generation():
            yield self._build_contextual_fallback_response(
                question,
                context_chunks,
                unavailable_reason=self._get_generation_unavailability_reason(),
            )
            return

        try:
            self._ensure_ready()
        except GeminiServiceError as error:
            self._mark_generation_unavailable(
                "Gemini no configurado o credenciales invalidas.",
                disable_remote=True,
            )
            if not self._generation_fallback_warned:
                LOGGER.warning(
                    "Gemini no disponible para chat, usando fallback contextual: %s",
                    error.message,
                )
                self._generation_fallback_warned = True

            yield self._build_contextual_fallback_response(
                question,
                context_chunks,
                unavailable_reason=self._get_generation_unavailability_reason(),
            )
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
                        max_output_tokens=max(
                            int(self.settings.gemini_chat_max_output_tokens),
                            1024,
                        ),
                        system_instruction=SYSTEM_PROMPT,
                    ),
                )
            except Exception as error:  # pragma: no cover - llamada externa
                model_errors.append(f"{model_name}: {error}")
                self._register_generation_failure(str(error))
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
                self._clear_generation_unavailable()
                return

            model_errors.append(f"{model_name}: sin texto util")

        if not self._generation_fallback_warned:
            LOGGER.warning(
                "No se pudo generar respuesta con Gemini. Fallback contextual activado. %s",
                "; ".join(model_errors[:3]) if model_errors else "sin detalles",
            )
            self._generation_fallback_warned = True

        yield self._build_contextual_fallback_response(
            question,
            context_chunks,
            unavailable_reason=self._get_generation_unavailability_reason(),
        )


gemini_service = GeminiService()
