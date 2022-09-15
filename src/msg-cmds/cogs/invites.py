import discord
from discord.ext import commands
import DiscordUtils

bot = commands.Bot(command_prefix="!")
tracker = DiscordUtils.InviteTracker(bot)

class Invites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        inviter = await tracker.fetch_inviter(member)
        print(inviter)

    @commands.command()
    async def whoinvited(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author
        inviter = await tracker.fetch_inviter(member)
        embed=discord.Embed(description=f"Das Mitglied {member.mention} wurde von {inviter.mention} zum Server eingeladen!", color=discord.Color.orange())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Invites(bot))