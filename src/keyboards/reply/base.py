import enum
from typing import Iterable

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class BaseButtons(enum.StrEnum):
    start = "Старт"
    stop = "Конец"


class StartButtons(enum.StrEnum):
    help = "Помощь"
    notes = "Заметки"
    stop = BaseButtons.stop


def get_reply_kb(seq: Iterable[str], adjust: int = 3) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for button in seq:
        builder.button(text=button)

    builder.adjust(adjust)
    return builder.as_markup(resize_keyboard=True)


def get_start_kb() -> ReplyKeyboardMarkup:
    return get_reply_kb(StartButtons, adjust=2)
