from aiogram import Router

from src.admin.routers import router as admin_router
from src.core.routers import router as base_router
from src.notes.callbacks import router as notes_callbacks_router
from src.notes.routers import router as notes_router

router = Router(name="main_router")

# needs to be first
router.include_router(base_router)

router.include_routers(
    admin_router,
    notes_callbacks_router,
)

# needs to be last
router.include_router(notes_router)