from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast
from _hiyobot.handler.interaction import HiyobotInteraction

from discord.http import HTTPClient

from mintchoco.client import Mintchoco
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey
from sanic import Request, Sanic
from sanic.exceptions import Unauthorized, InvalidUsage
from sanic.response import json  # pyright: ignore [reportUnknownVariableType]
from discord.webhook.async_ import AsyncWebhookAdapter

from _hiyobot.registry.command import RegisterCommand, RegisterdInfo


if TYPE_CHECKING:
    from discord.types.interactions import ApplicationCommandInteractionData


class HiyobotRequest(Request):
    headers: dict[str, Any]
    json: Any


class SingletonContext(SimpleNamespace):
    mintchoco: Mintchoco
    handler: "Hiyobot"
    discord: HTTPClient
    webhook_context: AsyncWebhookAdapter


class Context:
    def __init__(
        self, singleton_context: SingletonContext, request: HiyobotRequest
    ) -> None:
        self.singleton = singleton_context
        self.request = request
        self.interaction = HiyobotInteraction(self.request.json)


class Hiyobot:
    def __init__(
        self,
        client_public_key: str,
        token: str,
        uri: str = "discord_interaction",
        production: bool = False,
    ) -> None:
        self.sanic = Sanic("hiyobot")
        self.token = token
        self.client_public_key = client_public_key
        self.sanic.add_route(  # pyright: ignore [reportUnknownMemberType]
            self.handler, uri, ["POST"]
        )
        self.sanic.before_server_start(self.__setup)
        self.commands: dict[str, RegisterdInfo] = {}

    async def __setup(self, app: Sanic):
        self.ctx = SingletonContext()
        self.ctx.discord = HTTPClient(app.loop)
        self.ctx.mintchoco = Mintchoco()
        self.ctx.handler = self
        self.ctx.webhook_context = AsyncWebhookAdapter()

    @staticmethod
    def verify_signiture(
        raw_body: bytes, signature: str, timestamp: str, client_public_key: str
    ):
        message = timestamp.encode() + raw_body
        try:
            vk = VerifyKey(bytes.fromhex(client_public_key))
            vk.verify(message, bytes.fromhex(signature))
            return True
        except BadSignatureError:
            return False

    async def handler(self, request: HiyobotRequest):
        signature = request.headers.get("X-Signature-Ed25519")
        timestamp = request.headers.get("X-Signature-Timestamp")
        if (
            signature
            and request.json
            and timestamp
            and self.verify_signiture(
                request.body, signature, timestamp, self.client_public_key
            )
        ):
            context = Context(self.ctx, request)
            if request.json["type"] == 1:
                return json({"type": 1})

            if request.json["type"] == 2:
                return await self.dispatch_application_command(context)

            if request.json["type"] == 3:
                return await self.dispatch_message_component(context)

        raise Unauthorized("not_verified", 401)

    def register_command(self, command: RegisterCommand):
        self.commands.update({command.registerd_info.name: command.registerd_info})

    async def dispatch_chat_input_app_command(self, context: Context):
        assert context.interaction.data
        if name := context.interaction.data.get("name"):
            # Check Command
            if command := self.commands.get(name):
                # Get option
                options = context.interaction.data.get("options")
                if command := self.commands.get(name):
                    assert options
                    await command(context, *tuple(map(lambda x: x["value"], options)))
                    print(options)
            ...
        raise InvalidUsage

    async def dispatch_user_app_command(self):
        ...

    async def dispatch_message_app_command(self):
        ...

    async def dispatch_application_command(self, context: Context):
        if context.interaction.data:
            app_command_interaction_data = cast(
                "ApplicationCommandInteractionData", context.interaction.data
            )
            if app_command_interaction_data.get("type") == 1:
                await self.dispatch_chat_input_app_command(context)
            ...

    async def dispatch_message_component(self, context: Context):
        ...
