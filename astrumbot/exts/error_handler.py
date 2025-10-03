import logging

import disnake
from disnake.ext import commands

from astrumbot import settings

logger = logging.getLogger(__name__)


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(
        self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError
    ):

        if isinstance(error, commands.MissingPermissions) and inter.guild is None:
            return

        if isinstance(error, commands.CommandOnCooldown):
            return await inter.send(
                embed=disnake.Embed(
                    description=f"> ## :clock3: Кулдаун\n"
                                f"Немного подождите перед повторным выполнением команды!",
                    color=disnake.Color.light_grey(),
                ), ephemeral=True,
            )

        raise error


def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
    logger.info("%s loaded", __name__)