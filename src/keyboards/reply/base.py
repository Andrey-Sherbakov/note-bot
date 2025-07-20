import enum

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class BaseButtons(enum.StrEnum):
    start = "Старт"
    stop = "Конец"
    restart = "Перезапуск"


class StartButtons(enum.StrEnum):
    help = "Помощь"
    notes = "Заметки"
    stop = BaseButtons.stop


def get_start_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for button in StartButtons:
        builder.button(text=button)

    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)
