import enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Note


class AllNotesActions(enum.StrEnum):
    forward = "Вперед"
    back = "Назад"


class AllNotesInlineCallbackData(CallbackData, prefix="all_notes"):
    note_id: int
    note_name: str


class AddNoteCallbackData(CallbackData, prefix="add_note"):
    name: str


class AllNotesPaginationCallbackData(CallbackData, prefix="notes_page"):
    page: int


def get_similar_notes_kb(notes: list[Note], name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for note in notes:
        builder.button(
            text=note.name,
            callback_data=AllNotesInlineCallbackData(note_id=note.id, note_name=note.name).pack(),
        )
    builder.adjust(4)

    builder.row(
        InlineKeyboardButton(
            text=f"Добавить '{name}'", callback_data=AddNoteCallbackData(name=name).pack()
        )
    )

    return builder.as_markup()


def get_notes_pagination_kb(notes: list[Note], page: int, total_pages: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for note in notes:
        builder.button(
            text=note.name,
            callback_data=AllNotesInlineCallbackData(note_id=note.id, note_name=note.name).pack(),
        )

    if page > 1:
        builder.button(
            text=AllNotesActions.back,
            callback_data=AllNotesPaginationCallbackData(page=page - 1).pack(),
        )
    if page < total_pages:
        builder.button(
            text=AllNotesActions.forward,
            callback_data=AllNotesPaginationCallbackData(page=page + 1).pack(),
        )

    builder.adjust(len(notes), 2)

    return builder.as_markup()