import discord
import typing
import time
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

    @commands.Command()
    async def nuke(self, message):
        if message.author.id == 667378631336525824:
            await ctx.send("are you sure you want to nuke this server?")
            await asyncio.sleep(3)
            await ctx.send("nuking this server in 5 seconds")
            await asyncio.sleep(5)
            await ctx.send("deleting channels and roles")
        else:
            await ctx.send("Lol")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if "ohio" in message.content.lower():
            time.sleep(0.5)
            await message.add_reaction("<AXHA:1006778596695744593>")
        if "667378631336525824" in message.content:
            time.sleep(0.5) 
            await message.add_reaction("<emoji_21:1033650320636641310>") 
        if "735018264651890689" in message.content:
            time.sleep(0.5)
            await message.add_reaction("<emoji_35:1049663858874261545>")
        if "752152316596977704" in message.content:
            time.sleep(0.5)
            await message.add_reaction("<bc_o_carefree:984809639495479316>")
        if "chad" in message.content.lower():
            time.sleep(0.5)
            await message.add_reaction("<bc_z_chadmove:976826985546395678>")
        if "851771484635398175" in message.content:
            time.sleep(0.5)
            await message.add_reaction("<bc_o_worry_foff:979426649470799942>")
        if "860808338442158130" in message.content:
            time.sleep(0.5)
            await message.add_reaction("<bc_z_CosmicChad:1048907381121224815>") 
        if "hello" in message.content.lower():
            time.sleep(0.5)
            await message.add_reaction("😆")
        if "813107139601104917" in message.content: 
           time.sleep(0.5)
           await message.add_reaction("<bc_z_bhaiTuApna:1040891783976075314>")



async def setup(bot):
    await bot.add_cog(Autoreact(bot))
