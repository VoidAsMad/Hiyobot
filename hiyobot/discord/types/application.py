from typing import Literal, Optional, TypedDict, Union

from hiyobot.discord.types.snowflake import Snowflake

ApplicationCommandOptionTypes = Literal[1]
ApplicationCommandTypes = Literal[1, 2, 3, 4, 6, 7, 8, 9, 10]


class ApplicationCommandOptionChoice(TypedDict):
    name: str
    value: Union[str, int]


class _ApplicationCommandInteractionDataOptionOptional(TypedDict, total=False):
    value: Optional[ApplicationCommandOptionTypes]
    options: Optional[list["ApplicationCommandInteractionDataOption"]]


class ApplicationCommandInteractionDataOption(
    _ApplicationCommandInteractionDataOptionOptional
):
    name: str
    type: int


class _ApplicationCommandOptionOptional(TypedDict, total=False):
    required: Optional[bool]
    choices: Optional[list[ApplicationCommandOptionChoice]]
    options: Optional[list["ApplicationCommandOption"]]


class ApplicationCommandOption(_ApplicationCommandOptionOptional):
    type: ApplicationCommandOptionTypes
    name: str
    description: str


class _ApplicationCommandOptional(TypedDict, total=False):
    type: Optional[ApplicationCommandTypes]
    guild_id: Optional[Snowflake]
    options: Optional[list[ApplicationCommandOption]]
    default_permission: Optional[bool]


class ApplicationCommand(_ApplicationCommandOptional):
    id: Snowflake
    application_id: Snowflake
    name: str
    description: str


class _ApplicationRegisterCommmandOptional(TypedDict, total=False):
    options: Optional[list[ApplicationCommandOption]]
    default_permission: Optional[bool]
    type: Optional[ApplicationCommandTypes]


class ApplicationRegisterCommmand(_ApplicationRegisterCommmandOptional):
    name: str
    description: str
