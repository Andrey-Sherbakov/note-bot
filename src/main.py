import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from src.config import settings
from src.notes import router as notes_router

logging.basicConfig(level=logging.INFO)
router = Router()


@router.message(Command("start"))
async def handle_start(message: Message) -> None:
    await message.answer(
        f"Welcome, <b>{message.from_user.full_name}</b>!\nThis is simple note taking bot.\n"
        f"<i>Use /help to see available commands.</i>"
    )


@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    await message.answer("Available commands:\n - /start\n - /help")


async def main() -> None:
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(notes_router)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
