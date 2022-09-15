import discord
from discord.ext import commands
import mysql.connector
import random

def random_color():
    return discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

async def publish(msg, self):
    try:
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT guildID, channelID FROM globalchat")
        result = cursor.fetchall()
        if result is None:
            return
        member = 0
        bots = 0
        for user in msg.guild.members:
            if user.bot is False:
                member += 1
            if user.bot is True:
                bots += 1
        g = self.bot.get_guild(925729625580113951)
        mod = g.get_role(925737344412291122)
        developer = g.get_role(934379369319792650)
        if mod in msg.author.roles:
            e = "👮‍♀️"
        if developer in msg.author.roles:
            e = "🧑🏻‍💻"
        else:
            e = "👤"
        embed = discord.Embed(title=f"`{e}`〢{msg.author.name}", description=f"*{msg.content}*", color=random_color())
        embed.set_footer(text=f"{msg.guild.name} (👥{member} | 🤖{bots})", icon_url=msg.guild.icon if msg.guild.icon else 'https://cdn.discordapp.com/icons/925729625580113951/63a2e510fb885f12da3173da3413864c.png?size=1024')
        embed.set_thumbnail(url=msg.author.avatar if msg.author.avatar else 'https://cdn.discordapp.com/icons/925729625580113951/63a2e510fb885f12da3173da3413864c.png?size=1024')
        try:
            embed.set_image(url=msg.attachments[0].url)
        except IndexError:
            pass
        if msg.reference is not None:
            embed.add_field(name="<:chat:934764219365199902> Antwort auf:", value=f"> {msg.reference.resolved.embeds[0].description}", inline=False)
        embed.add_field(name="Bot Links", value="**[Support server](https://discord.gg/49jD3VXksp) | [Invite](https://discord.com/api/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot) | [Vote](https://top.gg/bot/925799559576322078/vote)**")
        for i in result:
            guild = self.bot.get_guild(int(i[0]))
            if guild:
                channel = guild.get_channel(int(i[1]))
                if channel:
                    await channel.send(embed=embed)
        await msg.delete()
    except Exception as e:
        await msg.channel.send(e)

class Globalchat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1.0, 3.0, commands.BucketType.user)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if msg.channel.type == discord.ChannelType.private:
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT guildID, channelID FROM globalchat WHERE guildID = {msg.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if msg.channel.id != int(result[1]):
            return
        bucket = self._cd.get_bucket(msg)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await msg.delete()
            return
        else:
            await publish(msg, self)

    @commands.command(aliases=["gchat"], usage="[channel]")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def globalchat(self, ctx, channel: discord.TextChannel=None):
        """Dieser Befehl zeigt dein Level und deine Erfahrungspunkte."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID FROM globalchat WHERE guildID = {ctx.guild.id}")
        result = cursor.fetchone()
        if channel == None:
            if result is None:
                return await ctx.send(f"**❌ Auf diesem Server ist kein Globalchat aktiv. Lege einen fest mit `{ctx.prefix}globalchat <Kanal>`**")
            globalchatchannel = ctx.guild.get_channel(int(result[0]))
            if globalchatchannel is None:
                return await ctx.send(f"**❌ Auf diesem Server ist kein Globalchat aktiv. Lege einen fest mit `{ctx.prefix}globalchat <Kanal>`**")
            embed = discord.Embed(title="Globalchat", description=f"**Der Globalchat dieses Servers ist aktiv in {globalchatchannel.mention}.**", color=discord.Color.orange())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        if result == None:
            cursor.execute("INSERT INTO globalchat(guildID, channelID) VALUES(%s, %s)", (ctx.guild.id, channel.id))
        if result != None:
            cursor.execute(f"UPDATE globalchat SET channelID = {channel.id} WHERE guildID = {ctx.guild.id}")
        await channel.edit(topic="""
        Willkommen im Globalchat von Vulpo!
        Hier kannst du jede 3 Sekunden eine Nachricht an alle Server senden, die auch einen Globalchat mit Vulpo eingerichtet haben.
        Viel Spaß!""", slowmode_delay=3)
        await ctx.send(f"**✅ Der Globalchat dieses Servers ist nun aktiv in {channel.mention}**")
        mydb.commit()
        mydb.close()

async def setup(bot):
    await bot.add_cog(Globalchat(bot))