from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
)
from aiogram.utils.markdown import hbold

from db import repository
from keyboards.inline import (
    AllNotesInlineCallbackData,
    DeleteNoteCallbackData,
    DeleteNoteInlineActions,
)
from service import notes as notes_service

router = Router(name=__name__)


# get all notes callbacks
@router.callback_query(AllNotesInlineCallbackData.filter())
async def all_notes_callback(
    callback: CallbackQuery, callback_data: AllNotesInlineCallbackData, state: FSMContext
):
    await notes_service.start_get_note(
        callback_data.note_name,
        user_id=callback.from_user.id,
        message=callback.message,
        state=state,
    )
    await callback.answer()


# delete note confirmation callbacks
@router.callback_query(DeleteNoteCallbackData.filter(F.action == DeleteNoteInlineActions.yes))
async def delete_note_confirmed_callback(
    callback: CallbackQuery, callback_data: DeleteNoteCallbackData, state: FSMContext
):
    note = await repository.get_by_id(callback_data.note_id, user_id=callback.from_user.id)
    if note is None:
        await callback.message.answer(
            f"Заметка '{hbold(callback_data.note_name.capitalize())}' уже удалена"
        )
    else:
        await repository.delete_note(note)
        await callback.message.answer("Заметка успешно удалена!")
    await callback.answer()
    await state.clear()


@router.callback_query(DeleteNoteCallbackData.filter(F.action == DeleteNoteInlineActions.no))
async def delete_note_cancelled_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Удаление заметки отменено")
    await callback.answer()
    await state.clear()
