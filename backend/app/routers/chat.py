from collections.abc import Generator
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse

from app.core.auth import get_current_user
from app.database.supabase_repository import SupabaseRepositoryError, supabase_repository
from app.models.schemas import (
    ChatMessageSummary,
    ChatRequest,
    ChatSessionCreateRequest,
    ChatSessionMode,
    ChatSessionSummary,
    UserPublic,
)
from app.services.gemini_service import GeminiServiceError, gemini_service


router = APIRouter(tags=["chat"])
LOGGER = logging.getLogger(__name__)


def _serialize_history(rows: list[dict], limit: int = 40) -> list[dict]:
    history_rows = rows[-limit:]
    return [
        {
            "role": row.get("role") or "user",
            "content": row.get("content") or "",
        }
        for row in history_rows
    ]


def _response_stream(
    question: str,
    context_chunks: list[dict],
    history: list[dict],
    chat_id: str,
) -> Generator[str, None, None]:
    chunks: list[str] = []

    try:
        for token in gemini_service.stream_chat_response(
            question=question,
            context_chunks=context_chunks,
            history=history,
        ):
            chunks.append(token)
            yield token
    except GeminiServiceError:
        fallback = "No se pudo completar la respuesta en este momento. Intenta de nuevo."
        chunks = [fallback]
        yield fallback
    finally:
        response_text = "".join(chunks).strip()
        if not response_text:
            return

        try:
            supabase_repository.create_chat_message(
                chat_session_id=chat_id,
                role="assistant",
                content=response_text,
            )
        except SupabaseRepositoryError as error:
            LOGGER.warning("No se pudo persistir respuesta asistente en chat=%s: %s", chat_id, error)


@router.get("/chats", response_model=list[ChatSessionSummary])
async def list_chat_sessions(
    document_id: str | None = Query(default=None),
    mode: ChatSessionMode | None = Query(default=None),
    current_user: UserPublic = Depends(get_current_user),
) -> list[ChatSessionSummary]:
    try:
        sessions = supabase_repository.list_chat_sessions(
            user_id=current_user.id,
            document_id=document_id,
            mode=mode.value if mode else None,
        )
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return [ChatSessionSummary(**session) for session in sessions]


@router.post("/chats", response_model=ChatSessionSummary, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    payload: ChatSessionCreateRequest,
    current_user: UserPublic = Depends(get_current_user),
) -> ChatSessionSummary:
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
        session = supabase_repository.create_chat_session(
            user_id=current_user.id,
            document_id=payload.document_id,
            mode=payload.mode.value,
            title=payload.title,
        )
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return ChatSessionSummary(**session)


@router.get("/chats/{chat_id}/messages", response_model=list[ChatMessageSummary])
async def list_chat_messages(
    chat_id: str,
    current_user: UserPublic = Depends(get_current_user),
) -> list[ChatMessageSummary]:
    try:
        chat_session = supabase_repository.get_chat_session_by_id(chat_id)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    if not chat_session or chat_session.get("user_id") != current_user.id:
        raise HTTPException(status_code=404, detail="Sesion de chat no encontrada.")

    try:
        messages = supabase_repository.list_chat_messages(chat_id)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return [ChatMessageSummary(**message) for message in messages]


@router.post("/chat")
async def chat_with_document(
    payload: ChatRequest,
    current_user: UserPublic = Depends(get_current_user),
) -> StreamingResponse:
    try:
        chat_session = supabase_repository.get_chat_session_by_id(payload.chat_id)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    if not chat_session or chat_session.get("user_id") != current_user.id:
        raise HTTPException(status_code=404, detail="Sesion de chat no encontrada.")

    if chat_session.get("mode") != ChatSessionMode.PDF_CHAT.value:
        raise HTTPException(
            status_code=400,
            detail="La sesion no corresponde al modo de chat sobre PDF.",
        )

    document_id = chat_session.get("document_id")
    if not document_id:
        raise HTTPException(status_code=400, detail="La sesion de chat no tiene documento asociado.")

    try:
        document = supabase_repository.get_document_by_id(document_id)
    except SupabaseRepositoryError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    if not document or document.get("user_id") != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado para el usuario autenticado.",
        )

    try:
        supabase_repository.create_chat_message(
            chat_session_id=payload.chat_id,
            role="user",
            content=payload.message,
        )
        persisted_messages = supabase_repository.list_chat_messages(payload.chat_id)
        history = _serialize_history(persisted_messages)

        query_embedding = gemini_service.embed_query(payload.message)
        context_chunks = supabase_repository.match_document_chunks(
            document_id=document_id,
            query_embedding=query_embedding,
            match_count=payload.match_count,
            query_text=payload.message,
        )
    except (GeminiServiceError, SupabaseRepositoryError) as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return StreamingResponse(
        _response_stream(
            question=payload.message,
            context_chunks=context_chunks,
            history=history,
            chat_id=payload.chat_id,
        ),
        media_type="text/plain; charset=utf-8",
    )
