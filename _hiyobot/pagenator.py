from discord.embeds import Embed
from _hiyobot.component.button import Button
from _hiyobot.component.helper import ComponentHelper


class Pagenator(ComponentHelper):
    def __init__(self, executor_id: int, embeds: list[Embed]) -> None:
        super().__init__()
        self.embeds = embeds
        self.executor_id = executor_id
        self.index = 0

    @property
    def total(self):
        return len(self.embeds)

    @Button.apply(label="다음", emoji="▶️")
    async def next(self, request):
        print(self.index, self.embeds)
        self.index += 1

        if self.index >= self.total:
            self.index = 0

        ...

    @Button.apply(label="이전", emoji="◀️")
    async def previous(self, request):
        print(self.index, self.embeds)
        self.index -= 1

        if self.index < 0:
            self.index = self.total - 1

        ...

    @Button.apply(label="닫기", emoji="❌")
    async def close(self, request):
        print(self.index, self.embeds)
        ...
