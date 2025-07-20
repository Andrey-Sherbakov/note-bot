from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hcode

from keyboards.reply import AdminCommands, AdminActions, get_pomodoro_kb, PomodoroActions
from service import CommandsFilter
from states import PomodoroMake

router = Router(name=__name__)


@router.message(CommandsFilter(AdminCommands.pomodoro, AdminActions.pomodoro, admin=True))
async def handle_pomodoro(message: Message) -> None:
    await message.answer("Администрирование Pomodoro", reply_markup=get_pomodoro_kb())


@router.message(CommandsFilter(PomodoroActions.make, admin=True))
async def handle_make(message: Message, state: FSMContext) -> None:
    await message.answer("Введите Make команду:")
    await state.set_state(PomodoroMake.cmd)


@router.message(PomodoroMake.cmd, F.text)
async def handle_make_state_cmd(message: Message, state: FSMContext) -> None:
    cmd = message.text.strip().lower()
    await message.answer(f"Выполняю команду для Pomodoro: {hcode(f'make {cmd}')}")

    with open("/tmp/bot_pipe", "w") as pipe:
        pipe.write(f"make -C /root/pomodoro-time {cmd}\n")

    await state.clear()


@router.message(PomodoroMake.cmd)
async def handle_make_state_cmd_fail(message: Message) -> None:
    await message.answer("Пожалуйста, введите Make команду для pomodoro")