from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.jwt import settings_jwt
from src.core.security import ADMIN_ROLE, decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)

def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized()

    payload = decode_access_token(credentials.credentials)
    if (
        payload is None
        or payload.get("role") != ADMIN_ROLE
        or payload.get("sub") != settings_jwt.ADMIN_LOGIN
    ):
        raise _unauthorized()

    return payload["sub"]
