import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from routers import router as main_router

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.send_message(chat_id=settings.ADMIN, text="Бот запущен.")

    dp.include_router(main_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
