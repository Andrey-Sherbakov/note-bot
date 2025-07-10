from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic

from db import repository
from keyboards.inline import get_note_inline_kb, get_delete_note_inline_kb
from states import UpdateNoteState, RenameNoteState, DeleteNoteState


# get note
async def start_get_note(name: str, user_id: int, message: Message, state: FSMContext) -> None:
    name = name.strip().lower()
    note = await repository.get_by_name(name=name, user_id=user_id)
    if note:
        await message.answer(f"{hbold(note.name.capitalize())}:")
        await message.answer(
            note.text,
            reply_markup=get_note_inline_kb(note.id, note.name),
        )
    else:
        await message.answer("Заметки с таким именем не существует.")

    await state.clear()


# update note
async def start_note_update(name: str, message: Message, state: FSMContext) -> None:
    name = name.strip().lower()
    note = await repository.get_by_name(name=name, user_id=message.from_user.id)

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
    name = name.strip().lower()
    note = await repository.get_by_name(name=name, user_id=message.from_user.id)

    if note:
        await message.answer(f"Изменение названия заметки - {hbold(note.name.capitalize())}:")
        await state.update_data(note_id=note.id)
        await state.set_state(RenameNoteState.new_name)
    else:
        await message.answer("Заметки с таким именем не существует.")
        await state.clear()


async def end_note_rename(new_name: str, message: Message, state: FSMContext) -> None:
    new_name = new_name.strip().lower()
    note = await repository.get_by_name(name=new_name, user_id=message.from_user.id)
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
    name = name.strip().lower()
    note = await repository.get_by_name(name=name, user_id=message.from_user.id)
    if note:
        await state.update_data(note_id=note.id)
        await message.answer(
            f"Удалить заметку - {hbold(note.name)}?:\n" + hitalic("Y/Д - Да, N/Н - Нет"),
            reply_markup=get_delete_note_inline_kb(note_id=note.id, note_name=note.name),
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
