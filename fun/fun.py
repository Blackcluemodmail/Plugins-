import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import random
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
    async def ranklog(self, ctx, member: discord.Member, *, gamertag = None, purchase = None , amount = None):
        """
        logs smp ranks
        """
        channel = ctx.guild.get_channel(960482007379497040)
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
                description =(
                    f"Discord Tag : {member.mention}\n"
                     "Discord User ID : {member.id}\n"
                     "Gamer Tag : {gamertag}\n"
                     "Amount : {amount}\n"
                     "Purchase type : {purchase}\n")
                )
        embed.set_footer(text="Fun Plugin v1.0")

        await ctx.channel.send(embed=embed) 
        amethyst = "amethyst"         
        if purchase == amethyst.lower():                 
            purchase = member.guild.get_role(1034474426902794321)
            await member.add_roles(purchase)
            time.sleep(30)
            await member.remove_roles(purchase)
                  
        
async def setup(bot):
    await bot.add_cog(FunCommands(bot))
