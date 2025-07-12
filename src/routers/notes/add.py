from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import NotesButtons
from service import notes as notes_service
from states import AddNoteState

router = Router(name=__name__)


@router.message(F.text == NotesButtons.add)
@router.message(Command("add"))
async def add_note(message: Message, state: FSMContext) -> None:
    args = message.text.strip().split(" ")
    if args[0].startswith("/") and len(args) == 2:
        await notes_service.start_add_note(name=args[1], message=message, state=state)
    else:
        await message.answer("Название заметки:")
        await state.set_state(AddNoteState.name)


@router.message(AddNoteState.name)
async def add_note_state_name(message: Message, state: FSMContext) -> None:
    await notes_service.start_add_note(name=message.text, message=message, state=state)


@router.message(AddNoteState.text)
async def add_note_state_text(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, введите текст заметки:")
    await notes_service.end_add_note(message=message, state=state)
