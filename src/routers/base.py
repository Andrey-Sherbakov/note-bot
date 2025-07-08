from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.keyboards import BaseButtons, StartButtons, get_start_kb

router = Router(name=__name__)


@router.message(F.text == BaseButtons.start)
@router.message(Command("start"))
async def handle_start(message: Message) -> None:
    await message.answer(
        f"Welcome, <b>{message.from_user.full_name}</b>!\nThis is simple note taking bot.\n"
        f"<i>Use /help to see available commands.</i>",
        reply_markup=get_start_kb(),
    )


@router.message(F.text == StartButtons.help)
@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    await message.answer("Available commands:\n - /start\n - /help")


@router.message(F.text == BaseButtons.stop)
@router.message(Command("stop"))
async def handle_stop(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"До скорых встреч, {message.from_user.first_name}!\n"
        f"<i>Для начала работы с ботом напишите /start</i>",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.clear()