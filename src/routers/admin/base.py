from aiogram import Router
from aiogram.types import Message

from keyboards.reply import (
    get_admin_kb,
    NoteBotActions,
    AdminActions,
    AdminCommands,
)
from service import CommandsFilter

router = Router(name=__name__)


@router.message(CommandsFilter("/admin", admin=True))
async def handle_admin(message: Message) -> None:
    await message.answer("Администрирование сервера", reply_markup=get_admin_kb())


@router.message(
    CommandsFilter(
        "/admin",
        AdminCommands.note_bot,
        AdminCommands.pomodoro,
        AdminCommands.notification_service,
        AdminActions.note_bot,
        AdminActions.pomodoro,
        AdminActions.notification_service,
        NoteBotActions.restart,
        NoteBotActions.down,
        NoteBotActions.up,
    )
)
async def handle_admin_false(message: Message) -> None:
    await message.answer("У вас недостаточно прав для этого действия")