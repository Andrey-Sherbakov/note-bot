from aiogram import Router

from .base import router as base_router
from .one_note import router as one_note_router

router = Router(name="notes_callbacks_router")

router.include_routers(
    base_router,
    one_note_router,
)

__all__ = [router]