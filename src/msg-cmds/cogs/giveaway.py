import discord
from discord.ext import commands
import mysql.connector
import datetime
import asyncio
import random
import math
from info import check_member_role, get_syntax, giveaway_end, discord_timestamp, convert

class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["giveaway"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def gstart(self, ctx):
        """Starte ein Giveaway."""
        a = 0
        b = 0
        embed = discord.Embed(title="__Starte ein Giveaway__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
        message = await ctx.send(embed=embed)
        await asyncio.sleep(3)

        fragen = [1, 2, 3, 4, 5]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in fragen:
            b += 1
            if b == 1:
                newembed = discord.Embed(title="__Starte ein Giveaway__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                newembed.add_field(name="Kanal", value="In welchem Kanal soll das Giveaway stattfinden? Bitte erwähne einen Kanal.", inline=False)
                await message.edit(embed=newembed)
            try:
                input = await self.bot.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("❌ Du hast die Fragen nicht in der vorgegebenen Zeit beantwortet. Sei beim nächstem Mal schneller!")
                return
            else:
                await input.delete()
                answers.append(input.content)
                a += 1

                if a == 1:
                    try:
                        channel_id = int(answers[0][2:-1])
                        channel = self.bot.get_channel(channel_id)
                        newembed = discord.Embed(title="__Starte ein Giveaway__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                        newembed.add_field(name="Kanal", value=channel.mention, inline=False)
                        newembed.add_field(name="Dauer", value="Wie lange sollte das Giveaway dauern? [s, m, h, d]\nBeispiele: **1h 10m 46s**, **1h 28s**, **50m**", inline=False)
                        await message.edit(embed=newembed)
                    except:
                        newembed = discord.Embed(title="❌ __Giveaway abgebrochen__", description=f"Du hast keinen Kanal erwähnt. Mach es beim nächstem Mal so wie: {ctx.channel.mention}", color=discord.Color.red())
                        await message.edit(embed=newembed)
                        return
                if a == 2:
                    time = convert(answers[1])
                    if time == -1 or time == False:
                        newembed = discord.Embed(title="❌ __Giveaway abgebrochen__", description=f"Du musst die Zeit mit Einheiten angeben. (s, m, h, d)", color=discord.Color.red())
                        await message.edit(embed=newembed)
                        return
                    if time == -2:
                        newembed = discord.Embed(title="❌ __Giveaway abgebrochen__", description=f"Die Zeit muss eine ganze Zahl sein. Ohne Dezimalstellen..", color=discord.Color.red())
                        await message.edit(embed=newembed)
                        return
                    elif time < 10:
                        newembed = discord.Embed(title="❌ __Giveaway abgebrochen__", description=f"Die Dauer des Giveaways darf nicht weniger als 10 Sekunden betragen.", color=discord.Color.red())
                        await message.edit(embed=newembed)
                        return
                    else:
                        t1 = math.floor(datetime.datetime.utcnow().timestamp() + time + 7200)
                        t2 = datetime.datetime.fromtimestamp(int(t1))
                        newembed = discord.Embed(title="__Starte ein Giveaway__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                        newembed.add_field(name="Kanal", value=channel.mention, inline=False)
                        newembed.add_field(name="Dauer", value=discord_timestamp(t2, "f"), inline=False)
                        newembed.add_field(name="Preis", value="Was ist der Preis des Giveaways?", inline=False)
                        await message.edit(embed=newembed)
                if a == 3:
                    prize = answers[2]
                    newembed = discord.Embed(title="__Starte ein Giveaway__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                    newembed.add_field(name="Kanal", value=channel.mention, inline=False)
                    newembed.add_field(name="Dauer", value=discord_timestamp(t2, "f"), inline=False)
                    newembed.add_field(name="Preis", value=prize, inline=False)
                    newembed.add_field(name="Gewinner", value="Wieviele Teilnehmer können gewinnen?", inline=False)
                    await message.edit(embed=newembed)
                if a == 4:
                    try:
                        winners = int(answers[3])
                        if winners < 1 or winners > 25:
                            newembed = discord.Embed(title="❌ __Giveaway abgebrochen__", description=f"Die Gewinneranzahl muss 1-25 sein.", color=discord.Color.red())
                            await message.edit(embed=newembed)
                            return
                        else:
                            newembed = discord.Embed(title="__Starte ein Giveaway__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                            newembed.add_field(name="Kanal", value=channel.mention)
                            newembed.add_field(name="Dauer", value=discord_timestamp(t2, "f"), inline=False)
                            newembed.add_field(name="Preis", value=prize, inline=False)
                            newembed.add_field(name="Gewinner", value=winners, inline=False)
                            newembed.add_field(name="Anforderungen", value="Erforderliche Rolle, sende die Rollen-ID. (0 für keine)", inline=False)
                            await message.edit(embed=newembed)
                    except:
                        newembed = discord.Embed(title="❌ __Giveaway abgebrochen__", description=f"Die Gewinneranzahl muss 1-25 sein.", color=discord.Color.red())
                        await message.edit(embed=newembed)
                        return
                if a == 5:
                    if answers[4] == 0 or answers[4] == "0":
                        role = None
                        finalemb = discord.Embed(title="__Starte ein Giveaway__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                        finalemb.add_field(name="Kanal", value=channel.mention, inline=False)
                        finalemb.add_field(name="Dauer", value=discord_timestamp(t2, "f"), inline=False)
                        finalemb.add_field(name="Preis", value=prize, inline=False)
                        finalemb.add_field(name="Gewinner", value=winners, inline=False)
                        finalemb.add_field(name="Anforderungen", value=role, inline=False)
                        await message.edit(embed=finalemb)
                    else:
                        try:
                            r = int(answers[4])
                            role = ctx.guild.get_role(r)
                            if role is None or role is False:
                                newembed = discord.Embed(title="❌ __Giveaway abgebrochen__", description=f"Rolle nicht gefunden.", color=discord.Color.red())
                                await message.edit(embed=newembed)
                                return
                            else:
                                finalemb = discord.Embed(title="__Starte ein Giveaway__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                                finalemb.add_field(name="Kanal", value=channel.mention, inline=False)
                                finalemb.add_field(name="Dauer", value=discord_timestamp(t2, "f"), inline=False)
                                finalemb.add_field(name="Preis", value=prize, inline=False)
                                finalemb.add_field(name="Gewinner", value=winners, inline=False)
                                finalemb.add_field(name="Anforderungen", value=role.mention, inline=False)
                                await message.edit(embed=finalemb)
                        except:
                            newembed = discord.Embed(title="❌ __Giveaway abgebrochen__", description=f"Rolle nicht gefunden.", color=discord.Color.red())
                            await message.edit(embed=newembed)
                            return

        time_to_convert = math.floor(datetime.datetime.utcnow().timestamp() + time + 7200)
        time_converted = datetime.datetime.fromtimestamp(int(time_to_convert))

        await message.edit(content=f"{ctx.author.mention} hat ein Giveaway gestartet.\n• End Command: `{ctx.prefix}gend <id der nachricht vom giveaway>`", embed=finalemb)

        embed = discord.Embed(title=f"🏆 {prize}", description=f"**{ctx.author.mention}** hat ein Giveaway gestartet.\nEs wird **{winners}** Gewinner geben.", color=discord.Color.purple())
        if role != None:
            embed.add_field(name="🎭 Erforderliche Rolle", value=role.mention)
        embed.add_field(name="⏰ Endet in", value=f'{discord_timestamp(t2, "f")}({discord_timestamp(t2, "R")})')
        embed.set_footer(text="🍀 Viel Glück")

        m = await channel.send("**🎊 Neues Giveaway 🎊**", embed=embed)
        asyncio.create_task(giveaway_end(time_converted, self.bot, m.id))
        await m.add_reaction("🎉")
        #Insert in mysql
        try:
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            cursor = mydb.cursor(buffered=True)
            if role is None:
                cursor.execute("INSERT INTO active_giveaways(guildID, endtime, gwID, prize, channelID, winners) VALUES(%s, %s, %s, %s, %s, %s)", (ctx.guild.id, time_to_convert, m.id, prize, channel.id, winners))
            if role is not None:
                cursor.execute("INSERT INTO active_giveaways(guildID, endtime, gwID, prize, channelID, winners, roleID) VALUES(%s, %s, %s, %s, %s, %s, %s)",(ctx.guild.id, time_to_convert, m.id, prize, channel.id,winners, role.id))
            mydb.commit()
            mydb.close()
            await ctx.message.delete()
        except Exception as e:
            return await ctx.send(e)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        try:
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            cursor = mydb.cursor(buffered=True)
            cursor.execute("SELECT roleID FROM active_giveaways WHERE guildID = (%s) AND gwID = (%s)", (payload.guild_id, payload.message_id))
            result = cursor.fetchall()
            if result[0] is None:
                return
            else:
                for i in result:
                    guild = self.bot.get_guild(int(payload.guild_id))
                    role = guild.get_role(int(i[0]))
                    if role is None:
                        return
                    else:
                        if check_member_role(payload.member, role) is True:
                            return
                        else:
                            channel = guild.get_channel(int(payload.channel_id))
                            message = await channel.fetch_message(int(payload.message_id))
                            await message.remove_reaction("🎉", payload.member)
            mydb.close()
        except:
            pass
        try:
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            cursor = mydb.cursor(buffered=True)
            cursor.execute("SELECT roleID FROM old_giveaways WHERE guildID = (%s) AND gwID = (%s)",
                        (payload.guild_id, payload.message_id))
            result = cursor.fetchall()
            if result[0] is None:
                return
            else:
                for i in result:
                    guild = self.bot.get_guild(int(payload.guild_id))
                    role = guild.get_role(int(i[0]))
                    if role is None:
                        return
                    else:
                        if check_member_role(payload.member, role) is True:
                            return
                        else:
                            channel = guild.get_channel(int(payload.channel_id))
                            message = await channel.fetch_message(int(payload.message_id))
                            await message.remove_reaction("🎉", payload.member)
            mydb.close()
        except:
            pass

    @commands.command(usage="<Giveaway ID>")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def gend(self, ctx, giveaway_id=None):
        """Beendet ein Giveaway."""
        if giveaway_id == None:
            await get_syntax(ctx)
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        try:
            cursor.execute(f"SELECT prize, winners, channelID, roleID FROM active_giveaways WHERE gwID = {giveaway_id}")
            result = cursor.fetchone()
            if result is None:
                return await ctx.send("❌ Ich habe kein Giveaway mit dieser ID gefunden.")
        except:
            return await ctx.send("❌ Ich habe kein Giveaway mit dieser ID gefunden.")
        prize = result[0]
        winner_count = result[1]
        channel = ctx.guild.get_channel(int(result[2]))
        if channel is None:
            return await ctx.send("❌ Ich habe kein Giveaway mit dieser ID gefunden.")
        msg = await ctx.channel.fetch_message(int(giveaway_id))
        if msg is None:
            return await ctx.send("❌ Ich habe kein Giveaway mit dieser ID gefunden.")
        time_end = int(datetime.datetime.utcnow().timestamp())
        timestamp = datetime.datetime.fromtimestamp(int(time_end))

        reactions = [reaction for reaction in msg.reactions if reaction.emoji == "🎉"][0]
        participants = [user async for user in reactions.users()]
        participants.remove(ctx.guild.me)
        winner = random.sample(participants,k=len(participants) if len(participants) < int(winner_count) else int(winner_count))
        if len(winner) < 1:
            errorembed = discord.Embed(title=f"😕 Leider...", description='Es gab keinen Gewinner.',
                                    color=discord.Colour.purple())
            try:
                r = ctx.guild.get_role(int(result[3]))
                if r is None:
                    pass
                else:
                    errorembed.add_field(name="🎭 Erforderliche Rolle", value=r.mention)
            except:
                pass
            errorembed.add_field(name="⏰ Geendet am", value=f'{discord_timestamp(timestamp, "f")}({discord_timestamp(timestamp, "R")})')
            await msg.edit(content="**🏁 Giveaway beendet 🏁**", embed=errorembed)
            await msg.reply('Es gab zu wenig Teilnehmer an der Verlosung. :c')
            cursor.execute(f'DELETE FROM active_giveaways WHERE gwID = {giveaway_id}')
            cursor.execute(
                'INSERT INTO old_giveaways(guildID, gwID, prize, channelID, winners) VALUES (%s, %s, %s, %s, %s)',
                (ctx.guild.id, giveaway_id, prize, ctx.channel.id, winner_count))
            mydb.commit()
            return
        else:
            winners = ', '.join(win.mention for win in winner)
            winembed = discord.Embed(title=f"🎊 Glückwunsch", description=f'{winners} hat **{prize}** gewonnen',
                                    color=discord.Colour.purple())
            try:
                r = ctx.guild.get_role(int(result[3]))
                if r is None:
                    pass
                else:
                    winembed.add_field(name="🎭 Erforderliche Rolle", value=r.mention)
            except:
                pass
            winembed.add_field(name="⏰ Geendet am", value=f'{discord_timestamp(timestamp, "f")}({discord_timestamp(timestamp, "R")})')
            await msg.reply(f':tada: Glückwunsch {winners}! Du hast **{prize}** gewonnen.')
            await msg.edit(content="**🏁 Giveaway beendet 🏁**", embed=winembed)
            cursor.execute(f'DELETE FROM active_giveaways WHERE gwID = {giveaway_id}')
            cursor.execute(
                'INSERT INTO old_giveaways(guildID, gwID, prize, channelID, winners) VALUES (%s, %s, %s, %s, %s)',
                (ctx.guild.id, giveaway_id, prize, ctx.channel.id, winner_count))
            mydb.commit()
        mydb.close()

    @commands.command(usage="<Giveaway ID> [gewinneranzahl]")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def greroll(self, ctx, giveaway_id=None, gewinneranzahl=None):
        """Wiederhole ein geendetes Giveaway."""
        if giveaway_id == None:
            await get_syntax(ctx)
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        try:
            cursor.execute(f"SELECT prize, winners, channelID, roleID FROM old_giveaways WHERE gwID = {giveaway_id}")
            result = cursor.fetchone()
            if result is None:
                return await ctx.send("❌ Ich habe kein beendetes Giveaway mit dieser ID gefunden.")
        except:
            return await ctx.send("❌ Ich habe kein beendetes Giveaway mit dieser ID gefunden.")
        prize = result[0]
        if gewinneranzahl == None:
            winner_count = result[1]
        if gewinneranzahl != None:
            winner_count = int(gewinneranzahl)
        channel = ctx.guild.get_channel(int(result[2]))
        if channel is None:
            return await ctx.send("❌ Ich habe kein beendetes Giveaway mit dieser ID gefunden.")
        msg = await ctx.channel.fetch_message(int(giveaway_id))
        if msg is None:
            return await ctx.send("❌ Ich habe kein beendetes Giveaway mit dieser ID gefunden.")
        time_end = int(datetime.datetime.utcnow().timestamp())
        timestamp = datetime.datetime.fromtimestamp(int(time_end))
        reactions = [reaction for reaction in msg.reactions if reaction.emoji == "🎉"][0]
        participants = [user async for user in reactions.users()]
        participants.remove(ctx.guild.me)
        winner = random.sample(participants,
                            k=len(participants) if len(participants) < int(winner_count) else int(winner_count))
        if len(winner) == 0 or len(winner) < 1 or len(winner) < int(winner_count):
            errorembed = discord.Embed(title=f"😕 Leider...", description='Es gab keinen Gewinner.',
                                    color=discord.Colour.purple())
            try:
                r = ctx.guild.get_role(int(result[3]))
                if r is None:
                    pass
                else:
                    errorembed.add_field(name="🎭 Erforderliche Rolle", value=r.mention)
            except:
                pass
            errorembed.add_field(name="⏰ Erneut gestartet vor", value=f'{discord_timestamp(timestamp, "f")}({discord_timestamp(timestamp, "R")})')
            await msg.edit(content="**🔁 Giveaway neugestartet 🔁**", embed=errorembed)
            await msg.reply('Es gab zu wenig Teilnehmer an der Verlosung. :c')
            cursor.execute(f'DELETE FROM active_giveaways WHERE gwID = {giveaway_id}')
            cursor.execute(
                'INSERT INTO old_giveaways(guildID, gwID, prize, channelID, winners) VALUES (%s, %s, %s, %s, %s)',
                (ctx.guild.id, giveaway_id, prize, ctx.channel.id, winner_count))
            mydb.commit()
            return
        else:
            winners = ', '.join(win.mention for win in winner)
            winembed = discord.Embed(title=f"🎊 Glückwunsch", description=f'{winners} hat {prize} gewonnen',
                                    color=discord.Colour.purple())
            try:
                r = ctx.guild.get_role(int(result[3]))
                if r is None:
                    pass
                else:
                    winembed.add_field(name="🎭 Erforderliche Rolle", value=r.mention)
            except:
                pass
            winembed.add_field(name="⏰ Erneut gestartet vor", value=f'{discord_timestamp(timestamp, "f")}({discord_timestamp(timestamp, "R")})')
            await msg.reply(f':tada: Glückwunsch {winners}! Du hast **{prize}** gewonnen.')
            await msg.edit(content="**🔁 Giveaway neugestartet 🔁**", embed=winembed)
            cursor.execute(f'DELETE FROM active_giveaways WHERE gwID = {giveaway_id}')
            cursor.execute(
                'INSERT INTO old_giveaways(guildID, gwID, prize, channelID, winners) VALUES (%s, %s, %s, %s, %s)',
                (ctx.guild.id, giveaway_id, prize, ctx.channel.id, winner_count))
            mydb.commit()
        mydb.close()

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def glist(self, ctx):
        """Liste aller aktiven Giveaways des Servers."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        try:
            cursor.execute(f"SELECT gwID FROM active_giveaways WHERE guildID = {ctx.guild.id}")
            r = cursor.fetchall()
            if r is None:
                return await ctx.respond("❌ Ich habe auf diesem Server kein Giveaway gefunden.")
        except:
            return await ctx.respond("❌ Ich habe auf diesem Server kein Giveaway gefunden.")

        cursor.execute(f"SELECT prize, channelID, gwID, endtime FROM active_giveaways WHERE guildID = {ctx.guild.id}")
        result = cursor.fetchall()
        embed = discord.Embed(title="Alle Giveaways", description="Hier kannst du alle aktiven Giveaways auf diesem Server sehen.", color=discord.Color.purple())
        a = 0
        for i in result:
            channel = ctx.guild.get_channel(int(i[1]))
            if channel is not None:
                a += 1
                giveaway = await channel.fetch_message(int(i[2]))
                time_converted = datetime.datetime.fromtimestamp(int(i[3]))
                embed.add_field(name=f"{i[0]}", value=f"[Springe zum Giveaway]({giveaway.jump_url})\nVerbleibende Zeit: {discord_timestamp(time_converted, 'f')}({discord_timestamp(time_converted, 'R')})")
        await asyncio.sleep(1)
        if a >= 1:
            await ctx.send(embed=embed)
        if a < 1:
            return await ctx.send("❌ Ich habe auf diesem Server kein Giveaway gefunden.")
        mydb.close()

async def setup(bot):
    await bot.add_cog(giveaway(bot))