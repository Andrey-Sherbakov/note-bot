from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.core.filters import CommandsFilter
from src.notes import service
from src.notes.keyboards.reply import NotesButtons
from src.notes.states import GetNoteState

router = Router(name=__name__)


# initial command
@router.message(CommandsFilter("/get", NotesButtons.get, require_arg=True))
async def get_note_with_name(message: Message, state: FSMContext, arg: str) -> None:
    await service.get_note_state_name(
        name=arg, user_id=message.from_user.id, message=message, state=state
    )


@router.message(CommandsFilter("/get", NotesButtons.get))
async def get_note(message: Message, state: FSMContext) -> None:
    await message.answer("Название заметки:")
    await state.set_state(GetNoteState.name)


# state name
@router.message(GetNoteState.name, F.text)
async def get_note_state_name(message: Message, state: FSMContext) -> None:
    await service.get_note_state_name(
        name=message.text, user_id=message.from_user.id, message=message, state=state
    )


@router.message(GetNoteState.name)
async def get_note_state_name_fail(message: Message) -> None:
    await message.answer("Пожалуйста, введите название заметки:")
