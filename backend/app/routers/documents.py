from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.auth import get_current_user
from app.database.supabase_repository import SupabaseRepositoryError, supabase_repository
from app.models.schemas import DocumentSummary, UploadResponse, UserPublic
from app.services.gemini_service import GeminiServiceError, gemini_service
from app.services.pdf_service import PDFServiceError, pdf_service


router = APIRouter(tags=["documents"])


@router.get("/documents", response_model=list[DocumentSummary])
async def list_documents(current_user: UserPublic = Depends(get_current_user)) -> list[DocumentSummary]:
    try:
        items = supabase_repository.list_documents(current_user.id)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return [DocumentSummary(**item) for item in items]


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: UserPublic = Depends(get_current_user),
) -> UploadResponse:
    filename = file.filename or "documento.pdf"
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="El archivo enviado esta vacio.")

    try:
        extracted_text = pdf_service.extract_text(file_bytes)
        chunks = pdf_service.chunk_text(extracted_text)
    except PDFServiceError as error:
        raise HTTPException(status_code=400, detail=error.message) from error

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No se pudieron generar fragmentos utiles del PDF.",
        )

    try:
        document = supabase_repository.create_document(current_user.id, filename)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    try:
        embeddings = gemini_service.embed_documents(chunks)
        chunk_count = supabase_repository.insert_document_chunks(
            document_id=document["id"],
            chunks=chunks,
            embeddings=embeddings,
        )
    except (GeminiServiceError, SupabaseRepositoryError) as error:
        try:
            supabase_repository.delete_document(document["id"])
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=str(error)) from error

    return UploadResponse(
        document_id=document["id"],
        filename=document["filename"],
        chunk_count=chunk_count,
        extracted_characters=len(extracted_text),
    )
