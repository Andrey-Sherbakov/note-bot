import enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class NoteInlineActions(enum.StrEnum):
    update = "Изменить"
    rename = "Переименовать"
    delete = "❌ Удалить"


class NoteInlineCallbackData(CallbackData, prefix="note_actions"):
    action: NoteInlineActions
    note_id: int


def get_note_inline_kb(note_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for action in NoteInlineActions:
        builder.button(
            text=action,
            callback_data=NoteInlineCallbackData(action=action, note_id=note_id).pack(),
        )

    builder.adjust(3)
    return builder.as_markup()