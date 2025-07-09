import enum

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class NoteInlineButtons(enum.StrEnum):
    update = "Изменить"
    rename = "Переименовать"
    delete = "❌ Удалить"


class NoteInlineCallbacks(enum.StrEnum):
    update = "update note:"
    rename = "rename note:"
    delete = "delete note:"


def get_note_inline_kb(note_id: int, note_name: str) -> InlineKeyboardMarkup:
    note_data = f"{note_id},{note_name}"
    builder = InlineKeyboardBuilder()

    builder.button(
        text=NoteInlineButtons.update, callback_data=NoteInlineCallbacks.update + note_data
    )
    builder.button(
        text=NoteInlineButtons.rename, callback_data=NoteInlineCallbacks.rename + note_data
    )
    builder.button(
        text=NoteInlineButtons.delete, callback_data=NoteInlineCallbacks.delete + note_data
    )

    builder.adjust(2)
    return builder.as_markup()