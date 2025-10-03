import logging

import disnake
from disnake.ext import commands

from astrumbot import settings

logger = logging.getLogger(__name__)

class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError):
        await self.command_error_logic(inter, error)

    @commands.Cog.listener()
    async def on_user_command_error(self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError):
        await self.command_error_logic(inter, error)

    async def command_error_logic(self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            return await inter.send(
                embed=disnake.Embed(
                    description=f"> ## :clock3: Кулдаун\n"
                                f"Немного подождите перед повторным выполнением команды!",
                    color=disnake.Color.light_grey(),
                ), ephemeral=True,
            )
        if isinstance(error, commands.CommandInvokeError):
            return await inter.send(
                embed=disnake.Embed(
                    description=f"> ## :x: Ошибка\n"
                                f"У бота недостаточно разрешений для выполнения действий.\n"
                                f"- Выдайте боту права администратора\n"
                                f"- Поставьте роль бота максимально высоко в списке ролей",
                    color=disnake.Color.red(),
                ), ephemeral=True,
            )
        raise error

def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
    logger.info("%s loaded", __name__)