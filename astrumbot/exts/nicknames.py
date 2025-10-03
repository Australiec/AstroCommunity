import logging
import disnake
from disnake.ext import commands
from astrumbot.utils.api import api_request
from astrumbot import settings

logger = logging.getLogger(__name__)

class Nicknames(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        if member.bot: return

        response = await api_request(f"{settings.api_server}/{member.id}")
        if response is None or response == "Server Error" or response == "none": return

        await member.edit(nick=response)
        print(f"Пользователю {member.id} был поменян ник на {response} на сервере {member.guild}")

    @commands.slash_command(default_member_permissions=disnake.Permissions(administrator=True), guild_only=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def update_nickname(
            self,
            inter: disnake.ApplicationCommandInteraction,
            member: disnake.Member = commands.Param(name="пользователь", description="Выберите пользователя")
    ):
        """Обновляет ник для пользователя"""
        await self.update_nickname_logic(inter, member)

    @commands.user_command(name="Обновить ник", default_member_permissions=disnake.Permissions(administrator=True), guild_only=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def update_nickname_context(
            self,
            inter: disnake.UserCommandInteraction,
            member: disnake.Member
    ):
        """Обновляет ник для пользователя"""
        await self.update_nickname_logic(inter, member)

    async def update_nickname_logic(self, inter, member):
        await inter.response.defer(ephemeral=True)

        response = await api_request(f"{settings.api_server}/{member.id}")
        if response is None or response == "Server Error":
            return await inter.edit_original_response(
                embed=disnake.Embed(
                    title=":x: Ошибка",
                    description="ASTRUM не отвечает, не получилось изменить ник!",
                    color=disnake.Color.red()
                )
            )

        if response == "none":
            return await inter.edit_original_response(
                embed=disnake.Embed(
                    title=":x: Ошибка",
                    description="К этому Дискорду еще нету привязанного ника!",
                    color=disnake.Color.red()
                )
            )

        await member.edit(nick=response)
        print(f"Пользователю {member.id} был поменян ник на {response} на сервере {member.guild}")

        return await inter.edit_original_response(
            embed=disnake.Embed(
                title=":white_check_mark: Успех",
                description=f"Пользователю <@{member.id}> был установлен его текущий ник на сервере: `{response}`",
                color=disnake.Color.green()
            )
        )


def setup(bot: commands.Bot):
    bot.add_cog(Nicknames(bot))
    logger.info("%s loaded", __name__)