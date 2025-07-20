from aiogram import Router
from aiogram.types import Message

from keyboards.reply import (
    AdminCommands,
    AdminActions,
    NotificationServiceActions,
    get_notification_service_kb,
)
from service import CommandsFilter

router = Router(name=__name__)


@router.message(
    CommandsFilter(
        AdminCommands.notification_service, AdminActions.notification_service, admin=True
    )
)
async def handle_note_bot(message: Message) -> None:
    await message.answer(
        "Администрирование Notification-Service", reply_markup=get_notification_service_kb()
    )


@router.message(CommandsFilter(NotificationServiceActions.restart, admin=True))
async def handle_restart(message: Message) -> None:
    await message.answer("Перезапускаю контейнеры для Notification-Service")

    with open("/tmp/bot_pipe", "w") as pipe:
        pipe.write("make -C /root/mail-service restart\n")


@router.message(CommandsFilter(NotificationServiceActions.down, admin=True))
async def handle_down(message: Message) -> None:
    await message.answer("Выключаю контейнеры для Notification-Service")

    with open("/tmp/bot_pipe", "w") as pipe:
        pipe.write("make -C /root/mail-service down\n")


@router.message(CommandsFilter(NotificationServiceActions.up, admin=True))
async def handle_up(message: Message) -> None:
    await message.answer("Запускаю контейнеры для Notification-Service")

    with open("/tmp/bot_pipe", "w") as pipe:
        pipe.write("make -C /root/mail-service up\n")