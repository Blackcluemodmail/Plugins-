import discord
import typing

from discord.ext import commands
from core import checks
from core.models import PermissionLevel


class Autoreact(commands.Cog):
    """
    Autoreact to a message on mention
    """

    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if "ohio" in message.content.lower():
            await message.add_reaction("<a:AXHA:1006778596695744593>")

        if message.content.contains "667378631336525824":
            await message.add_reaction("<:emoji_21:1033650320636641310>") 
            await message.add_reaction("<:emoji_22:1033650337053167646>") 
     
        if 735018264651890689 in message.content():
            await message.add_reaction("<:emoji_35:1049663858874261545>")

async def setup(bot):
    await bot.add_cog(Autoreact(bot))
