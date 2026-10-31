from fastapi import APIRouter, Depends

from src.routers.admin.dependencies import get_current_admin

from . import login, pending_costumes, set_costume_status

router = APIRouter()

# The login endpoint is public, every other admin endpoint requires a valid JWT
router.include_router(login.router)
router.include_router(
    pending_costumes.router, dependencies=[Depends(get_current_admin)]
)
router.include_router(
    set_costume_status.router, dependencies=[Depends(get_current_admin)]
)
