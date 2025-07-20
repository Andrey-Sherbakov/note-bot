from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.notes import service
from src.notes.keyboards.inline import (
    AllNotesInlineCallbackData,
    AllNotesPaginationCallbackData,
    get_notes_pagination_kb,
)

router = Router(name=__name__)


@router.callback_query(AllNotesInlineCallbackData.filter())
async def all_notes_callback(
    callback: CallbackQuery, callback_data: AllNotesInlineCallbackData, state: FSMContext
):
    await service.get_note_state_name(
        callback_data.note_name,
        user_id=callback.from_user.id,
        message=callback.message,
        state=state,
    )
    await callback.answer()


@router.callback_query(AllNotesPaginationCallbackData.filter())
async def all_notes_paginate(
    callback: CallbackQuery, callback_data: AllNotesPaginationCallbackData
):
    page = callback_data.page
    user_id = callback.from_user.id

    notes, total_pages = await service.get_notes_paginated(page=page, user_id=user_id)
    if not notes:
        await callback.answer("Заметки не найдены")
        return

    text = "\n\n".join(f"<b>{note.name.capitalize()}</b>:\n{note.text}" for note in notes)
    if page < total_pages:
        text += "\n\n..."
    if page > 1:
        text = "...\n\n" + text

    kb = get_notes_pagination_kb(notes=notes, page=page, total_pages=total_pages)

    await callback.message.edit_text(text=text, reply_markup=kb)
    await callback.answer()