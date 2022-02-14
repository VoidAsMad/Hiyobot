from hiyobot.commands.hitomi import hitomi
from hiyobot.handler.app import Hiyobot

bot = Hiyobot(
    "client_public_key",
    "bot_token",
)
bot.command_register(hitomi)
bot.sanic.run("0.0.0.0", 8000)
