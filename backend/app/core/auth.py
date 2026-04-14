from fastapi import Header, HTTPException, status

from app.models.schemas import UserPublic
from app.services.supabase_auth_service import AuthServiceError, supabase_auth_service


async def get_current_user(
    authorization: str | None = Header(default=None),
) -> UserPublic:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acceso faltante o invalido.",
        )

    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acceso vacio.",
        )

    try:
        payload = await supabase_auth_service.get_user(token)
    except AuthServiceError as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message,
        ) from error

    return UserPublic(id=payload["id"], email=payload.get("email"))
