from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.core.filters import CommandsFilter
from src.notes import service
from src.notes.keyboards.reply import NotesButtons
from src.notes.states import UpdateNoteState

router = Router(name=__name__)


# initial command
@router.message(CommandsFilter("/update", NotesButtons.update, require_arg=True))
async def update_note_with_name(message: Message, state: FSMContext, arg: str) -> None:
    await service.update_note_state_name(name=arg, message=message, state=state)


@router.message(CommandsFilter("/update", NotesButtons.update))
async def update_note(message: Message, state: FSMContext) -> None:
    await message.answer("Название заметки:")
    await state.set_state(UpdateNoteState.name)


# state name
@router.message(UpdateNoteState.name, F.text)
async def update_note_state_name(message: Message, state: FSMContext) -> None:
    await service.update_note_state_name(name=message.text, message=message, state=state)


@router.message(UpdateNoteState.name)
async def update_note_state_name_fail(message: Message) -> None:
    await message.answer("Пожалуйста, введите название заметки:")


# state text
@router.message(UpdateNoteState.text, F.text)
async def update_note_state_text(message: Message, state: FSMContext) -> None:
    await service.update_note_state_text(message=message, state=state)


@router.message(UpdateNoteState.text)
async def update_note_state_text_fail(message: Message) -> None:
    await message.answer("Пожалуйста, введите обновленный текст:")

