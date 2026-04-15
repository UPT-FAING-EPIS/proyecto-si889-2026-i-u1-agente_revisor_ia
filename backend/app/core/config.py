from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Asesor IA de Tesis API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"

    gemini_api_key: str = Field(
        default="",
        validation_alias=AliasChoices("GEMINI_API_KEY", "API_GEMINI"),
    )
    gemini_chat_model: str = Field(default="gemini-2.0-flash")
    gemini_embedding_model: str = Field(default="models/text-embedding-004")
    gemini_embedding_output_dimensionality: int = Field(
        default=3072,
        validation_alias=AliasChoices("GEMINI_EMBEDDING_OUTPUT_DIMENSIONALITY"),
    )

    supabase_url: str = Field(
        default="",
        validation_alias=AliasChoices("SUPABASE_URL", "NEXT_PUBLIC_SUPABASE_URL"),
    )
    supabase_publishable_key: str = Field(
        default="",
        validation_alias=AliasChoices(
            "SUPABASE_PUBLISHABLE_KEY",
            "NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY",
        ),
    )
    supabase_service_role_key: str = Field(default="")
    supabase_storage_bucket: str = Field(
        default="thesis-documents",
        validation_alias=AliasChoices("SUPABASE_STORAGE_BUCKET"),
    )
    supabase_storage_signed_url_expires_seconds: int = Field(
        default=3600,
        validation_alias=AliasChoices("SUPABASE_STORAGE_SIGNED_URL_EXPIRES_SECONDS"),
    )

    cors_origins: str = Field(
        default="http://localhost:3000",
        validation_alias=AliasChoices("CORS_ORIGINS", "FRONTEND_ORIGINS"),
    )
    cors_origin_regex: str = Field(
        default=r"https://.*\\.app\\.github\\.dev",
        validation_alias=AliasChoices("CORS_ORIGIN_REGEX"),
    )

    @property
    def supabase_key(self) -> str:
        return self.supabase_service_role_key or self.supabase_publishable_key

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin and origin.strip()
        ]


@lru_cache

def get_settings() -> Settings:
    return Settings()
