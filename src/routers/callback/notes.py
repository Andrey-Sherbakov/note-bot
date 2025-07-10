from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
)
from aiogram.utils.markdown import hbold, hitalic

from db import repository
from keyboards.inline import (
    NoteInlineActions,
    NoteInlineCallbackData,
    AllNotesInlineCallbackData,
    get_delete_note_inline_kb,
    DeleteNoteCallbackData,
    DeleteNoteInlineActions,
)
from service import notes as notes_service
from states import UpdateNoteState, RenameNoteState, DeleteNoteState

router = Router(name=__name__)


# one note callbacks
@router.callback_query(NoteInlineCallbackData.filter(F.action == NoteInlineActions.update))
async def note_update_callback(
    callback: CallbackQuery, callback_data: NoteInlineCallbackData, state: FSMContext
):
    await callback.message.answer(
        f"Изменение заметки - {hbold(callback_data.note_name.capitalize())}:"
    )
    await state.update_data(note_id=callback_data.note_id)
    await state.set_state(UpdateNoteState.text)


@router.callback_query(NoteInlineCallbackData.filter(F.action == NoteInlineActions.rename))
async def note_rename_callback(
    callback: CallbackQuery, callback_data: NoteInlineCallbackData, state: FSMContext
):
    await callback.message.answer(
        f"Изменение названия заметки - {hbold(callback_data.note_name.capitalize())}:"
    )
    await state.update_data(note_id=callback_data.note_id)
    await state.set_state(RenameNoteState.new_name)


@router.callback_query(NoteInlineCallbackData.filter(F.action == NoteInlineActions.delete))
async def note_rename_callback(
    callback: CallbackQuery, callback_data: NoteInlineCallbackData, state: FSMContext
):
    await callback.message.answer(
        f"Удалить заметку - {hbold(callback_data.note_name)}?:\n" + hitalic("Y/Д - Да, N/Н - Нет"),
        reply_markup=get_delete_note_inline_kb(
            note_id=callback_data.note_id, note_name=callback_data.note_name
        ),
    )
    await state.update_data(note_id=callback_data.note_id)
    await state.set_state(DeleteNoteState.confirmation)


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
    note = await repository.get_by_id(callback_data.note_id, user_id=callback.message.from_user.id)
    if note is None:
        await callback.message.answer(
            f"Заметка '{hbold(callback_data.note_name.capitalize())}' уже удалена"
        )
    else:
        await repository.delete_note(note)
        await callback.message.answer(
            f"Заметка '{hbold(callback_data.note_name.capitalize())}' успешно удалена!"
        )
    await callback.answer()
    await state.clear()


@router.callback_query(DeleteNoteCallbackData.filter(F.action == DeleteNoteInlineActions.no))
async def delete_note_confirmed_callback(
    callback: CallbackQuery, callback_data: DeleteNoteCallbackData, state: FSMContext
):
    await callback.message.answer(
        f"Удаление заметки '{hbold(callback_data.note_name.capitalize())}' отменено"
    )
    await callback.answer()
    await state.clear()
