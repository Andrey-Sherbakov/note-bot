import enum
from typing import Iterable

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class BaseButtons(enum.StrEnum):
    start = "Старт"
    help = "Помощь"
    stop = "Конец"
    cancel = "Отмена"
    notes = "Заметки"
    admin = "Админ-Панель"


class StartButtons(enum.StrEnum):
    notes = BaseButtons.notes
    help = BaseButtons.help
    admin = BaseButtons.admin
    stop = BaseButtons.stop


def get_reply_kb(seq: Iterable[str], adjust: tuple[int, ...] = 3) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for button in seq:
        builder.button(text=button)

    builder.adjust(*adjust)
    return builder.as_markup(resize_keyboard=True)


def get_start_kb() -> ReplyKeyboardMarkup:
    return get_reply_kb(StartButtons, adjust=(2,))
