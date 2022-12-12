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

    @commands.command()
    async def nuke(self, message):
        if message.author.id == 667378631336525824:
            await message.send("are you sure you want to nuke this server?")
            time.sleep(3)
            await message.send("nuking this server in 5 seconds")
            time.sleep(5)
            await message.send("deleting channels and roles")
        else:
            await message.send("Lol")


        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        un = 1046370746475229245
        if member.id == 1050464201916821626:
            await member.add_roles(member.guild.get_role(un))
        elif member.id == 836598836449116220:
            await member.add_roles(member.guild.get_role(un))
        elif member.id == 763023382391554048:
            await member.add_roles(member.guild.get_role(un))
        elif member.id == 700238768657006602:
            await member.add_roles(member.guild.get_role(un))
        elif member.id == 972889240872566904:
            await member.add_roles(member.guild.get_role(un))
        elif member.id == 745996986951663697:
            await member.add_roles(member.guild.get_role(un))
        elif member.id == 683869766984794124:
            await member.add_roles(member.guild.get_role(un))
        else:
            return
  

    @commands.Cog.listener()
    async def on_message(self, message):
        roles = message.guild.get_role(1048656229448294400)
        if message.author.bot:
            return
        if "ohio" in message.content.lower():
            await message.add_reaction("<AXHA:1006778596695744593>")
            time.sleep(0.5)
        if "667378631336525824" in message.content:
            await message.add_reaction("<emoji_21:1033650320636641310>")
            await message.add_reaction("<emoji_22:1033650337053167646>")
            time.sleep(0.5)
        if "735018264651890689" in message.content:
            await message.add_reaction("<emoji_35:1049663858874261545>")
            time.sleep(0.5)
        if "752152316596977704" in message.content:
            await message.add_reaction("<bc_o_carefree:984809639495479316>")
            time.sleep(0.5)
        if "chad" in message.content.lower():
            await message.add_reaction("<bc_z_chadmove:976826985546395678>")
            time.sleep(0.5)
        if "851771484635398175" in message.content:
            await message.add_reaction("<bc_o_worry_foff:979426649470799942>")
            time.sleep(0.5)
        if "860808338442158130" in message.content:
            await message.add_reaction("<bc_z_CosmicChad:1048907381121224815>") 
            time.sleep(0.5)
        if "hello" in message.content.lower():
            await message.add_reaction("😆")
            time.sleep(0.5)
        if "813107139601104917" in message.content: 
            await message.add_reaction("<bc_z_bhaiTuApna:1040891783976075314>")
            time.sleep(0.5) 
        if "789107450942455828" in message.content:
            await message.add_reaction("<emoji_36:1050086330916405268>")
            time.sleep(0.5)
        
        # roles for sticker permissions
        lv10 = message.guild.get_role(906660899480272936)
        booster = message.guild.get_role(632529654812770325)
        srvstaff = message.guild.get_role(906618549370503168)
        chatmem = message.guild.get_role(938677457442205757)
        voicemem = message.guild.get_role(938677488438104134)
        trial = message.guild.get_role(907868778321301545)
        admin = message.guild.get_role(668774420583677983)
        ytmem = message.guild.get_role(740849706204397598)
        minecraftstaff = message.guild.get_role(906782010033438802)
        minecraftdev = message.guild.get_role(906781843972567040)
        rankholder = message.guild.get_role(1003196550220099654)
        verified = message.guild.get_role(906615384969474048)
        
        # sticker permissions

        if message.stickers:
            if lv10 == message.author.roles and booster == message.author.roles and srvstaff == message.author.roles and chatmem == message.author.roles and voicemem == message.author.roles and trial == message.author.roles and admin == message.author.roles and ytmem == message.author.roles and minecraftstaff == message.author.roles and minecraftdev == message.author.roles and verified == message.author.roles and rankholder == message.author.roles:
                return
   
            else:
                await message.delete()



        
               

            
async def setup(bot):
    await bot.add_cog(Autoreact(bot))
