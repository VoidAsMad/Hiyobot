from _hiyobot.component.actionrow import ActionRow
from _hiyobot.component.button import Button
from functools import partial


class ComponentHelper:
    def __init__(self, timeout: int = 60) -> None:
        self.timeout = timeout
        self.start_check_timeout = False

    @property
    def childs(self):
        childs: list[Button] = []
        # Recursive error
        for attr in set(dir(self)) - set(dir(ComponentHelper)):
            maybe_button = getattr(self, attr)
            if isinstance(maybe_button, Button):
                maybe_button.func = partial(maybe_button.func, self)
                childs.append(maybe_button)
        return childs

    @property
    def action_rows(self):
        return ActionRow(self.childs)

    def to_dict(self):
        return {"components": self.action_rows.to_dict()}
