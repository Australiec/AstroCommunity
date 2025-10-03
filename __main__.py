import asyncio

from astrumbot import settings, log
from astrumbot.bot import AstrumBot

log.setup()

bot = AstrumBot()

bot.load_extensions("astrumbot/exts")

if __name__ == "__main__":
    bot.run(settings.TOKEN)
