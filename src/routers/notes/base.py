from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.markdown import hitalic

from keyboards.inline import get_notes_pagination_kb
from keyboards.reply import NotesButtons, StartButtons, get_notes_kb
from service import notes_service, CommandsFilter

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
@router.message(CommandsFilter(["/all", NotesButtons.all]))
async def get_all_notes(message: Message, state: FSMContext) -> None:
    await state.clear()

    async with ChatActionSender.typing(chat_id=message.chat.id, bot=message.bot):
        # all_notes = await repository.get_all_notes(user_id=message.from_user.id)
        # if not all_notes:
        #     await message.answer("Заметок пока нет.")
        #     return

        user_id = message.from_user.id
        page = 1

        notes, total_pages = await notes_service.get_notes_paginated(user_id, page)
        if not notes:
            await message.answer("Заметок пока нет.")
            return

        text = "\n\n".join(f"<b>{note.name.capitalize()}</b>:\n{note.text}" for note in notes)
        if page < total_pages:
            text += "\n\n..."

        kb = get_notes_pagination_kb(notes=notes, page=page, total_pages=total_pages)
        await message.answer(text, reply_markup=kb)


# default handler
@router.message()
async def default_message(message: Message, state: FSMContext) -> None:
    print("Standard handler")
    if not message.text:
        await message.answer(hitalic("Доступные действия: /help"))

    await notes_service.get_note_state_name(
        name=message.text, user_id=message.from_user.id, message=message, state=state
    )
