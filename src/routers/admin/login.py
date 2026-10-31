import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from src.routers.admin.dependencies import get_current_admin
from src.core.jwt import settings_jwt
from src.core.security import ADMIN_ROLE, create_access_token, verify_admin_credentials

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"])

class LoginRequest(BaseModel):
    login: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=200)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest) -> TokenResponse:
    if not verify_admin_credentials(body.login, body.password):
        logger.warning("Failed admin login attempt for login %r", body.login)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        {"sub": settings_jwt.ADMIN_LOGIN, "role": ADMIN_ROLE}
    )

    return TokenResponse(
        access_token=token,
        expires_in=settings_jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
