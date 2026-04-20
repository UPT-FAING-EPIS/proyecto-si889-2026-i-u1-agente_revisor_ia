from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class UserPublic(BaseModel):
    id: str
    email: str | None = None


class AuthRequest(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=6, max_length=128)


class AuthResponse(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    expires_in: int | None = None
    token_type: str | None = "bearer"
    user: UserPublic | None = None
    message: str | None = None


class DocumentSummary(BaseModel):
    id: str
    filename: str
    pdf_url: str | None = None
    created_at: datetime | None = None


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    pdf_url: str | None = None
    chunk_count: int
    extracted_characters: int
    replaced_document_id: str | None = None
    replace_warning: str | None = None


class ChatMessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatSessionMode(str, Enum):
    PDF_CHAT = "pdf_chat"
    THESIS_REVIEW = "thesis_review"


class ChatMessage(BaseModel):
    role: ChatMessageRole
    content: str = Field(min_length=1)


class ChatSessionSummary(BaseModel):
    id: str
    document_id: str
    mode: ChatSessionMode
    title: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    last_message_at: datetime | None = None


class ChatSessionCreateRequest(BaseModel):
    document_id: str
    mode: ChatSessionMode = ChatSessionMode.PDF_CHAT
    title: str | None = Field(default=None, min_length=1, max_length=120)


class ChatMessageSummary(BaseModel):
    id: int
    chat_session_id: str
    role: ChatMessageRole
    content: str
    created_at: datetime | None = None


class ChatRequest(BaseModel):
    chat_id: str
    message: str = Field(min_length=1, max_length=4000)
    match_count: int = Field(default=5, ge=1, le=20)


class ThesisReviewRequest(BaseModel):
    document_id: str
    chat_id: str
    message: str = Field(
        default="Evalua integralmente esta tesis y prioriza las mejoras de mayor impacto.",
        min_length=1,
        max_length=4000,
    )


class ThesisReviewResponse(BaseModel):
    chat_id: str
    document_id: str
    filename: str
    review: str
    total_chunks: int
    analyzed_chunks: int
    analyzed_characters: int
