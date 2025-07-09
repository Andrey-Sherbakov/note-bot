from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.markdown import hitalic, hbold

from db import repository
from db.schemas import BaseNote
from keyboards.reply import NotesButtons, StartButtons, get_notes_kb
from service import notes as notes_service
from states import AddNoteState, GetNoteState, UpdateNoteState, DeleteNoteState

router = Router(name=__name__)


@router.message(F.text == StartButtons.notes)
@router.message(Command("notes"))
async def handle_notes(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Модуль работы с заметками.\n\n"
        + hitalic(
            "Доступные действия:",
            " 1. Все заметки - /getall",
            " 2. Одна заметка - /get",
            " 3. Создать заметку - /add",
            " 4. Изменить заметку - /update",
            " 5. Удалить заметку - /delete",
            sep="\n",
        ),
        reply_markup=get_notes_kb(),
    )
    await state.clear()


# get all notes
@router.message(F.text == NotesButtons.all)
@router.message(Command("getall"))
async def get_all_notes(message: Message) -> None:
    async with ChatActionSender.typing(chat_id=message.chat.id, bot=message.bot):
        all_notes = await repository.get_all_notes()
        text = "\n\n".join(f"<b>{note.name}</b>: {note.text}" for note in all_notes)
        await message.answer(text)


# get one note
@router.message(F.text == NotesButtons.one)
@router.message(Command("get"))
async def get_note(message: Message, state: FSMContext) -> None:
    args = message.text.strip().split(" ")
    if args[0].startswith("/") and len(args) == 2:
        await notes_service.start_get_note(name=args[1], message=message, state=state)
    else:
        await message.answer("Название заметки:")
        await state.set_state(GetNoteState.name)


@router.message(GetNoteState.name)
async def get_note_state_name(message: Message, state: FSMContext) -> None:
    await notes_service.start_get_note(name=message.text, message=message, state=state)


# add note
@router.message(F.text == NotesButtons.add)
@router.message(Command("add"))
async def handle_add(message: Message, state: FSMContext) -> None:
    await message.answer("Enter new note name:")
    await state.set_state(AddNoteState.name)


@router.message(AddNoteState.name)
async def name_entered(message: Message, state: FSMContext) -> None:
    await state.update_data(note_name=message.text.strip().lower())
    await message.answer("Enter new note text:")
    await state.set_state(AddNoteState.text)


@router.message(AddNoteState.text)
async def text_entered(message: Message, state: FSMContext) -> None:
    try:
        new_note = BaseNote(
            name=(await state.get_data()).get("note_name"),
            text=message.text.strip(),
        )
        await repository.create_note(new_note=new_note)
        await message.answer("Note added!")
        await state.clear()
    except Exception as e:
        await message.answer(f"Something went wrong: {e}", parse_mode=None)


# update note
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


# delete note
@router.message(F.text == NotesButtons.delete)
@router.message(Command("delete"))
async def delete_note(message: Message, state: FSMContext) -> None:
    await message.answer("Enter note name:")
    await state.set_state(DeleteNoteState.name)


@router.message(DeleteNoteState.name)
async def delete_note_state_name(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Please enter name:")
        return

    name = message.text.strip().lower()
    note = await repository.get_by_name(name=name)
    if note:
        await state.update_data(note=note)
        await message.answer(
            f"Delete note: {hbold(note.name)}?\n" + hitalic("Y/Д - Yes/Да, N/Н - No/Нет")
        )
        await state.set_state(DeleteNoteState.confirmation)
    else:
        await message.answer("Note with that name does not exist.")
        await state.clear()


@router.message(DeleteNoteState.confirmation)
async def delete_note_state_confirmation(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Please enter valid symbol:" + hitalic("Y/Д - Yes/Да, N/Н - No/Нет"))
        return

    confirmation_map = {"yes": ["y", "д"], "no": ["n", "н"]}
    text = message.text.strip().lower()

    if text in confirmation_map["yes"]:
        data = await state.get_data()

        await repository.delete_note(note=data["note"])
        await message.answer("Note deleted!")
        await state.clear()

    elif text in confirmation_map["no"]:
        await message.answer("Note delete cancelled.")
        await state.clear()

    else:
        await message.answer("Please enter valid symbol:" + hitalic("Y/Д - Yes/Да, N/Н - No/Нет"))


# default handler
@router.message()
async def default_message(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer(hitalic('Доступные действия: /help'))

    await notes_service.start_get_note(name=message.text, message=message, state=state)