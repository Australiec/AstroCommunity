import logging

import disnake
from disnake.ext import commands

logger = logging.getLogger()

class AstrumBot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=disnake.Intents.all(),
            command_prefix=commands.when_mentioned,
        )

    async def on_ready(self):
        logger.info("Logged in as %s", self.user)