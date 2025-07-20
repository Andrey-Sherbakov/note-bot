import enum

from aiogram.types import ReplyKeyboardMarkup

from keyboards.reply.base import get_reply_kb


# admin
class AdminActions(enum.StrEnum):
    note_bot = "Note-Bot"
    pomodoro = "Pomodoro"
    notification_service = "Notification-Service"


class AdminCommands(enum.StrEnum):
    note_bot = "/note_bot"
    pomodoro = "/pomodoro"
    notification_service = "/notification_service"


def get_admin_kb() -> ReplyKeyboardMarkup:
    return get_reply_kb(AdminActions, adjust=2)


# Note Bot
class NoteBotActions(enum.StrEnum):
    restart = "Перезапуск-Note-Bot"
    up = "Запуск-Note-Bot"
    down = "Выключение-Note-Bot"


def get_note_bot_kb() -> ReplyKeyboardMarkup:
    return get_reply_kb(NoteBotActions, adjust=1)


# Notification Service
class NotificationServiceActions(enum.StrEnum):
    restart = "Перезапуск-Notification-Service"
    up = "Запуск-Notification-Service"
    down = "Выключение-Notification-Service"


def get_notification_service_kb() -> ReplyKeyboardMarkup:
    return get_reply_kb(NotificationServiceActions, adjust=1)
