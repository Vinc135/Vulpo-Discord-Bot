import discord
from discord.ext import commands
from datetime import datetime
import time
import sys
import psutil

class vulpo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.launch_time = datetime.utcnow()
        self.uptime = datetime.utcnow()

    @commands.command(aliases=["info","bot","botinfo"])
    @commands.guild_only()
    async def about(self, ctx):
        """Zeigt Infos über mich."""
        #uptime
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        all_users = 0

        #alle user
        all_users = 0
        for guild in self.bot.guilds:
            for member in guild.members:
                all_users += 1

        #teammember
        guild = self.bot.get_guild(925729625580113951)
        role = guild.get_role(947881106332582018)
        teammember = ""
        for member in role.members:
            if str(teammember) == "":
                teammember += f"{member}"
            else:
                teammember += f", {member}"

        embed = discord.Embed(color=discord.Color.orange(), title="Infos über Vulpo")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        embed.add_field(name="<:developer:964846664676429844> Entwickler",value=self.bot.get_user(824378909985341451))
        embed.add_field(name="<:team:965601672606932992> Team",value=teammember)
        embed.add_field(name="<a:live:964851937658961950> Online seit",value=f"{days} Tage, {hours} Stunden, {minutes} Minuten und {seconds} Sekunden")
        embed.add_field(name="<a:join:964850239565623356> Server", value=len(self.bot.guilds))
        embed.add_field(name="<:member:965600585724358676> User", value=all_users)
        embed.add_field(name="❗ Commands", value=len(self.bot.commands))
        embed.add_field(name="<:python:965603177883922483> Python Version", value=sys.version)
        embed.add_field(name="<:discordpy:965603293885792268> Library", value=f"discord.py: {discord.__version__}")
        embed.add_field(name="🎛 CPU", value=f"{psutil.cpu_percent()}%")

        await ctx.send(embed=embed)

    @commands.command(aliases=['inv'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def invite(self, ctx):
        """Zeigt einen Link um mich einzuladen."""
        embed = discord.Embed(colour=discord.Colour.blue(), title=f"Vulpo auf anderen Servern verwenden", description=f"Du kannst Vulpo mit [diesem Link](https://discord.com/api/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot) zu deinem Server hinzufügen.", url="https://discord.com/api/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sup'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def support(self, ctx):
        """Zeigt einen Link für den Support-Server."""
        embed = discord.Embed(colour=discord.Colour.blue(), title=f"Bekomme Hilfe", description=f"Wenn du Hilfe benötigst, kannst du meinem Supportserver über [diesen Link](https://discord.gg/49jD3VXksp) beitreten.", url="https://discord.gg/49jD3VXksp")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command(aliases=['internet'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def ping(self, ctx):
        """Zeigt den Ping"""
        #Websocket
        t_1 = time.perf_counter()
        embed = discord.Embed(title="Ping", description=f"```Bot: {round(self.bot.latency * 1000)} ms```", color=discord.Color.dark_red())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        msg = await ctx.send(embed=embed)
        #Answer
        t_2 = time.perf_counter()
        time_delta = round((t_2 - t_1) * 1000, 2)
        embed = discord.Embed(title="Pong", description=f"```Bot: {round(self.bot.latency * 1000)} ms\nDiscord-Api: {time_delta} ms```", color=discord.Color.dark_red())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await msg.edit(embed=embed)

    @commands.command(aliases=['online'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def uptime(self, ctx):
        """Zeigt meine Online-Zeit."""
        delta_uptime = datetime.utcnow() - self.uptime
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        embed = discord.Embed(colour=discord.Colour.green())
        embed.set_author(name=f"Online seit: {days}d {hours}h {minutes}m {seconds}s", icon_url=ctx.me.avatar)
        await ctx.send(embed=embed)

    @commands.command(aliases=['daten'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def datenschutz(self, ctx):
        """Erfahre was Vulpo mit deinen Daten anstellt."""
        embed=discord.Embed(color=discord.Color.orange(), title="Datenschutz des Bots Vulpo", description="""
        <:chat:934764219365199902> Vulpo speichert hauptsächlich die ID des Benutzers, die ID der Server und die ID des Channels, damit die Benutzer bestimmte Funktionen unseres Bots nutzen können. Und es gibt noch einige andere Daten, die wir nicht speichern, sondern in Echtzeit anzeigen, wie z.B. Userinfo und Serverinfo.\n
        <:chat:934764219365199902> Wir speichern die ID des Benutzers, damit es einfach ist, seinen Namen auf den globalen Ranglisten im Spiel anzuzeigen. Zweitens speichern wir die Server-ID, um ihnen die Nutzung bestimmter Funktionen zu ermöglichen. Schließlich speichern wir die Channel-ID, damit Server-Administratoren den Bot für Begrüßungsnachrichten und andere Funktionen verwenden können.\n
        <:chat:934764219365199902> Obwohl der Bot keine sensiblen Daten speichert, kann der Benutzer den Support-Server kontaktieren, um die Löschung seiner Daten zu beantragen.""")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(vulpo(bot))