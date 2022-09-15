import discord
from discord.ext import commands
import typing
from datetime import datetime
from info import get_syntax

class server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ctc'], usage="<name>")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def createtextchannel(self, ctx, *, name=None):
        """Erstelle einen Textkanal."""
        if name is None:
            await get_syntax(ctx)
            return
        else:
            try:
                await ctx.guild.create_text_channel(name=f"{name}")
                embe = discord.Embed(title="Server Command",description=f"Ich habe einen Textkanal, mit dem Namen **{name}**, erstellt" ,color=discord.Colour.green(), timestamp=datetime.utcnow())
                embe.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embe)
                return
            except:
                embed = discord.Embed(colour=discord.Colour.red(), description=f"Der Name ist zu lang.", timestamp=datetime.utcnow())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return


    @commands.command(aliases=['cvc'], usage="<name>")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def createvoicechannel(self, ctx, *, name=None):
        """Erstelle ein Sprachkanal."""
        if name is None:
            await get_syntax(ctx)
            return
        else:
            try:
                await ctx.guild.create_voice_channel(name=f"{name}")
                embe = discord.Embed(title="Server Command",description=f"Ich habe einen Sprachkanal, mit dem Namen **{name}**, erstellt" ,color=discord.Colour.green(), timestamp=datetime.utcnow())
                embe.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embe)
                return
            except:
                embed = discord.Embed(colour=discord.Colour.red(), description=f"Der Name ist zu lang.", timestamp=datetime.utcnow())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

    @commands.command(aliases=['dc'], usage="<name>")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def deletechannel(self, ctx, channels: typing.Union[discord.TextChannel, discord.VoiceChannel]=None):
        """Lösche einen Kanal."""
        if channels is None:
            await get_syntax(ctx)
            return
        else:
            try:
                await channels.delete()
                embe = discord.Embed(title="Server Command",description=f"Ich habe einen Kanal mit dem Namen **{channels.name}** gelöscht." ,color=discord.Colour.green(), timestamp=datetime.utcnow())
                embe.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embe)
                return
            except:
                pass

    @commands.command(aliases=['cr'], usage="<name>")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def createrole(self, ctx, *, name=None):
        """Erstelle eine Rolle."""
        if name is None:
            await get_syntax(ctx)
            return
        else:
            try:
                await ctx.guild.create_role(name=f"{name}")
                embe = discord.Embed(title="Server Command",description=f"Ich habe eine Rolle mit dem Namen **{name}** erstellt." ,color=discord.Colour.green(), timestamp=datetime.utcnow())
                embe.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embe)
                return
            except:
                embed = discord.Embed(colour=discord.Colour.red(), description=f"Der Name ist zu lang.", timestamp=datetime.utcnow())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

    @commands.command(aliases=['dr'], usage="<name>")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def deleterole(self, ctx, *, name:discord.Role=None):
        """Lösche eine Rolle."""
        if name is None:
            await get_syntax(ctx)
            return
        else:
            try:
                await discord.Role.delete(name)
                embe = discord.Embed(title="Server Command",description=f"Ich habe eine Rolle mit dem Namen **{name}** gelöscht." ,color=discord.Colour.green(), timestamp=datetime.utcnow())
                embe.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embe)
                return
            except:
                embed = discord.Embed(colour=discord.Colour.red(), description=f"Der Name ist zu lang.", timestamp=datetime.utcnow())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

    @commands.command(aliases=['cc'], usage="<name>")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def createcategory(self, ctx, *, name=None):
        """Erstellt eine Kategorie."""
        if name is None:
            await get_syntax(ctx)
            return
        else:
            try:
                await ctx.guild.create_category(f'{name}')
                embe = discord.Embed(title="Server Command",description=f"Ich habe eine Kategorie mit dem Namen **{name}** erstellt." ,color=discord.Colour.green(), timestamp=datetime.utcnow())
                embe.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embe)
                return
            except:
                embed = discord.Embed(colour=discord.Colour.red(), description=f"Der Name ist zu lang.", timestamp=datetime.utcnow())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

    @commands.command(aliases=['cc'], usage="<name>")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def createcategory(self, ctx, *, name=None):
        """Löscht eine Kategorie."""
        if name is None:
            await get_syntax(ctx)
            return
        else:
            try:
                category = ctx.guild.get_channel(name)
                await category.delete()
                embe = discord.Embed(title="Server Command",description=f"Ich habe eine Kategorie mit dem Namen **{name}** gelöscht." ,color=discord.Colour.green(), timestamp=datetime.utcnow())
                embe.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embe)
                return
            except:
                embed = discord.Embed(colour=discord.Colour.red(), description=f"Der Name ist zu lang.", timestamp=datetime.utcnow())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

async def setup(bot):
    await bot.add_cog(server(bot))