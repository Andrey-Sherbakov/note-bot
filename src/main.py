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
    await message.answer(f"This simple note taking bot.\nWelcome, {message.from_user.full_name}!")


async def main() -> None:
    bot = Bot(token=settings.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
