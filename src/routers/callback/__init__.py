from aiogram import Router

from .notes import router as notes_callback_router

router = Router(name=__name__)

router.include_routers(
    notes_callback_router,
)

__all__ = [router]