import html

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic

from db import repository
from db.models import Note
from db.schemas import BaseNote
from keyboards.inline import get_note_inline_kb, get_delete_note_inline_kb
from states import UpdateNoteState, RenameNoteState, DeleteNoteState, AddNoteState


async def validate_name(name: str, user_id: int) -> Note | None:
    name = name.strip().lower()
    note = await repository.get_by_name(name=name, user_id=user_id)
    return note


# get note
async def start_get_note(name: str, user_id: int, message: Message, state: FSMContext) -> None:
    note = await validate_name(name, user_id)

    if note:
        await message.answer(f"{hbold(note.name.capitalize())}:")
        await message.answer(
            note.text,
            reply_markup=get_note_inline_kb(note.id),
        )
    else:
        await message.answer("Заметки с таким именем не существует.")

    await state.clear()


# add note
async def start_add_note(name: str, message: Message, state: FSMContext) -> None:
    note = await validate_name(name, message.from_user.id)

    if note:
        await message.answer("Заметка с таким названием уже существует.\nВведите другое:")
        return

    await state.update_data(note_name=name.strip().lower())
    await message.answer("Текст заметки:")
    await state.set_state(AddNoteState.text)


async def end_add_note(message: Message, state: FSMContext) -> None:
    try:
        new_note = BaseNote(
            name=(await state.get_data()).get("note_name"),
            text=message.text.strip(),
            user_id=message.from_user.id,
        )
        await repository.create_note(new_note=new_note)
        await message.answer("Заметка добавлена!")
        await state.clear()
    except Exception as e:
        await message.answer(f"Произошла ошибка: {html.escape(str(e), quote=False)}")


# update note
async def start_note_update(name: str, message: Message, state: FSMContext) -> None:
    note = await validate_name(name, message.from_user.id)

    if note:
        await message.answer(f"Изменение заметки - {hbold(note.name.capitalize())}:")
        await state.update_data(note_id=note.id)
        await state.set_state(UpdateNoteState.text)
    else:
        await message.answer("Заметки с таким именем не существует.")
        await state.clear()


async def end_note_update(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    note_id = data["note_id"]
    note = await repository.get_by_id(note_id=note_id, user_id=message.from_user.id)
    note.text = message.text.strip()

    await repository.update_note(note)
    await message.answer("Заметка успешно обновлена!")
    await state.clear()


# rename note
async def start_rename_note(name: str, message: Message, state: FSMContext) -> None:
    note = await validate_name(name, message.from_user.id)

    if note:
        await message.answer(f"Изменение названия заметки - {hbold(note.name.capitalize())}:")
        await state.update_data(note_id=note.id)
        await state.set_state(RenameNoteState.new_name)
    else:
        await message.answer("Заметки с таким именем не существует.")
        await state.clear()


async def end_note_rename(new_name: str, message: Message, state: FSMContext) -> None:
    note = await validate_name(new_name, message.from_user.id)

    if note:
        await message.answer(
            f"Такое название уже существует.\n{hitalic('Введите другое название:')}"
        )
        return

    data = await state.get_data()
    note_id = data["note_id"]
    note = await repository.get_by_id(note_id=note_id, user_id=message.from_user.id)
    note.name = new_name

    await repository.update_note(note)
    await message.answer("Заметка успешно переименована!")
    await state.clear()


# delete note
async def start_delete_note(name: str, message: Message, state: FSMContext) -> None:
    note = await validate_name(name, message.from_user.id)

    if note:
        await state.update_data(note_id=note.id)
        await message.answer(
            f"Удалить заметку - {hbold(note.name)}?:\n" + hitalic("Y/Д - Да, N/Н - Нет"),
            reply_markup=get_delete_note_inline_kb(note_id=note.id),
        )
        await state.set_state(DeleteNoteState.confirmation)
    else:
        await message.answer("Заметки с таким именем не существует.")
        await state.clear()


async def end_note_delete(message: Message, state: FSMContext) -> None:
    confirmation_map = {"yes": ["y", "д"], "no": ["n", "н"]}
    text = message.text.strip().lower()

    if text in confirmation_map["yes"]:
        data = await state.get_data()

        note = await repository.get_by_id(note_id=data["note_id"], user_id=message.from_user.id)
        await repository.delete_note(note)
        await message.answer(f"Заметка '{hbold(note.name.capitalize())}' успешно удалена!")
        await state.clear()

    elif text in confirmation_map["no"]:
        await message.answer("Удаление заметки отменено")
        await state.clear()

    else:
        await message.answer(
            "Пожалуйста введите правильный символ:\n" + hitalic("Y/Д - Да, N/Н - Нет")
        )
