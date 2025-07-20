from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import settings


class CommandsFilter(BaseFilter):
    def __init__(self, *commands: str, require_arg: bool = False, admin: bool = False):
        self.commands = [cmd.lower() for cmd in commands]
        self.require_arg = require_arg
        self.admin = admin

    async def __call__(self, message: Message) -> bool | dict[str, str]:
        if self.admin and message.from_user.id != settings.ADMIN:
            return False

        text = message.text
        if not text:
            return False

        parts = text.strip().lower().split(maxsplit=1)
        command = parts[0]
        arg = parts[1] if len(parts) > 1 else None

        if command not in self.commands:
            return False

        if self.require_arg:
            if not arg:
                return False
            return {"arg": arg}

        return True