from aiogram import Router

from .base import router as base_router
from .notes import router as notes_router
from .callbacks import router as callback_router


router = Router(name="main_router")

router.include_routers(
    callback_router,
    base_router,
)
# needs to be last
router.include_router(notes_router)

__all__ = [router]
