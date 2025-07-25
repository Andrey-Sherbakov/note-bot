from typing import Iterable

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.core.config import settings


class CommandsFilter(BaseFilter):
    def __init__(
        self,
        *commands: str,
        iterables: list[Iterable[str]] | None = None,
        require_arg: bool = False,
        admin: bool = False,
    ):
        self.commands = {cmd.lower() for cmd in commands}
        self.require_arg = require_arg
        self.admin = admin

        if iterables:
            for iterable in iterables:
                self.commands.update({cmd.lower() for cmd in iterable})

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