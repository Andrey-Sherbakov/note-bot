import enum

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# one note
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

    for text, callback in zip(NoteInlineButtons, NoteInlineCallbacks):
        builder.button(text=text, callback_data=callback + note_data)

    builder.adjust(3)
    return builder.as_markup()


# delete note confirmation
class DeleteNoteInlineButtons(enum.StrEnum):
    yes = "Да"
    no = "Нет"


class DeleteNoteInlineCallbacks(enum.StrEnum):
    yes = "delete_note:"
    no = "cancel_delete_note:"


def get_delete_note_inline_kb(note_id: int, note_name: str) -> InlineKeyboardMarkup:
    note_data = f"{note_id},{note_name}"
    builder = InlineKeyboardBuilder()

    for text, callback in zip(DeleteNoteInlineButtons, DeleteNoteInlineCallbacks):
        builder.button(text=text, callback_data=callback + note_data)

    builder.adjust(3)
    return builder.as_markup()