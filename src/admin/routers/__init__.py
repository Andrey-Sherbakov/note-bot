from aiogram import Router

from src.admin.routers.base import router as base_router
from src.admin.routers.note_bot import router as note_bot_router
from src.admin.routers.notification_service import router as notification_service_router
from src.admin.routers.pomodoro import router as pomodoro_router

router = Router(name="admin_router")

router.include_routers(
    note_bot_router,
    notification_service_router,
    pomodoro_router,
)
# needs to be last
router.include_router(base_router)