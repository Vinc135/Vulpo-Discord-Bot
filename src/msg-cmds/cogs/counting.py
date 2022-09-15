import discord
from discord.ext import commands
import mysql.connector
import expr
from info import get_syntax
import asyncio

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="[channel]")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def count(self, ctx, channel: discord.TextChannel=None):
        """Lege einen Kanal fest, indem gezählt wird."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        if channel == None:
            cursor.execute(f"SELECT channelID FROM counting WHERE guildID = {ctx.guild.id}")
            result = cursor.fetchone()
            if result == None:
                await ctx.send(f"**❌ Hier ist kein Count-Channel eingerichtet. Richte einen mit `{ctx.prefix}count #channel` ein**")
                return
            if result != None:
                c = ctx.guild.get_channel(int(result[0]))
                if c == None:
                    await ctx.send(f"**❌ Hier ist kein Count-Channel eingerichtet. Richte einen mit `{ctx.prefix}count #channel` ein**")
                    return
                await ctx.send(f"**Der aktuelle Count-Channel ist hier {c.mention}**")
                return
        if channel != None:
            cursor.execute(f"SELECT channelID FROM counting WHERE guildID = {ctx.guild.id}")
            result = cursor.fetchone()
            if result == None:
                cursor.execute("INSERT INTO counting (channelID, guildID, zahl) VALUES (%s, %s, %s)", (channel.id, ctx.guild.id, 0))
            if result != None:
                cursor.execute("UPDATE counting SET channelID = (%s) WHERE guildID = (%s)", (channel.id, ctx.guild.id))
                cursor.execute("UPDATE counting SET zahl = (%s) WHERE guildID = (%s)", (0, ctx.guild.id))
            await ctx.send(f"✅ Es wird nun in {channel.mention} gezählt. Viel Spaß!\nDie nächste Zahl ist 1")
            mydb.commit()
            mydb.close()

    @commands.command(usage="<zahl>")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def setcount(self, ctx, zahl=None):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        if zahl == None:
            await get_syntax(ctx)
        try:
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT channelID FROM counting WHERE guildID = {ctx.guild.id}")
            result = cursor.fetchone()
            if result == None:
                await ctx.send(f"**❌ Hier ist kein Count-Channel eingerichtet. Richte einen mit `{ctx.prefix}count #channel` ein**")
                return
            if result != None:
                c = ctx.guild.get_channel(int(result[0]))
                if c == None:
                    await ctx.send(f"**❌ Hier ist kein Count-Channel eingerichtet. Richte einen mit `{ctx.prefix}count #channel` ein**")
                    return
                if c != None:
                    z = int(zahl)
                    cursor.execute("UPDATE counting SET zahl = (%s) WHERE guildID = (%s)", (z - 1, ctx.guild.id))
                    await ctx.send(f"**✅ Das Zählen beginnt nun bei {z}.**")
        except:
            await get_syntax(ctx)

        mydb.commit()
        mydb.close()

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if msg.guild == None:
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID, zahl FROM counting WHERE guildID = {msg.guild.id}")
        result = cursor.fetchone()
        if result == None:
            return
        if result != None:
            if int(result[0]) == int(msg.channel.id):
                try:
                    neue_zahl = expr.evaluate(msg.content)
                except:
                    await msg.delete()
                    return
                a = 0
                zahl = int(result[1])
                if int(neue_zahl) == int(zahl + 1):
                    async for message in msg.channel.history(limit=2, oldest_first=False):
                        a += 1
                        if a == 2:
                            if int(message.author.id) == int(msg.author.id) or int(message.author.id) == 925799559576322078:
                                m = await msg.reply("**❌ Warte bitte bis jemand anderes mitzählt. Alleine zählen ist doof.**\n*Diese Nachricht wird in 5 Sekunden gelöscht*")
                                await asyncio.sleep(5)
                                await m.delete()
                                await msg.delete()
                                return
                            else:
                                cursor.execute("UPDATE counting SET zahl = (%s) WHERE guildID = (%s)", (zahl + 1, msg.guild.id))
                                await msg.add_reaction("✅")
                else:
                    m = await msg.reply(f"**❌ Die nächste Zahl wäre {zahl + 1}**\n*Diese Nachricht wird in 5 Sekunden gelöscht*")
                    await asyncio.sleep(5)
                    await m.delete()
                    await msg.delete()
                    return
        mydb.commit()
        mydb.close()

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if msg.author.bot:
            return
        if msg.guild == None:
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID, zahl FROM counting WHERE guildID = {msg.guild.id}")
        result = cursor.fetchone()
        if result == None:
            return
        if result != None:
            if int(result[0]) == int(msg.channel.id):
                try:
                    neue_zahl = expr.evaluate(msg.content)
                    int(neue_zahl)
                except:
                    return
                zahl = int(result[1])
                if int(neue_zahl) == int(zahl + 1):
                    await msg.channel.send(f"**👮‍♀️ Es wurde die Zahl `{neue_zahl}` von {msg.author} gelöscht.**")
                    return
        mydb.commit()
        mydb.close()

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return
        if after.guild == None:
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID, zahl FROM counting WHERE guildID = {after.guild.id}")
        result = cursor.fetchone()
        if result == None:
            return
        if result != None:
            if int(result[0]) == int(after.channel.id):
                try:
                    zahl = expr.evaluate(before.content)
                    int(zahl)
                except:
                    return
                await after.channel.send(f"**👮‍♀️ Es wurde die Zahl `{zahl}` von {after.author} bearbeitet:**\n`{after.content}`")
                return
        mydb.commit()
        mydb.close()

async def setup(bot):
    await bot.add_cog(Counting(bot))