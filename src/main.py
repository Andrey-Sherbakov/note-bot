import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from src.config import settings

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()


@dp.message(Command("start"))
async def handle_start(message: Message) -> None:
    await message.answer(
        f"Welcome, {message.from_user.full_name}!\nThis is simple note taking bot.\n"
        f"Use /help to see available commands."
    )


@dp.message(Command("help"))
async def handle_help(message: Message) -> None:
    await message.answer("Available commands:\n - /start\n - /help")


async def main() -> None:
    bot = Bot(token=settings.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
