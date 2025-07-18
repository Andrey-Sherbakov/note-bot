from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
)

from keyboards.inline import (
    AllNotesInlineCallbackData,
    DeleteNoteCallbackData,
    DeleteNoteInlineActions,
)
from service import notes_service

router = Router(name=__name__)


# get all notes callbacks
@router.callback_query(AllNotesInlineCallbackData.filter())
async def all_notes_callback(
    callback: CallbackQuery, callback_data: AllNotesInlineCallbackData, state: FSMContext
):
    await notes_service.get_note_state_name(
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
    answer = await notes_service.delete_note_state_confirmed(
        note_id=callback_data.note_id, user_id=callback.from_user.id
    )
    await callback.message.answer(answer)
    await callback.answer()
    await state.clear()


@router.callback_query(DeleteNoteCallbackData.filter(F.action == DeleteNoteInlineActions.no))
async def delete_note_cancelled_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Удаление заметки отменено")
    await callback.answer()
    await state.clear()
