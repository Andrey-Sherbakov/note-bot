from aiogram.fsm.state import StatesGroup, State


class GetNoteQuery(StatesGroup):
    waiting_name = State()


class AddNoteQuery(StatesGroup):
    waiting_name = State()
    waiting_text = State()


class UpdateNoteQuery(StatesGroup):
    waiting_name = State()
    waiting_text = State()


class DeleteNoteQuery(StatesGroup):
    waiting_name = State()
    waiting_confirmation = State()
