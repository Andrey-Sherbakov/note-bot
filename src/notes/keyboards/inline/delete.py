import enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class DeleteNoteInlineActions(enum.StrEnum):
    yes = "Да"
    no = "Нет"


class DeleteNoteCallbackData(CallbackData, prefix="delete_confirmation"):
    action: DeleteNoteInlineActions
    note_id: int


def get_delete_note_inline_kb(note_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for action in DeleteNoteInlineActions:
        builder.button(
            text=action,
            callback_data=DeleteNoteCallbackData(action=action, note_id=note_id).pack(),
        )

    return builder.as_markup()