from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import NotesButtons
from service import notes as notes_service
from states import UpdateNoteState

router = Router(name=__name__)


@router.message(F.text == NotesButtons.update)
@router.message(Command("update"))
async def update_note(message: Message, state: FSMContext) -> None:
    args = message.text.strip().split(" ")
    print(args)
    if len(args) == 2:
        await notes_service.start_note_update(name=args[1], message=message, state=state)
    else:
        await message.answer("Название заметки:")
        await state.set_state(UpdateNoteState.name)


@router.message(UpdateNoteState.name)
async def update_note_state_name(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Введите название заметки:")
        return

    await notes_service.start_note_update(name=message.text, message=message, state=state)


@router.message(UpdateNoteState.text)
async def update_note_state_text(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Введите обновленный текст:")
        return

    await notes_service.end_note_update(message=message, state=state)
