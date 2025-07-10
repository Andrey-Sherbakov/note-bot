from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
)
from aiogram.utils.markdown import hbold, hitalic

from keyboards.inline import NoteInlineCallbacks, get_delete_note_inline_kb
from states import UpdateNoteState, RenameNoteState, DeleteNoteState

router = Router(name=__name__)


@router.callback_query(F.data.startswith(NoteInlineCallbacks.update))
async def note_update_callback(callback: CallbackQuery, state: FSMContext):
    note_id, note_name = callback.data.split(":")[1].split(",")

    await callback.message.answer(f"Изменение заметки - {hbold(note_name.capitalize())}:")
    await state.update_data(note_id=int(note_id))
    await state.set_state(UpdateNoteState.text)


@router.callback_query(F.data.startswith(NoteInlineCallbacks.rename))
async def note_rename_callback(callback: CallbackQuery, state: FSMContext):
    note_id, note_name = callback.data.split(":")[1].split(",")

    await callback.message.answer(f"Изменение названия заметки - {hbold(note_name.capitalize())}:")
    await state.update_data(note_id=int(note_id))
    await state.set_state(RenameNoteState.new_name)


@router.callback_query(F.data.startswith(NoteInlineCallbacks.delete))
async def note_rename_callback(callback: CallbackQuery, state: FSMContext):
    note_id, note_name = callback.data.split(":")[1].split(",")

    await callback.message.answer(
        f"Удалить заметку - {hbold(note_name)}?:\n" + hitalic("Y/Д - Yes/Да, N/Н - No/Нет"),
        reply_markup=get_delete_note_inline_kb(note_id=int(note_id), note_name=note_name),
    )
    await state.update_data(note_id=int(note_id))
    await state.set_state(DeleteNoteState.confirmation)