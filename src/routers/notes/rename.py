from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import NotesButtons
from service import notes as notes_service
from states import RenameNoteState

router = Router(name=__name__)


@router.message(F.text == NotesButtons.rename)
@router.message(Command("rename"))
async def rename_note(message: Message, state: FSMContext) -> None:
    args = message.text.strip().split(" ")
    if args[0].startswith("/") and len(args) == 2:
        await notes_service.start_rename_note(name=args[1], message=message, state=state)
    else:
        await message.answer("Введите название:")
        await state.set_state(RenameNoteState.name)


@router.message(RenameNoteState.name)
async def rename_note_state_name(message: Message, state: FSMContext) -> None:
    name = message.text
    if not name:
        await message.answer("Введите название:")

    await notes_service.start_rename_note(name=name, message=message, state=state)


@router.message(RenameNoteState.new_name)
async def rename_note_state_new_name(message: Message, state: FSMContext) -> None:
    new_name = message.text
    if not new_name:
        await message.answer("Введите новое название:")

    await notes_service.end_note_rename(new_name=new_name, message=message, state=state)
