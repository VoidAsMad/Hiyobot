from _hiyobot.handler.app import Hiyobot
from _hiyobot.commands import *

bot = Hiyobot()

bot.sanic.run("0.0.0.0", 8000)
