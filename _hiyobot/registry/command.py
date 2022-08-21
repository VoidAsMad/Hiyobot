from typing import Any, Callable, Optional

from discord.types.command import (
    ApplicationCommandOptionType,
    ApplicationCommandType,
)
from hiyobot.handler.types import CORO


class RegisterdInfo:
    def __init__(self, name: str) -> None:
        self.name = name
        self.single_command: dict[str, CORO] = {}
        self.sub_command: dict[str, CORO] = {}

    def add_command(self, func: CORO):
        self.single_command[self.name] = func

    def add_sub_command(self, name: str, func: CORO):
        self.sub_command[name] = func

    def __eq__(self, __o: object) -> bool:
        return __o == self.name


class CommandArgument:
    def __init__(
        self,
        *,
        name: str,
        description: str,
        value: Optional[Any] = None,
        type: ApplicationCommandOptionType = 1,
        required: Optional[bool] = None,
    ) -> None:
        self.name = name
        self.value = value
        self.description = description
        self.type: ApplicationCommandOptionType = type
        self.required = required
        self.options: list["CommandArgument"] = []

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "type": self.type,
        }

        if isinstance(self.required, bool):
            d["required"] = self.required

        if self.options:
            d["options"] = [ca.to_dict() for ca in self.options]

        if self.value:
            d["value"] = self.value

        return d


class RegisterCommand:
    def __init__(
        self,
        *,
        name: str,
        description: str,
        type: ApplicationCommandType = 1,
    ) -> None:
        self._is_sub_command_group = False
        self.name = name
        self.description = description
        self.type = type
        self.registerd_sub_command_groups: list["RegisterCommand"] = []
        self.registerd_sub_commands: list[CommandArgument] = []
        self.command_options: list[CommandArgument] = []

        self.registerd_info = RegisterdInfo(self.name)

    def to_dict(self) -> dict[str, Any]:
        base: dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "options": [],
        }

        if options := self.command_options:
            for option in options:
                base["options"].append(option.to_dict())

        if sub_command_groups := self.registerd_sub_command_groups:
            for sub_command_group in sub_command_groups:
                base["options"].append(sub_command_group.to_dict())

        if sub_commands := self.registerd_sub_commands:
            for sub_command in sub_commands:
                base["options"].append(sub_command.to_dict())

        return base

    def command(
        self, options: Optional[list[CommandArgument]] = None
    ) -> Callable[[CORO], None]:
        def decorator(f: CORO) -> None:
            if options:
                self.command_options.extend(options)
            self.registerd_info.add_command(f)

        return decorator

    def sub_command(
        self,
        *,
        name: str,
        description: str,
        options: Optional[list[CommandArgument]] = None,
    ) -> Callable[[CORO], None]:
        def decorator(f: CORO) -> None:
            sub_command = CommandArgument(name=name, description=description, type=1)
            if options:
                sub_command.options.extend(options)
            self.registerd_sub_commands.append(sub_command)
            self.registerd_info.add_sub_command(name, f)

        return decorator

    def sub_command_group(self, *, name: str, description: str) -> "RegisterCommand":
        if self._is_sub_command_group:
            raise RuntimeError("Invaild")
        ins = self.__class__(name=name, description=description, type=2)
        self.registerd_sub_command_groups.append(ins)
        ins._is_sub_command_group = True
        return ins
