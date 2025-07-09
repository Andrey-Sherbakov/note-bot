from aiogram import Router

from .base import router as base_router
from .notes import router as notes_router
from .callback import router as callback_router


router = Router(name=__name__)

router.include_routers(
    callback_router,
    base_router,
    notes_router,
)

__all__ = [router]