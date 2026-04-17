from datetime import datetime

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


class ChatMessage(BaseModel):
    role: str
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    document_id: str
    message: str = Field(min_length=1, max_length=4000)
    history: list[ChatMessage] = Field(default_factory=list)
    match_count: int = Field(default=5, ge=1, le=20)


class ThesisReviewRequest(BaseModel):
    document_id: str


class ThesisReviewResponse(BaseModel):
    document_id: str
    filename: str
    review: str
    total_chunks: int
    analyzed_chunks: int
    analyzed_characters: int
