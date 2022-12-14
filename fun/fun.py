import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import random
import asyncio
import time

class FunCommands(commands.Cog):
    """Fun commands for members to use!!"""
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.plugin_db.get_partition(self)


    @checks.has_permissions(PermissionLevel.MODERATOR)
    @commands.command()
    async def feed(self, ctx, member:discord.Member = None):
        feedGIF = [    
            "https://i.imgur.com/1vC0R20.gif",
            "https://data.whicdn.com/images/81561319/original.gif",
            "https://thumbs.gfycat.com/EagerSpectacularHoverfly-max-14mb.gif",
            "https://64.media.tumblr.com/4d160635539ef31d8b058bc3e35a907c/tumblr_p4e113SOw91wn2b96o1_400.gifv",
            "https://i.pinimg.com/originals/7a/cb/20/7acb209c594f42e0d56b87d70421c85d.gif",
               ]  

        if (member == ctx.author or member == None):
            feedSelfResponse = [
                f"{ctx.author.mention} feeds them selves. So eating?",
                f"{ctx.author.mention} feeds themselves yum!",
                f"{ctx.author.mention} is feeding their hungry stomach",
                f"{ctx.author.mention} is being fed by... themselves",
                 ]
            feed = random.choice(feedSelfResponse)
            embed = discord.Embed(color=0x9b59b6)
            embed.set_image(url=random.choice(feedGIF))
            embed.add_field(name="Feed", value=(feed))
            await ctx.send(embed=embed)
        else:
            feedResponse = [ 
            f"{ctx.author.mention} feeds {member.mention}",
            f"{member.mention} is being feed by {ctx.author.mention}. Open wide!",
            f"Yum! {ctx.author.mention} feeds {member.mention}. Here comes the airplane!",    
              ]  
            feed = random.choice(feedResponse)
            embed = discord.Embed(color=0x9b59b6)
            embed.set_image(url=random.choice(feedGIF))
            embed.add_field(name="Feed", value=(feed))
            await ctx.send(embed=embed)

    @checks.has_permissions(PermissionLevel.MODERATOR)
    @commands.command()
    async def tban(self, ctx, member:discord.Member = None):
        
        """ 
        Bans a member from discord server!
        (fun command)
        """
        await ctx.message.delete()
        if member == None:
            bmention = f"{ctx.author.mention} has been banned from **{ctx.author.guild}**"
            embed = discord.Embed(color=0x9b59b6)
            embed.set_image(url="https://images-ext-1.discordapp.net/external/H6c31dPQac4Keuzmwf5heM6mMMFGJU_tgqeF96T0PjU/https/media.tenor.com/images/01e6b4a18d1e4d5f375d421da3cf7ea1/tenor.gif")
            embed.add_field(name="Fun Commands", value=(bmention))
            embed.set_footer(text = f"Ban from {ctx.author}")
            await ctx.send(embed=embed, delete_after=30)
        else:
            bmention = f"{member.mention} has been banned from **{member.guild}**"
            embed = discord.Embed(color=0x9b59b6)
            embed.set_image(url="https://images-ext-1.discordapp.net/external/H6c31dPQac4Keuzmwf5heM6mMMFGJU_tgqeF96T0PjU/https/media.tenor.com/images/01e6b4a18d1e4d5f375d421da3cf7ea1/tenor.gif")
            embed.add_field(name="Fun Commands", value=(bmention))
            embed.set_footer(text = f"Ban from {ctx.author}")
            await ctx.send(embed=embed, delete_after=30)

    @checks.has_permissions(PermissionLevel.MODERATOR)
    @commands.command()
    async def ranklog(self, ctx, member: discord.Member, gamertag = None, purchase = None , amount = None):
        """
        logs smp ranks
        """
        if member == None:
            await ctx.send_help(ctx.command)
        channel = member.guild.get_channel(960482007379497040) 
        embed = discord.Embed(title="Rank Purchase",
                color=self.bot.main_color,
                description =(
                    f"Discord Tag : {member.mention}\n"
                     f"Discord User ID : {member.id}\n"
                     f"Gamer Tag : {gamertag}\n"
                     f"Amount : {amount}\n"
                     f"Purchase type : {purchase}\n")
                )
        embed.set_footer(text="Fun Plugin v1.0")

        await channel.send(embed=embed) 
        amethyst = "amethyst" 
        ruby = "ruby"
        obsidian = "obsidian"
        carneline = "carneline"
        epidote = "epidote"
        amazonite = "amazonite"
        smprank = member.guild.get_role(1003196550220099654)       
        if purchase == amethyst.lower():                 
            purchase = member.guild.get_role(1034474426902794321)
            await member.add_roles(purchase)
            await member.add_roles(smprank)
            embed = discord.Embed(
                    description = (f" Successfully added {purchase.mention} to {member.mention} for 30 days\n"
                                  f" Successfully added {smprank.mention} to {member.mention} for 30days\n"))
            await channel.send(embed=embed)
            await asyncio.sleep(2592000)
            await member.remove_roles(purchase)
            await member.remove_roles(smprank)
        elif purchase == ruby.lower():                 
            purchase = member.guild.get_role(1034474078754570353)
            await member.add_roles(purchase)
            await member.add_roles(smprank)
            embed = discord.Embed(
                    description = (f" Successfully added {purchase.mention} to {member.mention} for 30 days\n"
                                  f" Successfully added {smprank.mention} to {member.mention} for 30days\n"))
            await channel.send(embed=embed)
            await asyncio.sleep(2592000)
            await member.remove_roles(purchase)
            await member.remove_roles(smprank)
        elif purchase == obsidian.lower():                 
            purchase = member.guild.get_role(1034474068998631454)
            await member.add_roles(purchase)
            await member.add_roles(smprank)            
            embed = discord.Embed(
                    description = (f" Successfully added {purchase.mention} to {member.mention} for 30 days\n"
                                  f" Successfully added {smprank.mention} to {member.mention} for 30days\n"))
            await channel.send(embed=embed)
            await asyncio.sleep(2592000)
            await member.remove_roles(purchase)
            await member.remove_roles(smprank)            
        elif purchase == epidote.lower():                 
            purchase = member.guild.get_role(1034474059645329481)
            await member.add_roles(purchase)
            await member.add_roles(smprank)
            embed = discord.Embed(
                    description = (f" Successfully added {purchase.mention} to {member.mention} for 30 days\n"
                                  f" Successfully added {smprank.mention} to {member.mention} for 30days\n"))
            await channel.send(embed=embed)
            await asyncio.sleep(2592000)
            await member.remove_roles(purchase)
            await member.remove_roles(smprank)
        elif purchase == carneline.lower():                 
            purchase = member.guild.get_role(1034473986211467271)
            await member.add_roles(purchase)
            await member.add_roles(smprank)
            embed = discord.Embed(
                    description = (f" Successfully added {purchase.mention} to {member.mention} for 30 days\n"
                                  f" Successfully added {smprank.mention} to {member.mention} for 30days\n"))
            await channel.send(embed=embed)
            await asyncio.sleep(2592000)
            await member.remove_roles(purchase)
            await member.remove_roles(smprank)
        elif purchase == amazonite.lower():                 
            purchase = member.guild.get_role(1034473906863607889)
            await member.add_roles(purchase)
            await member.add_roles(smprank)
            embed = discord.Embed(
                    description = (f" Successfully added {purchase.mention} to {member.mention} for 30 days\n"
                                  f" Successfully added {smprank.mention} to {member.mention} for 30days\n"))
            await channel.send(embed=embed)
            await asyncio.sleep(2592000)
            await member.remove_roles(purchase)
            await member.remove_roles(smprank)                  
        else:
            embed = discord.Embed(
                    description = (
                       f"Couldn’t add roles to the {member.mention} due to incorrect log format!\n"
                       f"Please give them roles manially"))
            await channel.send(embed=embed)
            

                
                
            
            
async def setup(bot):
    await bot.add_cog(FunCommands(bot))
