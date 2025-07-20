from aiogram import Router
from aiogram.types import Message

from keyboards.reply import AdminActions, AdminCommands, NoteBotActions, get_note_bot_kb
from service import CommandsFilter

router = Router(name=__name__)


@router.message(CommandsFilter(AdminCommands.note_bot, AdminActions.note_bot, admin=True))
async def handle_note_bot(message: Message) -> None:
    await message.answer("Администрирование Note-Bot", reply_markup=get_note_bot_kb())


@router.message(CommandsFilter(NoteBotActions.restart, admin=True))
async def handle_restart(message: Message) -> None:
    await message.answer("Перезапускаю контейнеры для Note-Bot")

    with open("/tmp/bot_pipe", "w") as pipe:
        pipe.write("make -C /root/note-bot restart\n")


@router.message(CommandsFilter(NoteBotActions.down, admin=True))
async def handle_down(message: Message) -> None:
    await message.answer("Выключаю контейнеры для Note-Bot")

    with open("/tmp/bot_pipe", "w") as pipe:
        pipe.write("make -C /root/note-bot down\n")


@router.message(CommandsFilter(NoteBotActions.up, admin=True))
async def handle_up(message: Message) -> None:
    await message.answer("Запускаю контейнеры для Note-Bot")

    with open("/tmp/bot_pipe", "w") as pipe:
        pipe.write("make -C /root/note-bot up\n")