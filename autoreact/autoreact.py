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


  # --------- BLACKLISTING A MEMBER FROM SERVER -------     
 #   @commands.Cog.listener()
 #   async def on_member_join(self, member):
 #       un = 1046370746475229245 # THIS ROLE HAS NO PERMISSIONS IN ANY CHANNEL
  #     if member.id == 1050464201916821626:
  #          await member.add_roles(member.guild.get_role(un))
  #      elif member.id == 836598836449116220:
  #          await member.add_roles(member.guild.get_role(un))
  #      elif member.id == 763023382391554048:
   #         await member.add_roles(member.guild.get_role(un))
   #     elif member.id == 700238768657006602:
   #         await member.add_roles(member.guild.get_role(un))
   #     elif member.id == 972889240872566904:
   #         await member.add_roles(member.guild.get_role(un))
   #     elif member.id == 745996986951663697:
    #        await member.add_roles(member.guild.get_role(un))
   #     elif member.id == 683869766984794124:
    #        await member.add_roles(member.guild.get_role(un))
     #   else:
      #      return
  # -------------------------------

  #--------- Auto React --------
    @commands.Cog.listener()
    async def on_message(self, message):
        stk = message.guild.fetch_sticker(950684924246130708)
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
        if "813107139601104917" in message.content: 
            await message.add_reaction("<bc_z_bhaiTuApna:1040891783976075314>")
            time.sleep(0.5) 
        if "789107450942455828" in message.content:
            await message.add_reaction("<emoji_36:1050086330916405268>")
            time.sleep(0.5)
    # ----_-_----_-_-------------------
    
    # ----- Sticker Permissions --------
        lv10 = message.guild.get_role(906660899480272936)
        booster = message.guild.get_role(632529654812770325)
        srvstaff = message.guild.get_role(911126348372774912)
        chatmem = message.guild.get_role(938677457442205757)
        voicemem = message.guild.get_role(938677488438104134)
        trial = message.guild.get_role(907868778321301545)
        admin = message.guild.get_role(668774420583677983)
        ytmem = message.guild.get_role(740849706204397598)
        minecraftstaff = message.guild.get_role(906782010033438802)
        minecraftdev = message.guild.get_role(906781843972567040)
        rankholder = message.guild.get_role(1003196550220099654)
        verified = message.guild.get_role(906615384969474048)
        
        if message.stickers:
            if lv10 not in message.author.roles and booster not in message.author.roles and srvstaff not in message.author.roles and chatmem not in message.author.roles and voicemem not in message.author.roles and trial not in message.author.roles and admin not in message.author.roles and ytmem not in message.author.roles and minecraftstaff not in message.author.roles and minecraftdev not in message.author.roles and verified != message.author.roles and rankholder != message.author.roles:
                await message.delete()
            else:
                return
           

   # -------------------------------
        
   #----------- MEDIA DELETION AFTER FEW SECONDS WITH ROLE BYPASS ---------
      #  testrole = message.guild.get_role(873039799777361972) # role from dank memer server
      #  testrole2 = message.guild.get_role(770694204720283718) # role 2
        manager = message.guild.get_role(906618549370503168)
        for a in message.attachments:
            if a.filename.endswith(".png") or a.filename.endswith (".apng") or a.filename.endswith (".jpg") or a.filename.endswith(".jpeg"):
                gc = message.guild.get_channel(906577935874535455)
                if message.channel == gc and admin not in message.author.roles and manager not in message.author.roles:
                    time.sleep(30)
                    await message.delete()
                else:
                    return
   # ----------------------------

  # ------------ GIF DELETION AFTER A FEW SECONDS WITH ROLE BYPASS -------

        lv90 = message.guild.get_role(1051063310071644170)
        if "tenor.com" in message.content or ".gif" in message.content:
            if lv90 not in message.author.roles and admin not in message.author.roles and manager not in message.author.roles:
                await message.channel.send(f"{message.author.mention} That link is not allowed!", delete_after=10)
                await message.delete()
        if "tenor.com" in message.content or ".gif" in message.content:
            if lv90 in message.author.roles:
                time.sleep(30)
                await message.delete()
           
    @checks.has_permissions(PermissionLevel.MODERATOR)
    @commands.command()
    async def ranklog(self, ctx, member: discord.Member, gamertag, purchase, amount):
        """
        logs smp ranks
        """
        channel = member.guild.get_channel(960482007379497040)
        if member == None:
            await ctx.send_help(ctx.command)
        elif amount == None:
            await ctx.send("Please enter the amount")
        elif purchase == None: 
            await ctx.send("Please enter the rank name")
        elif gamertag == None:
            await ctx.send("Please enter the gamertag")
        
        embed = discord.Embed(title="Rank Purchase",
                color=self.bot.main_color,
                description = (
                    f"Discord Tag : {ctx.member.mention}\n"
                      "Discord User ID : {ctx.member.id}\n"
                      "Gamer Tag : {gamertag}\n"
                      "Amount : {amount}\n"
                      "Purchase type : {purchase}\n")
        await ctx.channel.send(embed=embed)
        if purchase == amethyst.lower():
            purchase = member.guild.get_role(1034474426902794321)
            await member.add_roles(purchase)
            time.sleep(30)
            await member.remove_roles(purchase)
                  
       
                              
                              

            
async def setup(bot):
    await bot.add_cog(Autoreact(bot))
