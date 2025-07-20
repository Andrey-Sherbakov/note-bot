from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hitalic

from keyboards.inline import get_delete_note_inline_kb
from keyboards.reply import NotesButtons
from service import notes_service, CommandsFilter
from states import DeleteNoteState

router = Router(name=__name__)


# initial command
@router.message(CommandsFilter("/delete", NotesButtons.delete, require_arg=True))
async def delete_note_with_name(message: Message, state: FSMContext, arg: str):
    await notes_service.delete_note_state_name(name=arg, message=message, state=state)


@router.message(CommandsFilter("/delete", NotesButtons.delete))
async def delete_note(message: Message, state: FSMContext) -> None:
    await message.answer("Название заметки:")
    await state.set_state(DeleteNoteState.name)


# state name
@router.message(DeleteNoteState.name, F.text)
async def delete_note_state_name(message: Message, state: FSMContext) -> None:
    await notes_service.delete_note_state_name(name=message.text, message=message, state=state)


@router.message(DeleteNoteState.name)
async def delete_note_state_name_fail(message: Message) -> None:
    await message.answer("Пожалуйста, введите название заметки:")


# state confirmation
@router.message(DeleteNoteState.confirmation, F.text.casefold().in_({"y", "д"}))
async def delete_note_confirmation_yes(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    answer = await notes_service.delete_note_state_confirmed(
        note_id=data["note_id"], user_id=message.from_user.id
    )
    await message.answer(answer)
    await state.clear()


@router.message(DeleteNoteState.confirmation, F.text.casefold().in_({"n", "н"}))
async def delete_note_confirmation_no(message: Message, state: FSMContext) -> None:
    await message.answer("Удаление заметки отменено")
    await state.clear()


@router.message(DeleteNoteState.confirmation)
async def delete_note_state_confirmation(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await message.answer(
        "Пожалуйста, введите правильный символ:\n" + hitalic("Y/Д - Да, N/Н - Нет"),
        reply_markup=get_delete_note_inline_kb(data["note_id"]),
    )

