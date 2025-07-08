from aiogram import Router

from src.routers.base import router as base_router
from src.routers.notes import router as notes_router


router = Router(name=__name__)

router.include_routers(
    notes_router,
    base_router,
)

__all__ = [router]