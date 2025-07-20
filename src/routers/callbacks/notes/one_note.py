from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hitalic

from keyboards.inline import NoteInlineCallbackData, NoteInlineActions, get_delete_note_inline_kb
from states import UpdateNoteState, RenameNoteState, DeleteNoteState

router = Router(name=__name__)


@router.callback_query(NoteInlineCallbackData.filter(F.action == NoteInlineActions.update))
async def note_update_callback(
    callback: CallbackQuery, callback_data: NoteInlineCallbackData, state: FSMContext
):
    await callback.message.answer("Изменение заметки:")
    await state.update_data(note_id=callback_data.note_id)
    await state.set_state(UpdateNoteState.text)
    await callback.answer()


@router.callback_query(NoteInlineCallbackData.filter(F.action == NoteInlineActions.rename))
async def note_rename_callback(
    callback: CallbackQuery, callback_data: NoteInlineCallbackData, state: FSMContext
):
    await callback.message.answer("Изменение названия заметки:")
    await state.update_data(note_id=callback_data.note_id)
    await state.set_state(RenameNoteState.new_name)
    await callback.answer()


@router.callback_query(NoteInlineCallbackData.filter(F.action == NoteInlineActions.delete))
async def note_delete_callback(
    callback: CallbackQuery, callback_data: NoteInlineCallbackData, state: FSMContext
):
    await callback.message.answer(
        "Удалить заметку?:\n" + hitalic("Y/Д - Да, N/Н - Нет"),
        reply_markup=get_delete_note_inline_kb(note_id=callback_data.note_id),
    )
    await state.update_data(note_id=callback_data.note_id)
    await state.set_state(DeleteNoteState.confirmation)
    await callback.answer()
