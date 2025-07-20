from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import NotesButtons
from service import notes as notes_service, CommandsFilter
from states import AddNoteState

router = Router(name=__name__)


# initial command
@router.message(CommandsFilter("/add", NotesButtons.add, require_arg=True))
async def add_note_with_name(message: Message, state: FSMContext, arg: str) -> None:
    await notes_service.add_note_state_name(
        name=arg, user_id=message.from_user.id, message=message, state=state
    )


@router.message(CommandsFilter("/add", NotesButtons.add))
async def add_note(message: Message, state: FSMContext) -> None:
    await message.answer("Название заметки:")
    await state.set_state(AddNoteState.name)


# state name
@router.message(AddNoteState.name, F.text)
async def add_note_state_name(message: Message, state: FSMContext) -> None:
    await notes_service.add_note_state_name(
        name=message.text,
        user_id=message.from_user.id,
        message=message,
        state=state,
    )


@router.message(AddNoteState.name)
async def add_note_state_name_fail(message: Message) -> None:
    await message.answer("Пожалуйста, введите название заметки:")


# state text
@router.message(AddNoteState.text, F.text)
async def add_note_state_text(message: Message, state: FSMContext) -> None:
    await notes_service.add_note_state_text(message=message, state=state)


@router.message(AddNoteState.text)
async def add_note_state_text_fail(message: Message) -> None:
    await message.answer("Пожалуйста, введите текст заметки:")
