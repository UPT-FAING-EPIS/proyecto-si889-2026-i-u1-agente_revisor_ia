import re
from io import BytesIO

from pypdf import PdfReader


class PDFServiceError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class PDFService:
    def extract_text(self, file_bytes: bytes) -> str:
        if not file_bytes:
            raise PDFServiceError("El archivo PDF esta vacio.")

        try:
            reader = PdfReader(BytesIO(file_bytes))
        except Exception as error:  # pragma: no cover - depende del parser externo
            raise PDFServiceError("No se pudo abrir el PDF enviado.") from error

        pages_text: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                pages_text.append(page_text)

        full_text = "\n\n".join(pages_text).strip()
        if not full_text:
            raise PDFServiceError(
                "No se encontro texto legible en el PDF. Verifica que no sea escaneado."
            )

        return full_text

    @staticmethod
    def _normalize_paragraph(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def chunk_text(
        self,
        text: str,
        max_chunk_chars: int = 1200,
    ) -> list[str]:
        raw_paragraphs = re.split(r"\n\s*\n+", text)
        paragraphs = [
            self._normalize_paragraph(paragraph)
            for paragraph in raw_paragraphs
            if self._normalize_paragraph(paragraph)
        ]

        if not paragraphs:
            return []

        chunks: list[str] = []
        current = ""

        for paragraph in paragraphs:
            candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
            if len(candidate) <= max_chunk_chars:
                current = candidate
                continue

            if current:
                chunks.append(current)

            if len(paragraph) <= max_chunk_chars:
                current = paragraph
                continue

            for index in range(0, len(paragraph), max_chunk_chars):
                piece = paragraph[index : index + max_chunk_chars].strip()
                if piece:
                    chunks.append(piece)
            current = ""

        if current:
            chunks.append(current)

        # Evita fragmentos demasiado pequenos que no aportan contexto semantico.
        return [chunk for chunk in chunks if len(chunk) >= 50]


pdf_service = PDFService()
