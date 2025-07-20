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