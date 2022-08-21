from typing import Optional

from discord.types.interactions import Interaction as Payload
from discord.types.interactions import InteractionData as DataPayload
from discord.utils import _get_as_snowflake  # pyright: ignore [reportPrivateUsage]


class Interaction:
    def __init__(self, data: Payload):
        self.id: int = int(data["id"])
        self.token: str = data["token"]
        self.version: int = data["version"]
        self.channel_id: Optional[int] = _get_as_snowflake(data, "channel_id")
        self.guild_id: Optional[int] = _get_as_snowflake(data, "channel_id")
        self.application_id: int = int(data["application_id"])
        self.data: Optional[DataPayload] = data.get("data")
