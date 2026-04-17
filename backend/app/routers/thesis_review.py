from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user
from app.database.supabase_repository import SupabaseRepositoryError, supabase_repository
from app.models.schemas import ThesisReviewRequest, ThesisReviewResponse, UserPublic
from app.services.gemini_service import GeminiServiceError, gemini_service


router = APIRouter(tags=["thesis-review"])


@router.post("/thesis/review", response_model=ThesisReviewResponse)
async def review_thesis(
    payload: ThesisReviewRequest,
    current_user: UserPublic = Depends(get_current_user),
) -> ThesisReviewResponse:
    try:
        document = supabase_repository.get_document_by_id(payload.document_id)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    if not document or document.get("user_id") != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado para el usuario autenticado.",
        )

    try:
        chunks = supabase_repository.list_document_chunks(payload.document_id)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="La tesis aun no tiene fragmentos procesados para evaluar.",
        )

    try:
        review, analyzed_chunks, analyzed_characters = gemini_service.review_thesis(
            filename=document.get("filename") or "tesis.pdf",
            chunks=chunks,
        )
    except GeminiServiceError as error:
        raise HTTPException(status_code=500, detail=error.message) from error

    return ThesisReviewResponse(
        document_id=document["id"],
        filename=document["filename"],
        review=review,
        total_chunks=len(chunks),
        analyzed_chunks=analyzed_chunks,
        analyzed_characters=analyzed_characters,
    )
