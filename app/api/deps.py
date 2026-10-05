import secrets
from fastapi import HTTPException, Header, status
from app.config import API_KEYS

def require_api_key(
        x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    if not API_KEYS:
        return
    if not x_api_key or not any(secrets.compare_digest(x_api_key, key) for key in API_KEYS):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key",
            headers={"WWW-Authenticate":"ApiKey"},
        )