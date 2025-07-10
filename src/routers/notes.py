from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.markdown import hitalic

from db import repository
from db.schemas import BaseNote
from keyboards.inline import get_all_notes_inline_kb
from keyboards.reply import NotesButtons, StartButtons, get_notes_kb
from service import notes as notes_service
from states import AddNoteState, GetNoteState, UpdateNoteState, DeleteNoteState, RenameNoteState

router = Router(name=__name__)


@router.message(F.text == StartButtons.notes)
@router.message(Command("notes"))
async def handle_notes(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Модуль работы с заметками.\n\n"
        + hitalic(
            "Доступные действия:",
            " 1. Все заметки - /all",
            " 2. Одна заметка - /get",
            " 3. Создать заметку - /add",
            " 5. Переименовать заметку - /rename",
            " 4. Изменить заметку - /update",
            " 5. Удалить заметку - /delete",
            sep="\n",
        ),
        reply_markup=get_notes_kb(),
    )
    await state.clear()


# get all notes
@router.message(F.text == NotesButtons.all)
@router.message(Command("all"))
async def get_all_notes(message: Message) -> None:
    async with ChatActionSender.typing(chat_id=message.chat.id, bot=message.bot):
        all_notes = await repository.get_all_notes(user_id=message.from_user.id)
        if not all_notes:
            await message.answer("Заметок пока нет.")
            return

        text = "\n\n".join(f"<b>{note.name}</b>: {note.text}" for note in all_notes)
        await message.answer(text, reply_markup=get_all_notes_inline_kb(all_notes))


# get one note
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
            user_id=message.from_user.id,
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


# rename note
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


# delete note
@router.message(F.text == NotesButtons.delete)
@router.message(Command("delete"))
async def delete_note(message: Message, state: FSMContext) -> None:
    args = message.text.strip().split(" ")
    if args[0].startswith("/") and len(args) == 2:
        await notes_service.start_delete_note(name=args[1], message=message, state=state)
    else:
        await message.answer("Enter note name:")
        await state.set_state(DeleteNoteState.name)


@router.message(DeleteNoteState.name)
async def delete_note_state_name(message: Message, state: FSMContext) -> None:
    name = message.text
    if not name:
        await message.answer("Please enter name:")
        return

    await notes_service.start_delete_note(name=name, message=message, state=state)


@router.message(DeleteNoteState.confirmation)
async def delete_note_state_confirmation(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Please enter valid symbol:\n" + hitalic("Y/Д - Yes/Да, N/Н - No/Нет"))
        return

    await notes_service.end_note_delete(message=message, state=state)


# default handler
@router.message()
async def default_message(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer(hitalic("Доступные действия: /help"))

    await notes_service.start_get_note(
        name=message.text, user_id=message.from_user.id, message=message, state=state
    )
