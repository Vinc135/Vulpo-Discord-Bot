import discord
from discord.ext import commands
import asyncio
import random

import mysql.connector
from info import get_syntax
##########

def random_color():
    return discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#welcome message

    @commands.Cog.listener()
    async def on_member_join(self, member):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID FROM welcome WHERE guildID = {member.guild.id}")
        channel = cursor.fetchone()
        cursor.execute(f"SELECT msg FROM welcome WHERE guildID = {member.guild.id}")
        message = cursor.fetchone()
        if channel == None and message == None:
            return
        else:
            try:
                ch = member.guild.get_channel(int(channel[0]))
            except:
                return
            finalmsg = message[0].replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
            try:
                embed = discord.Embed(color=random_color(), description=finalmsg)
                await ch.send(embed=embed)
            except:
                pass
            mydb.close()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def testjoin(self, ctx):
        """Sendet die Willkommensnachricht an den Kanal, um zu sehen, ob sie funktioniert."""
        member = ctx.author

        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID FROM welcome WHERE guildID = {member.guild.id}")
        channel = cursor.fetchone()
        cursor.execute(f"SELECT msg FROM welcome WHERE guildID = {member.guild.id}")
        message = cursor.fetchone()
        if channel == None and message == None:
            embed = discord.Embed(description=f"Die Willkommensnachricht ist auf diesem Server deaktiviert. Fügen eine mit **{ctx.prefix}joinmsg** hinzu", color=discord.Color.green())
            await ctx.send(embed=embed)
            return
        else:
            try:
                ch = ctx.guild.get_channel(int(channel[0]))
            except:
                return
            finalmsg = message[0].replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
            try:
                embed = discord.Embed(color=random_color(), description=finalmsg)
                embed.set_footer(text=f"Test-Willkommensnachricht angefordert von {ctx.author}")
                await ch.send(embed=embed)
                await ctx.send(f"Die Test-Willkommensnachricht wurde an den Kanal {ch.mention} gesendet.")
            except:
                pass
        mydb.close()
        
    @commands.command(usage="[update]")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def joinmsg(self, ctx, arg=None):
        """Legt die Willkommensnachricht fest und zeigt die aktuelle an."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID FROM welcome WHERE guildID = {ctx.guild.id}")
        channel = cursor.fetchone()
        cursor.execute(f"SELECT msg FROM welcome WHERE guildID = {ctx.guild.id}")
        message = cursor.fetchone()
        if channel == None and message == None or arg == "update":
            a = 0
            b = 0
            embed = discord.Embed(title="__Aktiviere die Willkommensnachricht__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
            message = await ctx.send(embed=embed)
            await asyncio.sleep(3)

            fragen = [1, 2]
            answers = []

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            for i in fragen:
                b += 1
                if b == 1:
                    newembed = discord.Embed(title="__Aktiviere die Willkommensnachricht__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                    newembed.add_field(name="Kanal", value="In welchem Kanal soll die Begrüßungsnachricht sein?", inline=False)
                    await message.edit(embed=newembed)
                try:
                    input = await self.bot.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("❌ Du hast die Fragen nicht in der vorgegebenen Zeit beantwortet. Sei beim nächsten Mal schneller!")
                    return
                else:
                    await input.delete()
                    answers.append(input.content)
                    a += 1
                    if a == 1:
                        try:
                            channel_id = int(answers[0][2:-1])
                            channel = self.bot.get_channel(channel_id)
                            newembed = discord.Embed(title="__Aktiviere die Willkommensnachricht__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                            newembed.add_field(name="Kanal", value=channel.mention, inline=False)
                            newembed.add_field(name="Nachricht", value="**Gib eine Willkommensnachricht ein!**\n*Du kannst diese Variablen für die Nachricht verwenden:*\n**%member** - Beispiel: Vulpo#6602\n**%name** - Beispiel: Vulpo\n**%mention** - Beispiel: @Vulpo\n**%guild** - Der Servername\n**%usercount** - Die Anzahl der Mitglieder im Server", inline=False)
                            await message.edit(embed=newembed)
                        except:
                            newembed = discord.Embed(title="❌ __Setup abgebrochen__", description=f"Du hast keinen Kanal erwähnt. Mach es beim nächsten Mal so wie: {ctx.channel.mention}", color=discord.Color.red())
                            await message.edit(embed=newembed)
                            return
                    if a == 2:
                        finalemb = discord.Embed(title="__Aktiviere die Willkommensnachricht__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                        finalemb.add_field(name="Kanal", value=channel.mention, inline=False)
                        finalemb.add_field(name="Nachricht", value=answers[1], inline=False)

            msg = answers[1]
            if arg == "update":
                cursor.execute("UPDATE welcome SET channelID = (%s), msg = (%s) WHERE guildID = (%s)", (channel.id, msg, ctx.guild.id))
                mydb.commit()
            if arg == None:
                cursor.execute("INSERT INTO welcome (guildID, channelID, msg) VALUES (%s, %s, %s)", (ctx.guild.id, channel.id, msg))
                mydb.commit()

            await message.edit(content=f"{ctx.author.mention} hat eine Willkommensnachricht eingerichtet", embed=finalemb)
        else:
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT channelID FROM welcome WHERE guildID = {ctx.guild.id}")
            wel = cursor.fetchone()
            cursor.execute(f"SELECT msg FROM welcome WHERE guildID = {ctx.guild.id}")
            come = cursor.fetchone()   

            try:
                ch = ctx.guild.get_channel(int(wel[0]))
            except:
                return

            embed = discord.Embed(title="Willkommensnachricht", description=f"Zum Aktualisieren der Nachricht einfach **{ctx.prefix}welcome update** schreiben.", color=discord.Color.green())
            embed.add_field(name="Kanal", value=ch, inline=False)
            embed.add_field(name="Nachricht", value=come[0], inline=False)
            await ctx.send(embed=embed)

        mydb.close()
#leave message
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID FROM leavemsg WHERE guildID = {member.guild.id}")
        channel = cursor.fetchone()
        cursor.execute(f"SELECT msg FROM leavemsg WHERE guildID = {member.guild.id}")
        message = cursor.fetchone()
        if channel == None and message == None:
            return
        else:
            try:
                ch = member.guild.get_channel(int(channel[0]))
            except:
                return
            finalmsg = message[0].replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
            try:
                embed = discord.Embed(color=random_color(), description=finalmsg)
                await ch.send(embed=embed)
            except:
                pass
            mydb.close()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def testleave(self, ctx):
        """Sendet die Leave-Nachricht an den Channel, um zu sehen, ob sie funktioniert."""
        member = ctx.author

        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID FROM leavemsg WHERE guildID = {member.guild.id}")
        channel = cursor.fetchone()
        cursor.execute(f"SELECT msg FROM leavemsg WHERE guildID = {member.guild.id}")
        message = cursor.fetchone()
        if channel == None and message == None:
            embed = discord.Embed(description=f"Die Leave-Nachricht ist auf diesem Server deaktiviert. Füge eine mit **{ctx.prefix}leave** hinzu", color=discord.Color.green())
            await ctx.send(embed=embed)
            return
        else:
            try:
                ch = ctx.guild.get_channel(int(channel[0]))
            except:
                return
            finalmsg = message[0].replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
            try:
                embed = discord.Embed(color=random_color(), description=finalmsg)
                embed.set_footer(text=f"Test-Verlassensnachricht angefordert von {ctx.author}")
                await ch.send(embed=embed)
                await ctx.send(f"Die Test-Verlassensnachricht wurde an den Kanal {ch.mention} gesendet.")
            except:
                pass
        mydb.close()
        
        
    @commands.command(usage="[update]")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def leavemsg(self, ctx, arg=None):
        """Setzt die Abwesenheitsnachricht und zeigt die aktuelle an."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID FROM leavemsg WHERE guildID = {ctx.guild.id}")
        channel = cursor.fetchone()
        cursor.execute(f"SELECT msg FROM leavemsg WHERE guildID = {ctx.guild.id}")
        message = cursor.fetchone()
        if channel == None and message == None or arg == "update":
            a = 0
            b = 0
            embed = discord.Embed(title="__Aktiviere die Leave-Message__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
            message = await ctx.send(embed=embed)
            await asyncio.sleep(3)

            fragen = [1, 2]
            answers = []

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            for i in fragen:
                b += 1
                if b == 1:
                    newembed = discord.Embed(title="__Aktiviere die Leave-Message__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                    newembed.add_field(name="Kanal", value="In welchen Kanal soll die Abschiedsnachricht gesendet werden?", inline=False)
                    await message.edit(embed=newembed)
                try:
                    input = await self.bot.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("❌ Du hast die Fragen nicht in der vorgegebenen Zeit beantwortet. Sei beim nächsten Mal schneller!")
                    return
                else:
                    await input.delete()
                    answers.append(input.content)
                    a += 1
                    if a == 1:
                        try:
                            channel_id = int(answers[0][2:-1])
                            channel = self.bot.get_channel(channel_id)
                            newembed = discord.Embed(title="__Aktiviere die Leave-Message__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                            newembed.add_field(name="Kanaö", value=channel.mention, inline=False)
                            newembed.add_field(name="Message", value="**Enter a leave message!**\n*Sie können diese Variablen für die Nachricht verwenden:*\n**%member** - Beispiel: Vulpo#6602\n**%name** - Beispiel: Vulpo\n**%mention** - Beispiel: @Vulpo\n**%guild** - Der Servername\n**%usercount** - Die Anzahl der Mitglieder im Server", inline=False)
                            await message.edit(embed=newembed)
                        except:
                            newembed = discord.Embed(title="❌ __Setup abgebrochen__", description=f"Du hast keinen Kanal erwähnt. Mach es beim nächsten Mal so wie: {ctx.channel.mention}", color=discord.Color.red())
                            await message.edit(embed=newembed)
                            return
                    if a == 2:
                        finalemb = discord.Embed(title="__Aktiviere die Leave-Message__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                        finalemb.add_field(name="Channel", value=channel.mention, inline=False)
                        finalemb.add_field(name="Nachricht", value=answers[1], inline=False)

            msg = answers[1]
            if arg == "update":
                cursor.execute("UPDATE leavemsg SET channelID = (%s), msg = (%s) WHERE guildID = (%s)", (channel.id, msg, ctx.guild.id))
                mydb.commit()
            if arg == None:
                cursor.execute("INSERT INTO leavemsg (guildID, channelID, msg) VALUES (%s, %s, %s)", (ctx.guild.id, channel.id, msg))
                mydb.commit()

            await message.edit(content=f"{ctx.author.mention} hat eine Abschiedsnachricht eingerichtet", embed=finalemb)
        else:
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT channelID FROM leavemsg WHERE guildID = {ctx.guild.id}")
            wel = cursor.fetchone()
            cursor.execute(f"SELECT msg FROM leavemsg WHERE guildID = {ctx.guild.id}")
            come = cursor.fetchone()   

            try:
                ch = ctx.guild.get_channel(int(wel[0]))
            except:
                return

            embed = discord.Embed(title="Nachricht hinterlassen", description=f"Zum Aktualisieren der Nachricht einfach **{ctx.prefix}leave update** senden.", color=discord.Color.green())
            embed.add_field(name="Kanal", value=ch, inline=False)
            embed.add_field(name="Message", value=come[0], inline=False)
            await ctx.send(embed=embed)

        mydb.close()


    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot or "blacklist remove" in msg.content:
            return
        try:
            if msg.author.guild_permissions.manage_messages:
                return
        except:
            pass
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT word FROM blacklist WHERE guildID = {msg.guild.id}")
        result = cursor.fetchall()
        if result is None:
            return
        for word in result:
            if str(word[0]) in str(msg.content):
                await msg.delete()
                cursor.execute("SELECT warnID FROM warns WHERE userID = (%s) AND guildID = (%s)", (msg.author.id, msg.guild.id))
                r = cursor.fetchall()
                if result is None:
                    cursor.execute("INSERT INTO warns(guildID, userID, grund, warnID) VALUES(%s, %s, %s, %s)", (msg.guild.id, msg.author.id, f"Hat ein verbotenes Wort gesendet: ||{word[0]}||", 1))
                if result != None:
                    warnID = 1
                    for warn in r:
                        warnID += 1
                    await asyncio.sleep(1)
                    cursor.execute("INSERT INTO warns(guildID, userID, grund, warnID) VALUES(%s, %s, %s, %s)", (msg.guild.id, msg.author.id, f"Hat ein verbotenes Wort gesendet: ||{word[0]}||", warnID))
                cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {msg.guild.id}")
                result = cursor.fetchone()
                if result != None:
                    chan = msg.guild.get_channel(int(result[0]))
                    if chan is None:
                        return
                    embed = discord.Embed(colour=discord.Colour.gold(),
                                    description=f"Der Benutzer {msg.author} (**{msg.author.id}**) wurde verwarnt.")
                    embed.add_field(name=f"🎛️ Server:", value=f"{msg.guild.name}", inline=False)
                    embed.add_field(name=f"👮 Moderator:", value=f"Vulpo#3749", inline=False)
                    embed.add_field(name=f"📄 Grund:", value=f"Hat ein verbotenes Wort gesendet. ||{msg.content}||", inline=False)
                    embed.set_author(name=msg.author, icon_url=msg.author.avatar)
                    await chan.send(embed=embed)
                await msg.channel.send(f"{msg.author.mention} Bitte unterlasse diesen Ausdruck. Du wurdest verwarnt!")
                
        mydb.commit()
        mydb.close()

    @commands.group(invoke_without_command=True, usage="<add <word>, remove>")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def blacklist(self, ctx):
        """Zeigt alle Wörter auf der Blacklist und alle Befehle die du benutzen kannst, um Wörter der Blacklist hinzuzufügen und der Blacklist zu entfernen."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT word FROM blacklist WHERE guildID = {ctx.guild.id}")
        result = cursor.fetchall()
        if result is None:
            await ctx.send(f"Die Blacklist dieses Servers ist leer.\nWort der Blacklist hinzufügen: `{ctx.prefix}blacklist add <wort>\n`Wort von der Blacklist entfernen: `{ctx.prefix}blacklist remove <wort>`")
            return
        desc = ""
        for word in result:
            desc += f"{word[0]}\n"
        if desc == "":
            desc = f"Die Blacklist dieses Servers ist leer.\nWort der Blacklist hinzufügen: `{ctx.prefix}blacklist add <wort>\n`Wort von der Blacklist entfernen: `{ctx.prefix}blacklist remove <wort>`"
        embed = discord.Embed(title="Die Blacklist", description=desc + f"\nWort der Blacklist hinzufügen: `{ctx.prefix}blacklist add <wort>\n`Wort von der Blacklist entfernen: `{ctx.prefix}blacklist remove <wort>`", color=discord.Color.red())
        await ctx.send(embed=embed)
        mydb.close()

    @blacklist.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def add(self, ctx, *, word=None):
        """Füge ein Wort der Blacklist hinzu."""
        if word == None:
            await get_syntax(ctx)
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute("INSERT INTO blacklist(guildID, word) VALUES(%s, %s)", (ctx.guild.id, word))
        await ctx.send(f"Das Wort `{word}` ist nun auf der Blacklist.")
        mydb.commit()
        mydb.close()

    @blacklist.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def remove(self, ctx, *, word=None):
        """Entferne ein Wort von der Blacklist."""
        if word == None:
            await get_syntax(ctx)
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT word FROM blacklist WHERE guildID = (%s) AND word = (%s)", (ctx.guild.id, word))
        result = cursor.fetchall()
        if result is None:
            await ctx.send(f"Das Wort `{word}` existiert nicht in der Blacklist.")
            return
        cursor.execute("DELETE FROM blacklist WHERE word = (%s) AND guildID = (%s)", (word, ctx.guild.id))
        await ctx.send(f"Das Wort `{word}` ist nun nicht mehr auf der Blacklist.")
        mydb.commit()
        mydb.close()
        
async def setup(bot):
    await bot.add_cog(message(bot))