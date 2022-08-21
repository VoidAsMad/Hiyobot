from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from discord.types.interactions import (
        Interaction as InteractionPayload,
        InteractionData,
    )

from discord.utils import _get_as_snowflake  # pyright: ignore [reportPrivateUsage]


class HiyobotInteraction:
    def __init__(self, data: "InteractionPayload"):
        self.id: int = int(data["id"])
        self.token: str = data["token"]
        self.version: int = data["version"]
        self.channel_id: Optional[int] = _get_as_snowflake(data, "channel_id")
        self.guild_id: Optional[int] = _get_as_snowflake(data, "channel_id")
        self.application_id: int = int(data["application_id"])
        self.data: Optional[InteractionData] = data.get("data")
