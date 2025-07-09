from aiogram.fsm.state import StatesGroup, State


class GetNoteState(StatesGroup):
    name = State()


class AddNoteState(StatesGroup):
    name = State()
    text = State()


class UpdateNoteState(StatesGroup):
    name = State()
    text = State()


class DeleteNoteState(StatesGroup):
    name = State()
    confirmation = State()
