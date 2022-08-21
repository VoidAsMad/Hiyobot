from os import urandom
from typing import Any

from discord.embeds import Embed
from hiyobot.handler.app import Component, HiyobotRequest


class Pagenator(Component):
    def __init__(self, executor_id: int, embeds: list[Embed]) -> None:
        super().__init__()
        self.embeds = embeds
        self.executor_id = executor_id
        self.index = 0

        self.previous_id = self.rhex()
        self.next_id = self.rhex()
        self.close_id = self.rhex()

    async def interaction_check(self, request: HiyobotRequest) -> bool:
        if self.executor_id != int(request.json["member"]["user"]["id"]):
            await request.ctx.response.send("명령어 실행자만 상호작용이 가능합니다.", ephemeral=True)
            return False
        return True

    @property
    def raw(self) -> dict[str, Any]:
        return {
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "이전",
                            "emoji": {"id": None, "name": "◀️"},
                            "style": 1,
                            "custom_id": self.previous_id,
                        },
                        {
                            "type": 2,
                            "label": "다음",
                            "emoji": {"id": None, "name": "▶️"},
                            "style": 1,
                            "custom_id": self.next_id,
                        },
                        {
                            "type": 2,
                            "label": "닫기",
                            "emoji": {"id": None, "name": "❌"},
                            "style": 4,
                            "custom_id": self.close_id,
                        },
                    ],
                }
            ],
        }

    @property
    def total(self):
        return len(self.embeds)

    def rhex(self):
        return urandom(16).hex()

    @property
    def mapping(self):
        return {
            self.previous_id: self.previous,
            self.next_id: self.next,
            self.close_id: self.close,
        }

    async def next(self, request: HiyobotRequest):
        self.index += 1

        if self.index >= self.total:
            self.index = 0

        await request.ctx.response.edit(embed=self.embeds[self.index])

    async def previous(self, request: HiyobotRequest):
        self.index -= 1

        if self.index < 0:
            self.index = self.total - 1

        await request.ctx.response.edit(embed=self.embeds[self.index])

    async def close(self, request: HiyobotRequest):
        await request.ctx.response.delete()
