from aiogram.fsm.state import StatesGroup, State


class PomodoroMake(StatesGroup):
    cmd = State()