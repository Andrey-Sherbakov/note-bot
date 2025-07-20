from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import settings
from keyboards.reply import BaseButtons, get_start_kb, StartButtons

router = Router(name=__name__)


@router.message(F.text == BaseButtons.start)
@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        f"Добро пожаловать, <b>{message.from_user.full_name}</b>!\nЭто простой бот для заметок.\n"
        f"<i>Используй /help чтобы увидеть возможные команды.</i>",
        reply_markup=get_start_kb(),
    )


@router.message(F.text == StartButtons.help)
@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    await message.answer("Команды:\n - /start\n - /help\n - /notes\n - /stop")


@router.message(F.text == BaseButtons.stop)
@router.message(Command("stop"))
async def handle_stop(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"До скорых встреч, {message.from_user.first_name}!\n"
        f"<i>Для начала работы с ботом напишите /start</i>",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.clear()


@router.message(F.text == BaseButtons.restart)
@router.message(Command("restart"))
async def handle_restart(message: Message) -> None:
    if message.from_user.id != settings.ADMIN:
        await message.answer("У вас нет прав на это действие")
        return

    await message.answer("Перезапускаю контейнеры")

    with open("/tmp/bot_pipe", "w") as pipe:
        pipe.write("make -C /note-bot restart\n")


