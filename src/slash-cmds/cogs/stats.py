import discord
from discord.ext import commands, tasks
from discord import app_commands
import typing
from googletrans import Translator
import datetime
import matplotlib.pyplot as plt
import os

async def getuserstats(self, art, member, guild):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            if art == "Textkanal":
                total1 = 0
                jahr1 = 0
                monat1 = 0
                woche1 = 0
                tag1 = 0
                await cursor.execute("SELECT anzahl, zeit FROM nachrichten WHERE guildID = (%s) AND userID = (%s)", (guild.id, member.id))
                r1 = await cursor.fetchall()
                if str(r1) != "()":
                    for datum in r1:
                        #für nachrichten
                        #jahr stats
                        total1 += int(datum[0])
                        if f".{discord.utils.utcnow().__format__('%Y')}" in str(datum[1]):
                            jahr1 += int(datum[0])
                        #monats stats
                        if f".{discord.utils.utcnow().__format__('%m')}." in str(datum[1]):
                            monat1 += int(datum[0])
                        #wochen stats
                        if int(discord.utils.utcnow().__format__('%d')) != 1:
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 1}." in str(datum[1]):
                                woche1 += int(datum[0])
                                
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 2}." in str(datum[1]):
                                woche1 += int(datum[0])
                        
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 3}." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 4}." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 5}." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 6}." in str(datum[1]):
                                woche1 += int(datum[0])
                        else:
                            if "31." in str(datum[1]):
                                woche1 += int(datum[0])
                                
                            if "30." in str(datum[1]):
                                woche1 += int(datum[0])
                        
                            if "29." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if "28." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if "27." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if "26." in str(datum[1]):
                                woche1 += int(datum[0])

                        #tages stats
                        if f"{discord.utils.utcnow().__format__('%d')}." in str(datum[1]):
                            tag1 += int(datum[0])
                            
                    liste = [total1, jahr1, monat1, woche1, tag1]
                    return liste
                liste = [0, 0, 0, 0, 0]
                return liste
            
            if art == "Sprachkanal":
                total1 = 0
                jahr1 = 0
                monat1 = 0
                woche1 = 0
                tag1 = 0
                await cursor.execute("SELECT anzahl, zeit FROM voice WHERE guildID = (%s) AND userID = (%s)", (guild.id, member.id))
                r1 = await cursor.fetchall()
                if str(r1) != "()":
                    for datum in r1:
                        #für nachrichten
                        #jahr stats
                        total1 += int(datum[0])
                        if f".{discord.utils.utcnow().__format__('%Y')}" in str(datum[1]):
                            jahr1 += int(datum[0])
                        #monats stats
                        if f".{discord.utils.utcnow().__format__('%m')}." in str(datum[1]):
                            monat1 += int(datum[0])
                        #wochen stats
                        if int(discord.utils.utcnow().__format__('%d')) != 1:
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 1}." in str(datum[1]):
                                woche1 += int(datum[0])
                                
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 2}." in str(datum[1]):
                                woche1 += int(datum[0])
                        
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 3}." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 4}." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 5}." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 6}." in str(datum[1]):
                                woche1 += int(datum[0])
                        else:
                            if "31." in str(datum[1]):
                                woche1 += int(datum[0])
                                
                            if "30." in str(datum[1]):
                                woche1 += int(datum[0])
                        
                            if "29." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if "28." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if "27." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if "26." in str(datum[1]):
                                woche1 += int(datum[0])

                        #tages stats
                        if f"{discord.utils.utcnow().__format__('%d')}." in str(datum[1]):
                            tag1 += int(datum[0])
                            
                    liste = [total1, jahr1, monat1, woche1, tag1]
                    return liste
                liste = [0, 0, 0, 0, 0]
                return liste

async def getuserslb(self, art, user, guild):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            if art == "Textkanal":
                await cursor.execute("SELECT channelID, anzahl FROM nachrichten WHERE guildID = (%s) AND userID = (%s)", (guild.id, user.id))
                result = await cursor.fetchall()
                if str(result) != "()":
                    leaderboard = {}
                    for data in result:
                        channel = guild.get_channel(int(data[0]))
                        if channel != None:
                            try:
                                leaderboard[int(data[0])] += int(data[1])
                            except:
                                leaderboard[int(data[0])] = int(data[1])
                                
                    s_l = sorted(leaderboard.items(), key=lambda kv: kv[1], reverse=True)
                    return s_l
                return None
                    
            if art == "Sprachkanal":
                await cursor.execute("SELECT channelID, anzahl FROM voice WHERE guildID = (%s) AND userID = (%s)", (guild.id, user.id))
                result = await cursor.fetchall()
                if str(result) != "()":
                    leaderboard = {}
                    for data in result:
                        channel = guild.get_channel(int(data[0]))
                        if channel != None:
                            try:
                                leaderboard[int(data[0])] += int(data[1])
                            except:
                                leaderboard[int(data[0])] = int(data[1])
                    s_l = sorted(leaderboard.items(), key=lambda kv: kv[1], reverse=True)
                    return s_l
                return None

async def getchannelstats(self, art, channel, guild):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            if art == "Textkanal":
                total1 = 0
                jahr1 = 0
                monat1 = 0
                woche1 = 0
                tag1 = 0
                await cursor.execute("SELECT anzahl, zeit FROM nachrichten WHERE guildID = (%s) AND channelID = (%s)", (guild.id, channel.id))
                r1 = await cursor.fetchall()
                if str(r1) != "()":
                    for datum in r1:
                        #für nachrichten
                        #jahr stats
                        total1 += int(datum[0])
                        if f".{discord.utils.utcnow().__format__('%Y')}" in str(datum[1]):
                            jahr1 += int(datum[0])
                        #monats stats
                        if f".{discord.utils.utcnow().__format__('%m')}." in str(datum[1]):
                            monat1 += int(datum[0])
                        #wochen stats
                        if f"{discord.utils.utcnow().__format__('%d')}." in str(datum[1]):
                            woche1 += int(datum[0])
                        
                        if int(discord.utils.utcnow().__format__('%d')) != 1:
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 1}." in str(datum[1]):
                                woche1 += int(datum[0])
                                
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 2}." in str(datum[1]):
                                woche1 += int(datum[0])
                        
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 3}." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 4}." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 5}." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 6}." in str(datum[1]):
                                woche1 += int(datum[0])
                        else:
                            if "31." in str(datum[1]):
                                woche1 += int(datum[0])
                                
                            if "30." in str(datum[1]):
                                woche1 += int(datum[0])
                        
                            if "29." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if "28." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if "27." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if "26." in str(datum[1]):
                                woche1 += int(datum[0])

                        #tages stats
                        if f"{discord.utils.utcnow().__format__('%d')}." in str(datum[1]):
                            tag1 += int(datum[0])
                            
                    liste = [total1, jahr1, monat1, woche1, tag1]
                    return liste
                liste = [0, 0, 0, 0, 0]
                return liste
            
            if art == "Sprachkanal":
                total1 = 0
                jahr1 = 0
                monat1 = 0
                woche1 = 0
                tag1 = 0
                await cursor.execute("SELECT anzahl, zeit FROM voice WHERE guildID = (%s) AND channelID = (%s)", (guild.id, channel.id))
                r1 = await cursor.fetchall()
                if str(r1) != "()":
                    for datum in r1:
                        #für nachrichten
                        #jahr stats
                        total1 += int(datum[0])
                        if f".{discord.utils.utcnow().__format__('%Y')}" in str(datum[1]):
                            jahr1 += int(datum[0])
                        #monats stats
                        if f".{discord.utils.utcnow().__format__('%m')}." in str(datum[1]):
                            monat1 += int(datum[0])
                        #wochen stats
                        if f"{discord.utils.utcnow().__format__('%d')}." in str(datum[1]):
                            woche1 += int(datum[0])
                            
                        if int(discord.utils.utcnow().__format__('%d')) != 1:
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 1}." in str(datum[1]):
                                woche1 += int(datum[0])
                                
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 2}." in str(datum[1]):
                                woche1 += int(datum[0])
                        
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 3}." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 4}." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 5}." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if f"{int(discord.utils.utcnow().__format__('%d')) - 6}." in str(datum[1]):
                                woche1 += int(datum[0])
                        else:
                            if "31." in str(datum[1]):
                                woche1 += int(datum[0])
                                
                            if "30." in str(datum[1]):
                                woche1 += int(datum[0])
                        
                            if "29." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if "28." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if "27." in str(datum[1]):
                                woche1 += int(datum[0])
                            
                            if "26." in str(datum[1]):
                                woche1 += int(datum[0])
                            

                        #tages stats
                        if f"{discord.utils.utcnow().__format__('%d')}." in str(datum[1]):
                            tag1 += int(datum[0])
                            
                    liste = [total1, jahr1, monat1, woche1, tag1]
                    return liste
                liste = [0, 0, 0, 0, 0]
                return liste

async def getchannelslb(self, art, channel, guild):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            if art == "Textkanal":
                await cursor.execute("SELECT userID, anzahl FROM nachrichten WHERE guildID = (%s) AND channelID = (%s)", (guild.id, channel.id))
                result = await cursor.fetchall()
                if str(result) != "()":
                    leaderboard = {}
                    for data in result:
                        mitglied = guild.get_member(int(data[0]))
                        if mitglied != None:
                            try:
                                leaderboard[int(data[0])] += int(data[1])
                            except:
                                leaderboard[int(data[0])] = int(data[1])
                                
                    s_l = sorted(leaderboard.items(), key=lambda kv: kv[1], reverse=True)
                    return s_l
                return None
                    
            if art == "Sprachkanal":
                await cursor.execute("SELECT userID, anzahl FROM voice WHERE guildID = (%s) AND channelID = (%s)", (guild.id, channel.id))
                result = await cursor.fetchall()
                if str(result) != "()":
                    leaderboard = {}
                    for data in result:
                        mitglied = guild.get_member(int(data[0]))
                        if mitglied != None:
                            try:
                                leaderboard[int(data[0])] += int(data[1])
                            except:
                                leaderboard[int(data[0])] = int(data[1])
                    s_l = sorted(leaderboard.items(), key=lambda kv: kv[1], reverse=True)
                    return s_l
                return None
            
async def getservernachrichtenstats(self, art, guild):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            if art == "Mitglieder":
                await cursor.execute("SELECT userID, anzahl FROM nachrichten WHERE guildID = (%s)", (guild.id))
                result = await cursor.fetchall()
                if str(result) != "()":
                    leaderboard = {}
                    for data in result:
                        mitglied = guild.get_member(int(data[0]))
                        if mitglied != None:
                            try:
                                leaderboard[int(data[0])] += int(data[1])
                            except:
                                leaderboard[int(data[0])] = int(data[1])
                                
                    s_l = sorted(leaderboard.items(), key=lambda kv: kv[1], reverse=True)
                    return s_l
                return None
            if art == "Kanäle":
                await cursor.execute("SELECT channelID, anzahl FROM nachrichten WHERE guildID = (%s)", (guild.id))
                result = await cursor.fetchall()
                if str(result) != "()":
                    leaderboard = {}
                    for data in result:
                        mitglied = guild.get_channel(int(data[0]))
                        if mitglied != None:
                            try:
                                leaderboard[int(data[0])] += int(data[1])
                            except:
                                leaderboard[int(data[0])] = int(data[1])
                                
                    s_l = sorted(leaderboard.items(), key=lambda kv: kv[1], reverse=True)
                    return s_l
                return None

async def getservervoicestats(self, art, guild):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            if art == "Mitglieder":
                await cursor.execute("SELECT userID, anzahl FROM voice WHERE guildID = (%s)", (guild.id))
                result = await cursor.fetchall()
                if str(result) != "()":
                    leaderboard = {}
                    for data in result:
                        mitglied = guild.get_member(int(data[0]))
                        if mitglied != None:
                            try:
                                leaderboard[int(data[0])] += int(data[1])
                            except:
                                leaderboard[int(data[0])] = int(data[1])
                                
                    s_l = sorted(leaderboard.items(), key=lambda kv: kv[1], reverse=True)
                    return s_l
                return None
            if art == "Kanäle":
                await cursor.execute("SELECT channelID, anzahl FROM voice WHERE guildID = (%s)", (guild.id))
                result = await cursor.fetchall()
                if str(result) != "()":
                    leaderboard = {}
                    for data in result:
                        mitglied = guild.get_channel(int(data[0]))
                        if mitglied != None:
                            try:
                                leaderboard[int(data[0])] += int(data[1])
                            except:
                                leaderboard[int(data[0])] = int(data[1])
                                
                    s_l = sorted(leaderboard.items(), key=lambda kv: kv[1], reverse=True)
                    return s_l
                return None
            
class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = dict()
    
    def cog_load(self):
        self.myLoop.start()

    def cog_unload(self):
        self.myLoop.cancel()

    #Voice Stats#
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT channelID FROM stats_blacklist WHERE guildID = (%s)", (member.guild.id))
                blacklist = await cursor.fetchall()
                if blacklist != None or str(blacklist) != "()":
                    for id in blacklist:
                        if before.channel:
                            if before.channel.id == int(id[0]):
                                return
                        if after.channel:
                            if after.channel.id == int(id[0]):
                                return
        if not before.channel and after.channel:
            self.data[member.id] = member.guild.id
        elif before.channel and not after.channel and member.id in self.data:
            del self.data[member.id]

    @tasks.loop(minutes=1)
    async def myLoop(self):
        try:
            for userid in list(self.data):
                guild = self.bot.get_guild(int(self.data.get(userid)))
                user = guild.get_member(int(userid))
                channelid = 0
                for voicechannel in guild.voice_channels:
                    if user in voicechannel.members:
                        channelid += int(voicechannel.id)
                channel = guild.get_channel(channelid)
                if channel is None:
                    pass
                async with self.bot.pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute("SELECT channelID FROM stats_blacklist WHERE guildID = (%s)", (guild.id))
                        blacklist = await cursor.fetchall()
                        if blacklist != None or str(blacklist) != "()":
                            for id in blacklist:
                                if channel.id == int(id[0]):
                                    return
                        await cursor.execute("SELECT anzahl FROM voice WHERE guildID = (%s) AND userID = (%s) AND zeit = (%s) AND channelID = (%s)", (guild.id, user.id, str(discord.utils.utcnow().__format__('%d.%m.%Y')), channel.id))
                        result = await cursor.fetchone()
                        if result is None:
                            return await cursor.execute("INSERT INTO voice(userID, guildID, zeit, anzahl, channelID) VALUES(%s, %s, %s, %s, %s)", (user.id, guild.id, str(discord.utils.utcnow().__format__('%d.%m.%Y')), 1, channel.id))
                        await cursor.execute("UPDATE voice SET anzahl = (%s) WHERE guildID = (%s) AND userID = (%s) AND zeit = (%s) AND channelID = (%s)", (result[0] + 1, guild.id, user.id, str(discord.utils.utcnow().__format__('%d.%m.%Y')), channel.id))
        except:
            pass
    
    
    #Nachrichten Stats#
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot:
            return
        if msg.guild != None:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelID FROM stats_blacklist WHERE guildID = (%s)", (msg.guild.id))
                    blacklist = await cursor.fetchall()
                    if blacklist != None or str(blacklist) != "()":
                        for id in blacklist:
                            if msg.channel.id == int(id[0]):
                                return
                    await cursor.execute("SELECT anzahl FROM nachrichten WHERE guildID = (%s) AND userID = (%s) AND zeit = (%s) AND channelID = (%s)", (msg.guild.id, msg.author.id, str(discord.utils.utcnow().__format__('%d.%m.%Y')), msg.channel.id))
                    result = await cursor.fetchone()
                    if result is None:
                        return await cursor.execute("INSERT INTO nachrichten(userID, guildID, zeit, anzahl, channelID) VALUES(%s, %s, %s, %s, %s)", (msg.author.id, msg.guild.id, str(discord.utils.utcnow().__format__('%d.%m.%Y')), 1, msg.channel.id))
                    await cursor.execute("UPDATE nachrichten SET anzahl = (%s) WHERE guildID = (%s) AND userID = (%s) AND zeit = (%s) AND channelID = (%s)", (result[0] + 1, msg.guild.id, msg.author.id, str(discord.utils.utcnow().__format__('%d.%m.%Y')), msg.channel.id))
    
    stats = app_commands.Group(name='stats', description='Verwalte Stats.')
    
    @stats.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def anzeigen(self, interaction: discord.Interaction, member: discord.Member=None, textkanal: discord.TextChannel=None, sprachkanal: discord.VoiceChannel=None):
        """Zeigt Stats für Member und Kanäle."""
        mydate = datetime.datetime.now()
        translator = Translator()
        translation = translator.translate(mydate.strftime("%B") , dest="de")
        monat = translation.text
        
        if member == None and textkanal == None and sprachkanal == None:
            return await interaction.response.send_message("**❌ Bitte gib beim nächsten Male an für welchen Kanal oder für welchen Member du die Stats einsehen willst.**", ephemeral=True)
        if member != None and textkanal != None or member != None and sprachkanal != None or textkanal != None and sprachkanal != None:
            return await interaction.response.send_message("**❌ Du kannst dich nur für eines entscheiden. Entweder für die Stats eines Members oder für die Stats eines Kanals.**", ephemeral=True)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if member != None:
                    stats1 = await getuserstats(self, "Textkanal", member, interaction.guild)
                    stats2 = await getuserstats(self, "Sprachkanal", member, interaction.guild)
                    text1 = ""
                    text2 = ""
                    channeluserstats1 = await getuserslb(self, "Textkanal", member, interaction.guild)
                    try:
                        a = 0
                        for data in channeluserstats1:
                            channel = interaction.guild.get_channel(int(data[0]))
                            if channel != None:
                                if a == 5:
                                    break
                                a += 1
                                text1 += f"> {channel.mention}: {data[1]} {'Nachrichten' if int(data[1]) > 1 else 'Nachricht'}\n"
                    except:
                        text1 += "Keine Daten"
                    
                    try:
                        b = 0
                        channeluserstats2 = await getuserslb(self, "Sprachkanal", member, interaction.guild)
                        for data in channeluserstats2:
                            channel = interaction.guild.get_channel(int(data[0]))
                            if channel != None:
                                if b == 5:
                                    break
                                b += 1
                                text2 += f"> {channel.mention}: {data[1]} {'Minuten' if int(data[1]) > 1 else 'Minute'}\n"
                    except:
                        text2 += "Keine Daten"
                    
                    embed = discord.Embed(colour=member.color, title=f"<:stats:944569387615125545> Statistiken von {member.name}", description=f"""
<:textchannel:997093466473508874> **Nachrichten Stats:**
> Insgesammt: {stats1[0]} Nachrichten
> Jahr {discord.utils.utcnow().__format__('%Y')}: {stats1[1]} Nachrichten
> Monat {monat}: {stats1[2]} Nachrichten
> Letzten 7 Tage: {stats1[3]} Nachrichten
> Tag: {stats1[4]} Nachrichten

<:textchannel:997093466473508874> **Aktivste Kanäle des Nutzers:**
{text1}


<:voicechannel:997093527391580200> **Sprachkanal Stats:**
> Insgesammt: {stats2[0]} Minuten
> Jahr: {stats2[1]} Minuten
> Monat: {stats2[2]} Minuten
> Letzten 7 Tage: {stats2[3]} Minuten
> Tag: {stats2[4]} Minuten

<:voicechannel:997093527391580200> **Aktivste Sprachkanäle des Nutzers:**
{text2}""")
                    embed.set_thumbnail(url=member.avatar)
                    return await interaction.response.send_message(embed=embed)
                
                
                if textkanal != None:
                    text = ""
                    channeluserstats = await getchannelslb(self, "Textkanal", textkanal, interaction.guild)
                    try:
                        a = 0
                        for data in channeluserstats:
                            mitglied = interaction.guild.get_member(int(data[0]))
                            if mitglied != None:
                                if a == 5:
                                    break
                                a += 1
                                text += f"> {mitglied.mention}: {data[1]} {'Nachrichten' if int(data[1]) > 1 else 'Nachricht'}\n"
                    except:
                        text += "Keine Daten"
                        
                    stats = await getchannelstats(self, "Textkanal", textkanal, interaction.guild)
                    embed = discord.Embed(colour=discord.Colour.green(), title=f"<:stats:944569387615125545> Statistiken von {textkanal.name}", description=f"""
<:textchannel:997093466473508874> **Nachrichten Stats:**
> Insgesammt: {stats[0]} Nachrichten
> Jahr {discord.utils.utcnow().__format__('%Y')}: {stats[1]} Nachrichten
> Monat {monat}: {stats[2]} Nachrichten
> Letzten 7 Tage: {stats[3]} Nachrichten
> Tag: {stats[4]} Nachrichten

<:textchannel:997093466473508874> **Aktivste Nutzer des Kanals:**
{text}""")
                    embed.set_thumbnail(url=interaction.guild.icon)
                    return await interaction.response.send_message(embed=embed)
                
                if sprachkanal != None:
                    text = ""
                    channeluserstats = await getchannelslb(self, "Sprachkanal", sprachkanal, interaction.guild)
                    try:
                        a = 0
                        for data in channeluserstats:
                            mitglied = interaction.guild.get_member(int(data[0]))
                            if mitglied != None:
                                if a == 5:
                                    break
                                a += 1
                                text += f"> {mitglied.mention}: {data[1]} {'Nachrichten' if int(data[1]) > 1 else 'Nachricht'}\n"
                    except:
                        text += "Keine Daten"
                        
                    stats = await getchannelstats(self, "Sprachkanal", sprachkanal, interaction.guild)
                    embed = discord.Embed(colour=discord.Colour.green(), title=f"<:stats:944569387615125545> Statistiken von {sprachkanal.name}", description=f"""
<:voicechannel:997093527391580200> **Aktivität im Sprachkanal:**
> Insgesammt: {stats[0]} Minuten
> Jahr {discord.utils.utcnow().__format__('%Y')}: {stats[1]} Minuten
> Monat {monat}: {stats[2]} Minuten
> Letzten 7 Tage: {stats[3]} Minuten
> Tag: {stats[4]} Minuten

<:voicechannel:997093527391580200> **Aktivste Nutzer des Kanals:**
{text}""")
                    embed.set_thumbnail(url=interaction.guild.icon)
                    return await interaction.response.send_message(embed=embed)        
                
    @stats.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def blacklist(self, interaction: discord.Interaction, kanal: discord.TextChannel):
        """Setze Kanäle auf die Blacklist für Nachrichten."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT channelID FROM stats_blacklist WHERE guildID = (%s) AND channelID = (%s)", (interaction.guild.id, kanal.id))
                result = await cursor.fetchone()
                if result == None:
                    await cursor.execute("INSERT INTO stats_blacklist(guildID, channelID) VALUES(%s, %s)", (interaction.guild.id, kanal.id))
                    return await interaction.response.send_message(f"**✅ {kanal.mention} ist nun auf der Blacklist.**")
                await cursor.execute("DELETE FROM stats_blacklist WHERE guildID = (%s) AND channelID = (%s)", (interaction.guild.id, kanal.id))
                return await interaction.response.send_message(f"**✅ {kanal.mention} ist nun nicht mehr auf der Blacklist.**")
    
    @stats.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def reset(self, interaction: discord.Interaction, bestätigung: typing.Literal["Ich verstehe dass diese Aktion unumkehrbar ist und dadurch alle Stats dieses Server gelöscht werden."]):
        """Setze alle Stats auf 0 zurück."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM nachrichten WHERE guildID = (%s)", (interaction.guild.id))
                await interaction.response.send_message("**✅ Alle Stats dieses Servers wurden gelöscht.**")
    
    @stats.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def top(self, interaction: discord.Interaction, art: typing.Literal["Mitglieder", "Kanäle"]):
        """Lass dir die besten Stats dieses Servers anzeigen."""
        await interaction.response.send_message("**⚙️ Ich generiere die Embeds und die Graphen. Einen kleinen Moment bitte.**", ephemeral=True)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if art == "Mitglieder":
                    ###
                    
                    liste1 = []
                    liste2 = []
                    legend = []
                    tod = datetime.datetime.now()
                    for i in range(14):
                        d = datetime.timedelta(days=i)
                        a = tod - d
                        liste1.append(f"{a.strftime('%b')} {int(a.__format__('%d'))}")
                        
                        await cursor.execute("SELECT anzahl FROM nachrichten WHERE guildID = (%s) AND zeit = (%s)", (interaction.guild.id, a.strftime(f"%d.%m.%Y")))
                        result = await cursor.fetchall()
                        if result != ():
                            anzahl = 0
                            for stat in result:
                                anzahl += int(stat[0])
                            liste2.append(anzahl)
                        else:
                            liste2.append(0)

                    #plt.plot(liste1, liste2, color="#0a0a0d", marker=".")

                    plt.xlabel("Datum")
                    plt.ylabel("Anzahl")
                    plt.title("14 Tage Nachrichten Stats der aktivsten Nutzer")

                    text = ""
                    b = await getservernachrichtenstats(self, "Mitglieder", interaction.guild)
                    text2 = ""
                    c = await getservervoicestats(self, "Mitglieder", interaction.guild)
                    try:
                        a = 0
                        for data in b:
                            l = []
                            mitglied = interaction.guild.get_member(int(data[0]))
                            if mitglied != None:
                                if a == 5:
                                    break
                                a += 1
                                text += f"> {mitglied.mention}: {data[1]} {'Nachrichten' if int(data[1]) > 1 else 'Nachricht'}\n"
                                legend.append(mitglied.name)
                                
                                for i in range(14):
                                    d2 = datetime.timedelta(days=i)
                                    ab = tod - d2
                                    
                                    
                                    await cursor.execute("SELECT anzahl FROM nachrichten WHERE guildID = (%s) AND zeit = (%s) AND userID = (%s)", (interaction.guild.id, ab.strftime(f"%d.%m.%Y"), mitglied.id))
                                    result = await cursor.fetchall()
                                    if result != ():
                                        anzahl = 0
                                        for stat in result:
                                            anzahl += int(stat[0])
                                        l.append(anzahl)
                                    else:
                                        l.append(0)
                            plt.plot(liste1, l)
                                
                    except:
                        text += f"Keine Daten"
                    
                    try:
                        a = 0
                        for data in c:
                            mitglied = interaction.guild.get_member(int(data[0]))
                            if mitglied != None:
                                if a == 5:
                                    break
                                a += 1
                                text2 += f"> {mitglied.mention}: {data[1]} {'Minuten' if int(data[1]) > 1 else 'Minute'}\n"
                    except:
                        text2 += "Keine Daten"
                        
                    plt.legend(legend)
                    plt.xticks(rotation=45)
                    plt.savefig("stats.png")
                    plt.close()
                    embed = discord.Embed(colour=discord.Colour.green(), title=f"<:stats:944569387615125545> Statistiken der aktivsten {art}", description=f"""
<:textchannel:997093466473508874> **Aktivste Nutzer in Textkanälen:**
{text}

<:voicechannel:997093527391580200> **Aktivste Nutzer in Sprachkanälen:**
{text2}""")
                    embed.set_thumbnail(url=interaction.guild.icon)
                    embed.set_image(url="attachment://stats.png")
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    
                    file = discord.File("stats.png", filename="stats.png")
                    os.remove("stats.png")
                    return await interaction.channel.send(file=file, embed=embed)
                
                if art == "Kanäle":
                    liste1 = []
                    liste2 = []
                    legend = []
                    tod = datetime.datetime.now()
                    for i in range(14):
                        d = datetime.timedelta(days=i)
                        a = tod - d
                        liste1.append(f"{a.strftime('%b')} {int(a.__format__('%d'))}")
                        
                        await cursor.execute("SELECT anzahl FROM voice WHERE guildID = (%s) AND zeit = (%s)", (interaction.guild.id, a.strftime(f"%d.%m.%Y")))
                        result = await cursor.fetchall()
                        if result != ():
                            anzahl = 0
                            for stat in result:
                                anzahl += int(stat[0])
                            liste2.append(anzahl)
                        else:
                            liste2.append(0)

                    #plt.plot(liste1, liste2, color="#0a0a0d", marker=".")

                    plt.xlabel("Datum")
                    plt.ylabel("Anzahl")
                    plt.title("14 Tage Nachrichten Stats der aktivsten Kanäle")
                    
                    text = ""
                    b = await getservernachrichtenstats(self, "Kanäle", interaction.guild)
                    text2 = ""
                    c = await getservervoicestats(self, "Kanäle", interaction.guild)
                    try:
                        a = 0
                        for data in b:
                            l = []
                            mitglied = interaction.guild.get_channel(int(data[0]))
                            if mitglied != None:
                                if a == 5:
                                    break
                                a += 1
                                text += f"> {mitglied.mention}: {data[1]} {'Nachrichten' if int(data[1]) > 1 else 'Nachricht'}\n"
                                legend.append(mitglied.name)
                                
                                for i in range(14):
                                    d2 = datetime.timedelta(days=i)
                                    ab = tod - d2
                                    
                                    
                                    await cursor.execute("SELECT anzahl FROM nachrichten WHERE guildID = (%s) AND zeit = (%s) AND channelID = (%s)", (interaction.guild.id, ab.strftime(f"%d.%m.%Y"), mitglied.id))
                                    result = await cursor.fetchall()
                                    if result != ():
                                        anzahl = 0
                                        for stat in result:
                                            anzahl += int(stat[0])
                                        l.append(anzahl)
                                    else:
                                        l.append(0)
                            plt.plot(liste1, l)
                                
                    except:
                        text += f"Keine Daten"
                    
                    try:
                        a = 0
                        for data in c:
                            mitglied = interaction.guild.get_channel(int(data[0]))
                            if mitglied != None:
                                if a == 5:
                                    break
                                a += 1
                                text2 += f"> {mitglied.mention}: {data[1]} {'Minuten' if int(data[1]) > 1 else 'Minute'}\n"
                    except:
                        text2 += "Keine Daten"
                        
                    plt.legend(legend)
                    plt.xticks(rotation=45)
                    plt.savefig("stats.png")
                    plt.close()
                    embed = discord.Embed(colour=discord.Colour.green(), title=f"<:stats:944569387615125545> Statistiken der aktivsten {art}", description=f"""
<:textchannel:997093466473508874> **Aktivste Textkanäle:**
{text}

<:voicechannel:997093527391580200> **Aktivste Sprachkanäle:**
{text2}""")
                    embed.set_thumbnail(url=interaction.guild.icon)
                    embed.set_image(url="attachment://stats.png")
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    
                    file = discord.File("stats.png", filename="stats.png")
                    os.remove("stats.png")
                    return await interaction.channel.send(file=file, embed=embed)

                    
async def setup(bot):
    await bot.add_cog(Stats(bot))