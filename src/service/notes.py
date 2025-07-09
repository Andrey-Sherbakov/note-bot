from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from db import repository
from keyboards.inline import get_note_inline_kb
from states import UpdateNoteState


# get note
async def start_get_note(name: str, message: Message, state: FSMContext) -> None:
    name = name.strip().lower()
    note = await repository.get_by_name(name=name)
    if note:
        await message.answer(
            f"{hbold(note.name.capitalize())}: {note.text}",
            reply_markup=get_note_inline_kb(note.id, note.name),
        )
    else:
        await message.answer("Заметки с таким именем не существует.")

    await state.clear()


# update note
async def start_note_update(name: str, message: Message, state: FSMContext) -> None:
    name = name.strip().lower()
    note = await repository.get_by_name(name=name)

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
    note = await repository.get_by_id(note_id=note_id)
    note.text = message.text.strip()

    await repository.update_note(note)
    await message.answer("Заметка успешно обновлена!")
    await state.clear()