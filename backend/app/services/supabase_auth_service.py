import httpx

from app.core.config import get_settings


class AuthServiceError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class SupabaseAuthService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.timeout_seconds = 20.0

    @property
    def base_url(self) -> str:
        if not self.settings.supabase_url:
            raise AuthServiceError(
                "SUPABASE_URL no esta configurado en las variables de entorno.",
                status_code=500,
            )
        return self.settings.supabase_url.rstrip("/")

    @property
    def apikey(self) -> str:
        key = self.settings.supabase_publishable_key or self.settings.supabase_service_role_key
        if not key:
            raise AuthServiceError(
                "SUPABASE_PUBLISHABLE_KEY o SUPABASE_SERVICE_ROLE_KEY no esta configurado.",
                status_code=500,
            )
        return key

    def _build_headers(self, access_token: str | None = None) -> dict[str, str]:
        headers = {
            "apikey": self.apikey,
            "Content-Type": "application/json",
        }
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        return headers

    @staticmethod
    def _extract_error_message(response: httpx.Response) -> str:
        try:
            payload = response.json()
        except ValueError:
            return f"Error de autenticacion ({response.status_code})."

        return (
            payload.get("error_description")
            or payload.get("msg")
            or payload.get("message")
            or payload.get("error")
            or f"Error de autenticacion ({response.status_code})."
        )

    async def _request(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
        access_token: str | None = None,
    ) -> dict:
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.request(
                method=method,
                url=url,
                json=payload,
                headers=self._build_headers(access_token),
            )

        if response.status_code >= 400:
            raise AuthServiceError(
                message=self._extract_error_message(response),
                status_code=response.status_code,
            )

        if not response.content:
            return {}

        return response.json()

    async def register(self, email: str, password: str) -> dict:
        return await self._request(
            method="POST",
            path="/auth/v1/signup",
            payload={"email": email, "password": password},
        )

    async def login(self, email: str, password: str) -> dict:
        return await self._request(
            method="POST",
            path="/auth/v1/token?grant_type=password",
            payload={"email": email, "password": password},
        )

    async def get_user(self, access_token: str) -> dict:
        payload = await self._request(
            method="GET",
            path="/auth/v1/user",
            access_token=access_token,
        )
        if "id" not in payload:
            raise AuthServiceError(
                message="No se pudo validar el usuario autenticado.",
                status_code=401,
            )
        return payload


supabase_auth_service = SupabaseAuthService()
