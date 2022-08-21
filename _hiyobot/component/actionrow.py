from _hiyobot.component.button import Button
from discord import ComponentType


class ActionRow:
    def __init__(
        self, child: list[Button]
    ) -> None:
        self.child = child

    def to_dict(self):
        return {
            "type": ComponentType.action_row.value,
            "components": [button.to_dict() for button in self.child],
        }
