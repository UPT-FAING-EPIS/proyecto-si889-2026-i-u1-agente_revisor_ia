from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user
from app.database.supabase_repository import SupabaseRepositoryError, supabase_repository
from app.models.schemas import ChatSessionMode, ThesisReviewRequest, ThesisReviewResponse, UserPublic
from app.services.gemini_service import GeminiServiceError, gemini_service


router = APIRouter(tags=["thesis-review"])


def _serialize_history(rows: list[dict], limit: int = 16) -> list[dict]:
    history_rows = rows[-limit:]
    return [
        {
            "role": row.get("role") or "user",
            "content": row.get("content") or "",
        }
        for row in history_rows
    ]


@router.post("/thesis/review", response_model=ThesisReviewResponse)
async def review_thesis(
    payload: ThesisReviewRequest,
    current_user: UserPublic = Depends(get_current_user),
) -> ThesisReviewResponse:
    try:
        chat_session = supabase_repository.get_chat_session_by_id(payload.chat_id)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    if not chat_session or chat_session.get("user_id") != current_user.id:
        raise HTTPException(status_code=404, detail="Sesion de chat no encontrada.")

    if chat_session.get("mode") != ChatSessionMode.THESIS_REVIEW.value:
        raise HTTPException(
            status_code=400,
            detail="La sesion no corresponde al modo de revision de tesis.",
        )

    if chat_session.get("document_id") != payload.document_id:
        raise HTTPException(
            status_code=400,
            detail="La sesion de revision no pertenece al documento indicado.",
        )

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
        supabase_repository.create_chat_message(
            chat_session_id=payload.chat_id,
            role="user",
            content=payload.message,
        )
        persisted_messages = supabase_repository.list_chat_messages(payload.chat_id)
        history = _serialize_history(persisted_messages)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    try:
        review, analyzed_chunks, analyzed_characters = gemini_service.review_thesis(
            filename=document.get("filename") or "tesis.pdf",
            chunks=chunks,
            history=history,
            user_request=payload.message,
        )
    except GeminiServiceError as error:
        raise HTTPException(status_code=500, detail=error.message) from error

    try:
        supabase_repository.create_chat_message(
            chat_session_id=payload.chat_id,
            role="assistant",
            content=review,
        )
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return ThesisReviewResponse(
        chat_id=payload.chat_id,
        document_id=document["id"],
        filename=document["filename"],
        review=review,
        total_chunks=len(chunks),
        analyzed_chunks=analyzed_chunks,
        analyzed_characters=analyzed_characters,
    )
