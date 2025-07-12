from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import NotesButtons
from service import notes as notes_service
from states import GetNoteState

router = Router(name=__name__)


@router.message(F.text == NotesButtons.one)
@router.message(Command("get"))
async def get_note(message: Message, state: FSMContext) -> None:
    args = message.text.strip().split(" ")
    if args[0].startswith("/") and len(args) == 2:
        await notes_service.start_get_note(
            name=args[1], user_id=message.from_user.id, message=message, state=state
        )
    else:
        await message.answer("Название заметки:")
        await state.set_state(GetNoteState.name)


@router.message(GetNoteState.name)
async def get_note_state_name(message: Message, state: FSMContext) -> None:
    await notes_service.start_get_note(
        name=message.text, user_id=message.from_user.id, message=message, state=state
    )
