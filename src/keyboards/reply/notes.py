import enum

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from keyboards.reply.base import BaseButtons


class NotesButtons(enum.StrEnum):
    all = "Все"
    get = "Одна"
    add = "Добавить"
    rename = "Переименовать"
    update = "Изменить"
    delete = "Удалить"
    start = BaseButtons.start
    stop = BaseButtons.stop


def get_notes_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for button in NotesButtons:
        builder.button(text=button)

    builder.adjust(3, 3, 2)
    return builder.as_markup(resize_keyboard=True)
