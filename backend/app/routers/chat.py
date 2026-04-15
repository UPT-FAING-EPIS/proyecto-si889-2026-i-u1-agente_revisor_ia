from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.core.auth import get_current_user
from app.database.supabase_repository import SupabaseRepositoryError, supabase_repository
from app.models.schemas import ChatRequest, UserPublic
from app.services.gemini_service import GeminiServiceError, gemini_service


router = APIRouter(tags=["chat"])


def _response_stream(
    question: str,
    context_chunks: list[dict],
    history: list[dict],
) -> Generator[str, None, None]:
    try:
        for token in gemini_service.stream_chat_response(
            question=question,
            context_chunks=context_chunks,
            history=history,
        ):
            yield token
    except GeminiServiceError:
        yield "No se pudo completar la respuesta en este momento. Intenta de nuevo."


@router.post("/chat")
async def chat_with_document(
    payload: ChatRequest,
    current_user: UserPublic = Depends(get_current_user),
) -> StreamingResponse:
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
        query_embedding = gemini_service.embed_query(payload.message)
        context_chunks = supabase_repository.match_document_chunks(
            document_id=payload.document_id,
            query_embedding=query_embedding,
            match_count=payload.match_count,
            query_text=payload.message,
        )
    except (GeminiServiceError, SupabaseRepositoryError) as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    history = [message.model_dump() for message in payload.history]

    return StreamingResponse(
        _response_stream(
            question=payload.message,
            context_chunks=context_chunks,
            history=history,
        ),
        media_type="text/plain; charset=utf-8",
    )
