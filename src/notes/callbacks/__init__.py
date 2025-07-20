from aiogram import Router

from .all import router as all_router
from .base import router as base_router
from .one_note import router as one_note_router

router = Router(name="notes_callbacks_router")

router.include_routers(
    all_router,
    base_router,
    one_note_router,
)

__all__ = [router]