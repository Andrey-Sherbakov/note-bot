from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.core.filters import CommandsFilter
from src.notes import service
from src.notes.keyboards.reply import NotesButtons
from src.notes.states import RenameNoteState

router = Router(name=__name__)


# initial command
@router.message(CommandsFilter("/rename", NotesButtons.rename, require_arg=True))
async def rename_note_with_name(message: Message, state: FSMContext, arg: str) -> None:
    await service.rename_note_state_name(name=arg, message=message, state=state)


@router.message(CommandsFilter("/rename", NotesButtons.rename))
async def rename_note(message: Message, state: FSMContext) -> None:
    await message.answer("Введите название:")
    await state.set_state(RenameNoteState.name)


# state name
@router.message(RenameNoteState.name, F.text)
async def rename_note_state_name(message: Message, state: FSMContext) -> None:
    await service.rename_note_state_name(name=message.text, message=message, state=state)


@router.message(RenameNoteState.name)
async def rename_note_state_name_fail(message: Message) -> None:
    await message.answer("Пожалуйста, введите название заметки:")


# state new name
@router.message(RenameNoteState.new_name, F.text)
async def rename_note_state_new_name(message: Message, state: FSMContext) -> None:
    await service.rename_note_state_new_name(new_name=message.text, message=message, state=state)


@router.message(RenameNoteState.new_name)
async def rename_note_state_new_name_fail(message: Message) -> None:
    await message.answer("Пожалуйста, введите новое название заметки:")

