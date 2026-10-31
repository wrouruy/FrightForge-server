import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt

from .jwt import settings_jwt

TOKEN_TYPE = "access"
ADMIN_ROLE = "admin"

def verify_admin_credentials(login: str, password: str) -> bool:
    """Constant-time check of the single admin credentials from the environment."""
    login_ok = secrets.compare_digest(login, settings_jwt.ADMIN_LOGIN)
    password_ok = secrets.compare_digest(password, settings_jwt.ADMIN_PASSWORD)
    return login_ok and password_ok


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings_jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"iat": now, "exp": expire, "type": TOKEN_TYPE})
    return jwt.encode(
        to_encode,
        settings_jwt.SECRET_KEY,
        algorithm=settings_jwt.ALGORITHM,
    )


def decode_access_token(token: str) -> Optional[dict[str, Any]]:
    try:
        return jwt.decode(
            token,
            settings_jwt.SECRET_KEY,
            algorithms=[settings_jwt.ALGORITHM],
            options={"require_exp": True, "require_sub": True},
        )
    except JWTError:
        return None
