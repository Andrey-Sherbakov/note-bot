from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.core.filters import CommandsFilter
from src.core.keyboards import BaseButtons, get_start_kb

router = Router(name=__name__)


@router.message(CommandsFilter("/start", BaseButtons.start))
async def handle_start(message: Message) -> None:
    await message.answer(
        f"Добро пожаловать, <b>{message.from_user.full_name}</b>!\nЭто простой бот для заметок.\n"
        f"<i>Используй /help чтобы увидеть возможные команды.</i>",
        reply_markup=get_start_kb(),
    )


@router.message(CommandsFilter("/help", BaseButtons.help))
async def handle_help(message: Message) -> None:
    await message.answer("Команды:\n - /start\n - /help\n - /notes\n - /stop")


@router.message(CommandsFilter("/stop", BaseButtons.stop))
async def handle_stop(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"До скорых встреч, {message.from_user.first_name}!\n"
        f"<i>Для начала работы с ботом напишите /start</i>",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.clear()


@router.message(CommandsFilter("/cancel", BaseButtons.cancel))
async def handle_cancel(message: Message, state: FSMContext) -> None:
    await message.answer("Действие отменено.")
    await state.clear()





