from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
)
from aiogram.utils.markdown import hbold

from keyboards.inline import NoteInlineCallbacks
from states import UpdateNoteState

router = Router(name=__name__)


@router.callback_query(F.data.startswith(NoteInlineCallbacks.update))
async def note_update_callback(callback: CallbackQuery, state: FSMContext):
    note_id, note_name = callback.data.split(":")[1].split(",")

    await callback.message.answer(f"Изменение заметки - {hbold(note_name.capitalize())}:")
    await state.update_data(note_id=int(note_id))
    await state.set_state(UpdateNoteState.text)

