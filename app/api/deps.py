import secrets
from fastapi import HTTPException, Header, status, Security
from fastapi.security import APIKeyHeader
from app.config import API_KEYS

_api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)

def require_api_key(
        x_api_key: str | None = Security(_api_key_scheme),
) -> None:
    if not API_KEYS:
        return
    if not x_api_key or not any(secrets.compare_digest(x_api_key, key) for key in API_KEYS):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key",
            headers={"WWW-Authenticate":"ApiKey"},
        )