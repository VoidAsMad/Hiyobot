from os import urandom
from typing import Any, Optional
from discord import ButtonStyle

from _hiyobot.types import Handler


class Button:
    def __init__(
        self,
        func: Handler,
        label: str,
        emoji: str,
        style: ButtonStyle = ButtonStyle.secondary,
        custom_id: Optional[str] = None,
    ):
        self.func = func
        self.label = label
        self.emoji = emoji
        self.style = style
        self.custom_id = custom_id or self._rhex()

    @classmethod
    def apply(
        cls,
        *,
        label: str,
        emoji: str,
        style: ButtonStyle = ButtonStyle.secondary,
        custom_id: Optional[str] = None,
    ):
        def inner(func: Handler):
            return cls(func, label, emoji, style, custom_id)

        return inner

    def _rhex(self):
        return urandom(16).hex()

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": 2,
            "label": self.label,
            "emoji": {"id": None, "name": self.emoji},
            "style": self.style.value,
            "custom_id": self.custom_id,
        }
