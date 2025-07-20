import enum

from aiogram.types import ReplyKeyboardMarkup

from keyboards.reply.base import get_reply_kb, BaseButtons


# admin
class AdminActions(enum.StrEnum):
    note_bot = "Note-Bot"
    pomodoro = "Pomodoro"
    notification_service = "Notification-Service"
    admin = BaseButtons.admin
    logs = "Pipe-Логи"
    stop = BaseButtons.stop


class AdminCommands(enum.StrEnum):
    note_bot = "/note_bot"
    pomodoro = "/pomodoro"
    notification_service = "/notification_service"
    logs = "/logs"


def get_admin_kb() -> ReplyKeyboardMarkup:
    return get_reply_kb(AdminActions, adjust=(1, 1, 1, 3))


# Note Bot
class NoteBotActions(enum.StrEnum):
    restart = "Перезапуск-Note-Bot"
    up = "Запуск-Note-Bot"
    down = "Выключение-Note-Bot"
    admin = BaseButtons.admin
    stop = BaseButtons.stop


def get_note_bot_kb() -> ReplyKeyboardMarkup:
    return get_reply_kb(NoteBotActions, adjust=(1, 1, 1, 2))


# Notification Service
class NotificationServiceActions(enum.StrEnum):
    restart = "Перезапуск-Notification-Service"
    up = "Запуск-Notification-Service"
    down = "Выключение-Notification-Service"
    admin = BaseButtons.admin
    stop = BaseButtons.stop


def get_notification_service_kb() -> ReplyKeyboardMarkup:
    return get_reply_kb(NotificationServiceActions, adjust=(1, 1, 1, 2))


# Pomodoro
class PomodoroActions(enum.StrEnum):
    make = "Make-Pomodoro"
    admin = BaseButtons.admin
    stop = BaseButtons.stop


def get_pomodoro_kb() -> ReplyKeyboardMarkup:
    return get_reply_kb(PomodoroActions, adjust=(1,2))