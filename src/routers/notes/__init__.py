from aiogram import Router

from .add import router as add_router
from .base import router as base_router
from .delete import router as delete_router
from .get import router as get_router
from .rename import router as rename_router
from .update import router as update_router

router = Router(name="notes_router")

router.include_routers(
    add_router,
    delete_router,
    get_router,
    rename_router,
    update_router,
)
# needs to be last
router.include_router(base_router)

__all__ = [router]