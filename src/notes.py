from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from src.db import repository
from src.db.schemas import BaseNote

router = Router()


# get all notes
@router.message(Command("getall"))
async def get_all_notes(message: Message) -> None:
    all_notes = await repository.get_all_notes()
    text = "\n\n".join(f"<b>{note.name}</b>: {note.text}" for note in all_notes)
    await message.answer(text)


# get one note
class GetNoteQuery(StatesGroup):
    waiting_name = State()


@router.message(Command("get"))
async def get_note(message: Message, state: FSMContext) -> None:
    await message.answer("Enter note name:")
    await state.set_state(GetNoteQuery.waiting_name)


@router.message(GetNoteQuery.waiting_name)
async def get_note_w_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip().lower()
    note = await repository.get_one(name=name)
    if note:
        await message.answer(note.text)
    else:
        await message.answer("Note with that name does not exist.")
    await state.clear()


# add note
class AddNoteQuery(StatesGroup):
    waiting_name = State()
    waiting_text = State()


@router.message(Command("add"))
async def handle_add(message: Message, state: FSMContext) -> None:
    await message.answer("Enter new note name:")
    await state.set_state(AddNoteQuery.waiting_name)


@router.message(AddNoteQuery.waiting_name)
async def name_entered(message: Message, state: FSMContext) -> None:
    await state.update_data(note_name=message.text.strip().lower())
    await message.answer("Enter new note text:")
    await state.set_state(AddNoteQuery.waiting_text)


@router.message(AddNoteQuery.waiting_text)
async def text_entered(message: Message, state: FSMContext) -> None:
    try:
        new_note = BaseNote(
            name=(await state.get_data()).get("note_name"),
            text=message.text.strip(),
        )
        await repository.create_note(new_note=new_note)
        await message.answer("Note added!")
    except Exception as e:
        await message.answer(f"Something went wrong: {e}", parse_mode=None)
