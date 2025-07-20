import html
import os

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import (
    get_admin_kb,
    NoteBotActions,
    AdminActions,
    AdminCommands,
    NotificationServiceActions,
    BaseButtons,
)
from service import CommandsFilter

router = Router(name=__name__)


@router.message(CommandsFilter("/admin", BaseButtons.admin, admin=True))
async def handle_admin(message: Message, state: FSMContext) -> None:
    await message.answer("Администрирование сервера", reply_markup=get_admin_kb())
    await state.clear()


@router.message(CommandsFilter(AdminCommands.logs, AdminActions.logs, admin=True))
async def handle_logs(message: Message) -> None:
    file_path = "../logs/pipelogs.txt"

    if not os.path.isfile(file_path):
        await message.answer(f"Файл логов не найден по пути: {file_path}")
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            logs = f.read().strip()
            await message.answer(
                text=f"Последние логи из `pipelogs.txt`:\n\n{html.escape(logs, quote=False)}"
            )


@router.message(
    CommandsFilter(
        "/admin",
        iterables=[
            AdminCommands,
            AdminActions,
            NoteBotActions,
            NotificationServiceActions,
        ],
    )
)
async def handle_admin_false(message: Message) -> None:
    await message.answer("У вас недостаточно прав для этого действия")