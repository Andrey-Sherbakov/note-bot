import enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Note


# one note
class NoteInlineActions(enum.StrEnum):
    update = "Изменить"
    rename = "Переименовать"
    delete = "❌ Удалить"


class NoteInlineCallbackData(CallbackData, prefix="note_actions"):
    action: NoteInlineActions
    note_id: int
    note_name: str


def get_note_inline_kb(note_id: int, note_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for action in NoteInlineActions:
        builder.button(
            text=action,
            callback_data=NoteInlineCallbackData(
                action=action, note_id=note_id, note_name=note_name
            ).pack(),
        )

    builder.adjust(3)
    return builder.as_markup()


# all notes
class AllNotesInlineCallbackData(CallbackData, prefix="all_notes"):
    note_id: int
    note_name: str


def get_all_notes_inline_kb(notes: list[Note]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for note in notes:
        builder.button(
            text=note.name,
            callback_data=AllNotesInlineCallbackData(note_id=note.id, note_name=note.name).pack(),
        )

    builder.adjust(4)
    return builder.as_markup()


# delete note confirmation
class DeleteNoteInlineActions(enum.StrEnum):
    yes = "Да"
    no = "Нет"


class DeleteNoteCallbackData(CallbackData, prefix="delete_confirmation"):
    action: DeleteNoteInlineActions
    note_id: int
    note_name: str


def get_delete_note_inline_kb(note_id: int, note_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for action in DeleteNoteInlineActions:
        builder.button(
            text=action,
            callback_data=DeleteNoteCallbackData(
                action=action, note_id=note_id, note_name=note_name
            ).pack(),
        )

    return builder.as_markup()
