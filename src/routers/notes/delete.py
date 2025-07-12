from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hitalic

from keyboards.inline import get_delete_note_inline_kb
from keyboards.reply import NotesButtons
from service import notes as notes_service
from states import DeleteNoteState

router = Router(name=__name__)


@router.message(F.text == NotesButtons.delete)
@router.message(Command("delete"))
async def delete_note(message: Message, state: FSMContext) -> None:
    args = message.text.strip().split(" ")
    if args[0].startswith("/") and len(args) == 2:
        await notes_service.start_delete_note(name=args[1], message=message, state=state)
    else:
        await message.answer("Название заметки:")
        await state.set_state(DeleteNoteState.name)


@router.message(DeleteNoteState.name)
async def delete_note_state_name(message: Message, state: FSMContext) -> None:
    name = message.text
    if not name:
        await message.answer("Пожалуйста, введите название заметки:")
        return

    await notes_service.start_delete_note(name=name, message=message, state=state)


@router.message(DeleteNoteState.confirmation)
async def delete_note_state_confirmation(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if not message.text:
        await message.answer(
            "Пожалуйста, введите правильный символ:\n" + hitalic("Y/Д - Да, N/Н - Нет"),
            reply_markup=get_delete_note_inline_kb(data["note_id"]),
        )
        return

    await notes_service.end_note_delete(message=message, state=state)
