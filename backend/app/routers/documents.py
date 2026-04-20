from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

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


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    current_user: UserPublic = Depends(get_current_user),
) -> None:
    try:
        document = supabase_repository.get_document_by_id(document_id)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    if not document or document.get("user_id") != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado para el usuario autenticado.",
        )

    storage_path = supabase_repository.resolve_document_pdf_storage_path(
        user_id=current_user.id,
        document_id=document["id"],
        filename=document.get("filename") or "documento.pdf",
        pdf_storage_path=document.get("pdf_storage_path"),
    )

    try:
        supabase_repository.delete_document_pdf(storage_path)
        supabase_repository.delete_document(document_id)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    replace_document_id: str | None = Form(default=None),
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

    replace_target_id = (replace_document_id or "").strip()
    document_to_replace: dict | None = None
    if replace_target_id:
        try:
            document_to_replace = supabase_repository.get_document_by_id(replace_target_id)
        except SupabaseRepositoryError as error:
            raise HTTPException(status_code=500, detail=str(error)) from error

        if not document_to_replace or document_to_replace.get("user_id") != current_user.id:
            raise HTTPException(
                status_code=404,
                detail="El documento que intentas reemplazar no existe para este usuario.",
            )

    try:
        document = supabase_repository.create_document(current_user.id, filename)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    storage_path = ""
    try:
        storage_path = supabase_repository.upload_document_pdf(
            user_id=current_user.id,
            document_id=document["id"],
            filename=document["filename"],
            file_bytes=file_bytes,
        )
    except SupabaseRepositoryError as error:
        try:
            supabase_repository.delete_document(document["id"])
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=str(error)) from error

    try:
        supabase_repository.update_document_pdf_metadata(
            document_id=document["id"],
            pdf_storage_path=storage_path,
            pdf_size_bytes=len(file_bytes),
            pdf_mime_type=(file.content_type or "application/pdf"),
        )
        document["pdf_storage_path"] = storage_path
    except SupabaseRepositoryError as error:
        try:
            supabase_repository.delete_document_pdf(storage_path)
        except Exception:
            pass
        try:
            supabase_repository.delete_document(document["id"])
        except Exception:
            pass
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
            supabase_repository.delete_document_pdf(storage_path)
        except Exception:
            pass
        try:
            supabase_repository.delete_document(document["id"])
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=str(error)) from error

    replaced_document_id: str | None = None
    replace_warning: str | None = None
    if document_to_replace and document_to_replace.get("id") != document["id"]:
        replace_storage_path = supabase_repository.resolve_document_pdf_storage_path(
            user_id=current_user.id,
            document_id=document_to_replace["id"],
            filename=document_to_replace.get("filename") or "documento.pdf",
            pdf_storage_path=document_to_replace.get("pdf_storage_path"),
        )

        try:
            supabase_repository.delete_document_pdf(replace_storage_path)
            supabase_repository.delete_document(document_to_replace["id"])
            replaced_document_id = document_to_replace["id"]
        except SupabaseRepositoryError as error:
            replace_warning = (
                "El nuevo PDF se subio correctamente, pero no se pudo eliminar el PDF anterior. "
                f"Detalle: {error}"
            )

    try:
        pdf_url = supabase_repository.get_document_pdf_url(
            user_id=current_user.id,
            document_id=document["id"],
            filename=document["filename"],
            pdf_storage_path=document.get("pdf_storage_path") or storage_path,
        )
    except SupabaseRepositoryError:
        pdf_url = None

    return UploadResponse(
        document_id=document["id"],
        filename=document["filename"],
        pdf_url=pdf_url,
        chunk_count=chunk_count,
        extracted_characters=len(extracted_text),
        replaced_document_id=replaced_document_id,
        replace_warning=replace_warning,
    )
