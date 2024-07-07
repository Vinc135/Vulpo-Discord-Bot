import discord
from discord.ext import commands, tasks
from utils.utils import convert, voicetime_to_xp
from discord import app_commands
import typing
from googletrans import Translator
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
from utils.utils import getcolour, haspremium_forserver
from utils.MongoDB import getMongoDataBase
import time
import mplcyberpunk
import json
import math
import numpy

async def generateStatsImage(xWerte, yWerteMSG, yWerteTALK):
    plt.figure(figsize=(7.5, 3.5))
    plt.style.use("./stats.mplstyle")
    plt.plot(xWerte, yWerteMSG, marker="o", label="Nachrichten")
    plt.plot(xWerte, yWerteTALK, marker="o", label="Sprachzeit")
    mplcyberpunk.make_lines_glow()
    
    locs, labels = plt.yticks()
    dloc = math.ceil(locs[1] - locs[0])
    dloc_int = int(dloc)
    new_yticks = numpy.arange(0, locs.max(), dloc_int, dtype=int)
    plt.yticks(new_yticks)
    
    for i, label in enumerate(plt.gca().get_xticklabels()):
        if i % 2 == 0:
            label.set_visible(False)
    
    labels = ["Nachrichten", "Sprachzeit"]
    
    plt.legend(labels, loc="upper center", bbox_to_anchor=(0.5, 1.1))
    
    plt.savefig("stats.png", bbox_inches='tight')
    plt.close()

async def generateServerStatsImage(xWerte, yWerteMSG, yWerteTALK):
    plt.figure(figsize=(7.5, 3.5))
    plt.style.use("./stats.mplstyle")
    plt.plot(xWerte, yWerteMSG, marker="o", label="Nachrichten")
    plt.plot(xWerte, yWerteTALK, marker="o", label="Sprachzeit")
    mplcyberpunk.make_lines_glow()
    
    locs, labels = plt.yticks()
    dloc = math.ceil(locs[1] - locs[0])
    dloc_int = int(dloc)
    new_yticks = numpy.arange(0, locs.max(), dloc_int, dtype=int)
    plt.yticks(new_yticks)
    
    for i, label in enumerate(plt.gca().get_xticklabels()):
        if i % 2 == 0:
            label.set_visible(False)
    
    labels = ["Nachrichten", "Sprachzeit"]
    
    plt.legend(labels, loc="upper center", bbox_to_anchor=(0.5, 1.1))
    
    plt.savefig("ServerStats.png", bbox_inches='tight')
    plt.close()


    
async def get_user_data(bot, user_id):
    user_data = {}

    # Aktuelles Datum und Zeit
    current_datetime = datetime.now()

    # Letzte 14 Tage
    last_14_days = current_datetime - timedelta(days=14)
    
    db = getMongoDataBase()

    # Anzahl der Nachrichten des Benutzers in den letzten 14 Tagen abrufen
    
    message_count_last_14_days = db['nachrichten'].count_documents({"userID": user_id, "datum": {"$gte": last_14_days}})
    
    user_data['message_count_last_14_days'] = message_count_last_14_days
    
    server_ranks = db['nachrichten'].aggregate([
        {"$match": {"userID": user_id, "datum": {"$gte": last_14_days}}},
        {"$group": {"_id": "$guildID", "message_count": {"$count": {}}}},
        {"$sort": {"message_count": -1}}
    ])

    user_server_ranks = {}
    for idx, rank in enumerate(server_ranks, start=1):
        user_server_ranks[rank['guildID']] = idx

    user_data['server_ranks_last_14_days'] = user_server_ranks

    return user_data


async def bild_server_stats(bot, guild_id):
    stats = []
    daten = []
    all_messages = {}
    statsvoice = []
    
    db = getMongoDataBase()
    
    for i in range(14):
        tag = (datetime.now() - timedelta(days=13-i)).strftime('%Y-%m-%d')
        tag_voice = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
        tag_format = (datetime.now() - timedelta(days=13-i)).strftime('%d.%m')
        daten.append(tag_format)  
        
        result = await db['nachrichten'].find_one({"guildID": guild_id, "datum": tag})
        
        if result is None:
            all_messages[tag] = 0
        else:
            json_data = json.loads(result["daten"])   
            total_messages = 0
            for user_data in json_data.values():
                for channel_count in user_data.values():
                    total_messages += channel_count
            all_messages[tag] = total_messages
            
        #VOICE

        result = await db['voice'].find({"guildID": guild_id, "zeit": tag_voice}).to_list(length=None)
        anzahl = 0
        
        for minuten in result:
            anzahl += minuten["anzahl"]
        statsvoice.append(anzahl)
        
    for entry in all_messages.values():
        stats.append(entry)     
    statsvoice = statsvoice[::-1]
    return daten, stats, statsvoice

async def get_server_stats(bot, guild_id):
            #TEXT
            
            db = getMongoDataBase()
            
            stats = {}
            alle_user_tages = {}
            alle_channel_letzte_7tage = {}
            alle_user_tages_voice = {}
            voice7 = 0
            voice30 = 0
            
            anzahl_letzte_7tage = 0
            anzahl_letzte_30tage = 0

            heute = datetime.now().strftime('%Y-%m-%d')
            
            for i in range(31):
                tag = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                tag_voice = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
                
                result = await db['nachrichten'].find_one({"guildID": guild_id, "datum": tag})
                
                if result is None:
                    continue
                
                json_data = result["daten"]
                
                print (json_data)
                
                server_stats = json.loads(json_data)
                
                for user_id, user_data in server_stats.items():
                    for channel_id, channel_count in user_data.items():
                        if(i <= 6):
                            anzahl_letzte_7tage += channel_count
                        anzahl_letzte_30tage += channel_count
                        if tag == heute:
                            # Aktivster Nutzer des Tages
                            if user_id in alle_user_tages:
                                alle_user_tages[user_id] += channel_count
                            else:
                                alle_user_tages[user_id] = channel_count
                                
                            result = await db['voice'].find({"guildID": guild_id, "zeit": tag_voice}).to_list(length=None)
                                
                            for r in result:
                                user = r["userID"]
                                anzahl = r["anzahl"]
                                if user in alle_user_tages_voice:
                                    alle_user_tages_voice[user] += anzahl
                                else:
                                    alle_user_tages_voice[user] = anzahl
                            
                        # Top-Kanal der letzten 7 Tage
                        if channel_id in alle_channel_letzte_7tage:
                            alle_channel_letzte_7tage[channel_id] += channel_count
                        else:
                            alle_channel_letzte_7tage[channel_id] = channel_count
                #VOICE
            
                result = await db['voice'].find({"guildID": guild_id, "zeit": tag_voice}).to_list(length=None)
 
                for minuten in result:
                    if(i <= 6):
                        voice7 += int(minuten[0])
                    voice30 += int(minuten[0])
                    
            
            #MESSAGES
                           
            stats["<:v_chat:1119577968457568327> Nachrichten (7 Tage)"] = anzahl_letzte_7tage
            stats["<:v_chat:1119577968457568327> Nachrichten (30 Tage)"] = anzahl_letzte_30tage
            
            #CHANNEL
            
            msgs_channel = 0
            
            aktivster_channel = max(alle_channel_letzte_7tage.items(), key=lambda x: x[1])[0] if alle_channel_letzte_7tage else "Es gibt keinen aktivsten Kanal"   
            if aktivster_channel != "Es gibt keinen aktivsten Kanal":
                msgs_channel = alle_channel_letzte_7tage[aktivster_channel]
            
                stats["<:v_stats:1119583678083895346> Top Channel (7 Tage)"] = f"<#{aktivster_channel}> - {msgs_channel} Nachrichten"
            else:
                stats["<:v_stats:1119583678083895346> Top Channel (7 Tage)"] = f"{aktivster_channel} - {msgs_channel} Nachrichten"

            stats["<:v_stats:1119583678083895346> Voice Minuten (7 Tage)"] = f"{voice7} Minuten"
            stats["<:v_stats:1119583678083895346> Voice Minuten (30 Tage)"] = f"{voice30} Minuten"

            #USER
            
            msgs_user = 0
            talk_user = 0
            talk_msgs_user = 0
            
            aktivster_nutzer_voice_str = "Es gibt keinen aktivsten Nutzer"
            aktivster_nutzer_str = "Es gibt keinen aktivsten Nutzer"
            
            aktivster_nutzer_voice = max(alle_user_tages_voice.items(), key=lambda x: x[1])[0] if alle_user_tages_voice else "Es gibt keinen aktivsten Nutzer"
            aktivster_nutzer = max(alle_user_tages.items(), key=lambda x: x[1])[0] if alle_user_tages else "Es gibt keinen aktivsten Nutzer"
            if aktivster_nutzer != "Es gibt keinen aktivsten Nutzer":
                aktivster_nutzer_str = f"<@{aktivster_nutzer}>"
                msgs_user = alle_user_tages[aktivster_nutzer]
                talk_msgs_user = alle_user_tages_voice[aktivster_nutzer] if aktivster_nutzer in alle_user_tages_voice else "0"
            if aktivster_nutzer_voice != "Es gibt keinen aktivsten Nutzer":
                aktivster_nutzer_voice_str = f"<@{aktivster_nutzer_voice}>"
                talk_user = alle_user_tages_voice[aktivster_nutzer_voice]
            
            if(aktivster_nutzer_str != aktivster_nutzer_voice_str):
                stats["<:v_user:1119585450923929672> Aktivste Nutzer des Tages"] = f"{aktivster_nutzer_str} - {msgs_user} Nachrichten \n{aktivster_nutzer_voice_str} - {talk_user} Minuten"
            else:
                stats["<:v_user:1119585450923929672> Aktivste Nutzer des Tages"] = f"{aktivster_nutzer_str} - {msgs_user} Nachrichten, {talk_msgs_user} Minuten"
            
            return stats

async def bild_user_stats(bot, guild_id, user_id):
            stats = []
            daten = []
            all_messages = {}
            statsvoice = []

            db = getMongoDataBase()

            for i in range(14):
                tag = (datetime.now() - timedelta(days=13-i)).strftime('%Y-%m-%d')
                tag_voice = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')

                tag_format = (datetime.now() - timedelta(days=13-i)).strftime('%d.%m')
                daten.append(tag_format)
                
                result = await db['nachrichten'].find_one({"guildID": guild_id, "datum": tag})
                
                if result is None:
                    all_messages[tag] = 0
                else:
                    json_data = json.loads(result["daten"])
                    
                    total_messages = 0
                    for id, user_data in json_data.items():
                        if(id == str(user_id)):
                            for channel_count in user_data.values():
                                total_messages += channel_count
                    all_messages[tag] = total_messages
                    
                #VOICE
                result = await db["nachrichten"].find({"guildID": guild_id, "datum": tag, "userID": user_id}).to_list(length=None)
 
                anzahl = 0
 
                for minuten in result:
                    anzahl += minuten["anzahl"]
                statsvoice.append(anzahl)
            
            for entry in all_messages.values():
                stats.append(entry)
                
            statsvoice = statsvoice[::-1]
            
            return daten, stats, statsvoice


async def get_user_stats(bot, user_id, guild_id):
            #TEXT
            stats = {}
            voice7 = 0
            voice30 = 0
            all_users_msgs = {}
            all_users_talk = {}
            
            anzahl_letzte_7tage = 0
            anzahl_letzte_30tage = 0
            
            db = getMongoDataBase()
            
            for i in range(31):
                tag = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                tag_voice = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
                
                result = await db['nachrichten'].find_one({"guildID": guild_id, "datum": tag})
                
                if result is None:
                    continue
                
                server_stats = json.loads(result["daten"])
                
                for id, user_data in server_stats.items():
                    for channel_id, channel_count in user_data.items():
                        if(id == str(user_id)):
                            if(i <= 6):
                                anzahl_letzte_7tage += channel_count
                            anzahl_letzte_30tage += channel_count
                        if(id in all_users_msgs):
                            all_users_msgs[id] += channel_count
                        else:
                            all_users_msgs[id] = channel_count
                        
                                
                #VOICE
            
                result = await db['voice'].find({"guildID": guild_id, "zeit": tag_voice}).to_list(length=None)
 
                for user in result:
                    id = user[0]
                    if(user[0] == str(user_id)):
                        if(i <= 6):
                            voice7 += int(user[1])
                        voice30 += int(user[1])
                    
                    if(id in all_users_talk):
                        all_users_talk[id] += user[1]
                    else:
                        all_users_talk[id] = user[1]
                    
            
            #MESSAGES
                           
            stats["<:v_chat:1119577968457568327> Nachrichten (7 Tage)"] = anzahl_letzte_7tage
            stats["<:v_chat:1119577968457568327> Nachrichten (30 Tage)"] = anzahl_letzte_30tage

            stats["<:v_stats:1119583678083895346> Voice Minuten (7 Tage)"] = f"{voice7} Minuten"
            stats["<:v_stats:1119583678083895346> Voice Minuten (30 Tage)"] = f"{voice30} Minuten"
            
            #RANK
            
            rank_msg = ""
            
            sortedUsersMSGS = dict(sorted(all_users_msgs.items(), key=lambda item: item[1], reverse=True))
            sortedUsersTalk = dict(sorted(all_users_talk.items(), key=lambda item: item[1], reverse=True))
            if(str(user_id) in sortedUsersMSGS):
                MSGRank = list(sortedUsersMSGS.keys()).index(str(user_id))+1
                rank_msg = f"**#{MSGRank}** (Nachrichten)"
            else:
                rank_msg = f"**#{len(sortedUsersMSGS)+1}** (Nachrichten)"
            if(str(user_id) in sortedUsersTalk):
                MSGRank = list(sortedUsersTalk.keys()).index(str(user_id))+1
                rank_msg += f"\n\n**#{MSGRank}** (Sprachzeit)"
            else:
                rank_msg += f"\n\n**#{len(sortedUsersTalk)+1}** (Sprachzeit)"
            
            stats["<:v_stats:1119583678083895346> Server Rank"] = rank_msg
            
            return stats


async def update_all(self):
            result = await getMongoDataBase()["upstats"].find().to_list(length=None)
            for ergebnis in result:
                try:
                    guild = self.bot.get_guild(int(ergebnis[0]))
                    if guild:
                        kanal = guild.get_channel(int(ergebnis[1]))
                        if kanal:
                            online = 0
                            offline = 0
                            dnd = 0
                            idle = 0
                            bots = 0
                            for user in guild.members:
                                if str(user.status.name) == "online":
                                    online += 1
                                if str(user.status.name) == "dnd":
                                    dnd += 1
                                if str(user.status.name) == "idle":
                                    idle += 1
                                if str(user.status.name) == "offline":
                                    offline += 1
                                if user.bot:
                                    bots += 1
                            finaltext = ergebnis[2].replace("%usercount", str(guild.member_count)).replace("%notoffline", str(int(guild.member_count) - offline)).replace("%membercount", str(int(guild.member_count) - bots)).replace("%botcount", str(bots)).replace("%online", str(online)).replace("%dnd", str(dnd)).replace("%idle", str(idle)).replace("%offline", str(offline))
                            await kanal.edit(name=finaltext)
                except:
                    continue


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def cog_load(self):
        self.channel_update.start()
        
    def cog_unload(self):
        self.channel_update.cancel()
        
    @tasks.loop(minutes=10)
    async def channel_update(self):
        await update_all(self)
            
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
                db = getMongoDataBase()
        
                result = await db["voice"].find_one({"userID": member.id})

                if result != None:
                    if before.channel:
                        voice_leave_time = datetime.now().time().strftime('%H:%M:%S')
                        voice_join_time = result["zeit"]

                        calculate_time = (
                                datetime.strptime(voice_leave_time, '%H:%M:%S') - datetime.strptime(
                            voice_join_time, '%H:%M:%S'))
                        
                        string = f"{str(calculate_time)[0]}h {str(calculate_time)[2]}{str(calculate_time)[3]}m {str(calculate_time)[5]}{str(calculate_time)[6]}s"
                        time_in_seconds = convert(string)
                        if time_in_seconds == None:
                            return
                        time_in_minutes = round(time_in_seconds / 60)
                            
                        await db["voicedata"].delete_one({"userID": member.id})
                        if(time_in_minutes <= 1):
                            return
                        
                        result = await db["voice"].find_one({"userID": member.id, "guildID": member.guild.id, "zeit": str(discord.utils.utcnow().__format__('%d.%m.%Y')), "channelID": before.channel.id})
                        
                        if result is None:
                            await db["voice"].insert_one({"userID": member.id, "guildID": member.guild.id, "zeit": str(discord.utils.utcnow().__format__('%d.%m.%Y')), "anzahl": time_in_minutes, "channelID": before.channel.id})
                        else:
                            await db["voice"].update_one({"userID": member.id, "guildID": member.guild.id, "zeit": str(discord.utils.utcnow().__format__('%d.%m.%Y')), "channelID": before.channel.id}, {"$set": {"anzahl": result["anzahl"] + time_in_minutes}})
                            
                        await voicetime_to_xp(self, member, time_in_minutes, before)
                        
                        try:
                            result2 = await db["gewinnspiele"].find({"guildID": member.guild.id, "status": "Aktiv"}).to_list()
                            
                            if result2 == ():
                                return
                            for gewinnspiel in result2:
                                result = await db["gw_voice"].find_one({"userID": member.id, "guildID": member.guild.id, "gwID": gewinnspiel[0]})
                                if result == None:
                                    await db["gw_voice"].insert_one({"userID": member.id, "guildID": member.guild.id, "gwID": gewinnspiel[0], "anzahl": time_in_minutes})
                                else:
                                    await db["gw_voice"].update_one({"userID": member.id, "guildID": member.guild.id, "gwID": gewinnspiel[0]}, {"$set": {"anzahl": result["anzahl"] + time_in_minutes}})
                        except:
                            pass
                if after.channel:
                    new_voice_join_time = datetime.now().time().strftime('%H:%M:%S')
                    await db["voicedata"].insert_one({"time": new_voice_join_time, "userID": member.id})

    #Nachrichten Stats#

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild is None or msg.author.bot:
            return
        
        current_datetime = datetime.now().strftime('%Y-%m-%d')
        
        db = getMongoDataBase()
        
        result = await db["nachrichten"].find_one({"guildID": msg.guild.id, "datum": current_datetime})
                
        if result is None:
            initial_data = {
                str(msg.author.id): {
                    str(msg.channel.id): 1,
                }
            }
            json_data = json.dumps(initial_data)
            await db["nachrichten"].insert_one({"guildID": msg.guild.id, "datum": current_datetime, "daten": json_data})
        else:
            # Laden des vorhandenen JSON aus der Datenbank und Aktualisieren der Daten
            existing_json = json.loads(result["daten"])
            user_id = str(msg.author.id)
            channel_id = str(msg.channel.id)
            if user_id in existing_json:
                if channel_id in existing_json[user_id]:
                    existing_json[user_id][channel_id] += 1
                else:
                    existing_json[user_id][channel_id] = 1
            else:
                existing_json[user_id] = {channel_id: 1}
            
            updated_json = json.dumps(existing_json)
                    
        # Aktualisierten JSON in die Datenbank speichern
        await db["nachrichten"].update_one({"guildID": msg.guild.id, "datum": current_datetime}, {"$set": {"daten": updated_json}})
        
    stats = app_commands.Group(name='stats', description='Verwalte Stats.', guild_only=True)
    
    @stats.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def server(self, interaction: discord.Interaction):
        """Schau dir die Stats des Servers an."""
        
        await interaction.response.defer()
        
        server_stats = await get_server_stats(self.bot, interaction.guild.id)
        embed = discord.Embed(title=f"Stats für {interaction.guild.name}", color=await getcolour(self, interaction.user))
        for stat_name, stat_value in server_stats.items():
            if stat_name == "<:v_user:1119585450923929672> Aktivste Nutzer des Tages" or stat_name == "<:v_stats:1119583678083895346> Top Channel (7 Tage)":
                embed.add_field(name=f"{stat_name}", value=stat_value, inline=False)
            else:
                embed.add_field(name=stat_name, value=stat_value, inline=True)
        
        xWerte, yWerteMSG, yWerteTALK = await bild_server_stats(self.bot, interaction.guild.id)
        
        await generateServerStatsImage(xWerte, yWerteMSG, yWerteTALK)
        
        embed.set_image(url="attachment://ServerStats.png")       
        file = discord.File("ServerStats.png", filename="ServerStats.png")
        await interaction.followup.send(file=file, embed=embed)
        os.remove("ServerStats.png")

    @stats.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def user(self, interaction: discord.Interaction, user: discord.Member = None):
        """Schau dir die Stats eines Users an."""
        
        await interaction.response.defer()
        
        member = user
        if(member is None):
            member = interaction.user
        server_stats = await get_user_stats(self.bot, member.id, interaction.guild.id)
        embed = discord.Embed(title=f"Stats für {member}", color=await getcolour(self, interaction.user))
        for stat_name, stat_value in server_stats.items():
            embed.add_field(name=stat_name, value=stat_value, inline=False)
            #if stat_name == "<:v_stats:1119583678083895346> Voice Minuten (7 Tage)" or stat_name == "<:v_stats:1119583678083895346> Server Rank":
            #    embed.add_field(name=f"{stat_name}", value=stat_value, inline=False)
            #else:
            #    embed.add_field(name=stat_name, value=stat_value, inline=True)
        
        xWerte, yWerteMSG, yWerteTALK = await bild_user_stats(self.bot, interaction.guild.id, member.id)
        
        await generateStatsImage(xWerte, yWerteMSG, yWerteTALK)
        
        embed.set_image(url="attachment://stats.png")       
        file = discord.File("stats.png", filename="stats.png")
        await interaction.followup.send(file=file, embed=embed)
        os.remove("stats.png")

    @stats.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def blacklist(self, interaction: discord.Interaction, kanal: discord.TextChannel):
        """Setze Kanäle auf die Blacklist für Nachrichten."""
        
        await interaction.response.defer()
        
        #status = await haspremium_forserver(self, interaction.guild)
        #if status == False:
        #    return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Der Serverowner dieses Servers hat kein Premiumabo. Aus diesem Grund sind alle Befehle des Stats-Systems hier deaktiviert.**")
        
        db = getMongoDataBase()
        
        result = await db["stats_blacklist"].insert_one({"guildID": interaction.guild.id, "channelID": kanal.id})
        
        if result == None:
            await db["stats_blacklist"].insert_one({"guildID": interaction.guild.id, "channelID": kanal.id})
            return await interaction.followup.send(f"**<:v_haken:1119579684057907251> {kanal.mention} ist nun auf der Blacklist.**")
        
        await db["stats_blacklist"].delete_one({"guildID": interaction.guild.id, "channelID": kanal.id})
        return await interaction.followup.send(f"**<:v_haken:1119579684057907251> {kanal.mention} ist nun nicht mehr auf der Blacklist.**")
    
    @stats.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def reset(self, interaction: discord.Interaction, bestätigung: typing.Literal["Ich verstehe dass diese Aktion unumkehrbar ist und dadurch alle Stats dieses Server gelöscht werden."]):
        """Setze alle Stats auf 0 zurück."""
        
        await interaction.response.defer()
        
        #status = await haspremium_forserver(self, interaction.guild)
        #if status == False:
        #    return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Der Serverowner dieses Servers hat kein Premiumabo. Aus diesem Grund sind alle Befehle des Stats-Systems hier deaktiviert.**")
        
        getMongoDataBase()["nachrichten"].delete_many({"guildID": interaction.guild.id})
        
        await interaction.followup.send("**<:v_haken:1119579684057907251> Alle Stats dieses Servers wurden gelöscht.**")
    
#     @stats.command()
#     @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
#     async def top(self, interaction: discord.Interaction, art: typing.Literal["Mitglieder", "Kanäle"]):
#         """Lass dir die besten Stats dieses Servers anzeigen."""
#         await interaction.response.defer(ephemeral=True)
#         start = time.time()
#         status = await haspremium_forserver(self, interaction.guild)
#         if status == False:
#             return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Der Serverowner dieses Servers hat kein Premiumabo. Aus diesem Grund sind alle Befehle des Stats-Systems hier deaktiviert.**")
#         print(f"Zeit:  {time.time() - start}")
#         await interaction.followup.send("**<:v_einstellungen:1119578559086874636> Ich generiere die Embeds und die Graphen. Einen kleinen Moment bitte.**", ephemeral=True)
        
#         maxdays = 7
        
#         async with self.bot.pool.acquire() as conn:
#             async with conn.cursor() as cursor:
#                 #plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')
                
#                 if art == "Mitglieder":
#                     ###
                    
#                     liste1 = []
#                     liste2 = []
#                     legend = []
#                     tod = datetime.datetime.now()
                    
#                     startLoop = time.time()
#                     for i in range(maxdays):
#                         print(f"i: {i}")
#                         d = datetime.timedelta(days=maxdays-1-i)
#                         print(f"d: {d}")
#                         a = tod - d
#                         print(f"tod: {tod}")
#                         print(f"a: {a}")
#                         liste1.append(f"{a.strftime('%d.%m')}")
                        
#                         await cursor.execute("SELECT anzahl FROM nachrichten WHERE guildID = (%s) AND zeit = (%s)", (interaction.guild.id, a.strftime(f"%d.%m.%Y")))
#                         result = await cursor.fetchall()
#                         if result != ():
#                             anzahl = 0
#                             for stat in result:
#                                 anzahl += int(stat[0])
#                             liste2.append(anzahl)
#                         else:
#                             liste2.append(0)
#                     print(time.time() - startLoop)

#                     #plt.plot(liste1, liste2, color="#0a0a0d", marker=".")

#                     #plt.xlabel("Datum")
#                     #plt.ylabel("Anzahl")
#                     #plt.title("7 Tage Nachrichten Stats der aktivsten Nutzer")

#                     text = ""
#                     servermsgstats = time.time()
#                     b = await getservernachrichtenstats(self, "Mitglieder", interaction.guild)
#                     print(f"Servernachrichtenstats: {time.time() - servermsgstats}")
#                     text2 = ""
#                     servervoicestats = time.time()
#                     c = await getservervoicestats(self, "Mitglieder", interaction.guild)
#                     print(f"Serversprachstats: {time.time() - servervoicestats}")
#                     try:
#                         a = 0
#                         completeloopstart = time.time()
#                         print(f"b: {b}")
#                         for data in b:
#                             loopstart = time.time()
#                             print(f"data: {data}")
#                             l = []
#                             mitglied = interaction.guild.get_member(int(data[0]))
#                             if mitglied != None:
#                                 if a == 5:
#                                     break
#                                 a += 1
#                                 text += f"> {mitglied.mention}: {data[1]} {'Nachrichten' if int(data[1]) > 1 else 'Nachricht'}\n"
#                                 legend.append(mitglied.name)
                                
#                                 secondloopstart = time.time()
#                                 for i in range(maxdays):
#                                     d2 = datetime.timedelta(days=maxdays-1-i)
#                                     ab = tod - d2
                                    
#                                     dbstart = time.time()
#                                     await cursor.execute("SELECT anzahl FROM nachrichten WHERE guildID = (%s) AND zeit = (%s) AND userID = (%s)", (interaction.guild.id, ab.strftime(f"%d.%m.%Y"), mitglied.id))
#                                     print(f"dbend: {time.time() - dbstart}")
#                                     result = await cursor.fetchall()
#                                     if result != ():
#                                         anzahl = 0
#                                         for stat in result:
#                                             anzahl += int(stat[0])
#                                         l.append(anzahl)
#                                     else:
#                                         l.append(0)
#                                 print(f"secondloopend: {time.time() - secondloopstart}")
#                             plt.plot(liste1, l, marker="o")
                            
#                             print(f"LoopEnd {time.time() - loopstart}")
                        
#                         print(f"Completeloop: {time.time() - completeloopstart}")
                                
#                     except:
#                         text += f"Keine Daten"
                    
#                     try:
#                         a = 0
#                         for data in c:
#                             mitglied = interaction.guild.get_member(int(data[0]))
#                             if mitglied != None:
#                                 if a == 5:
#                                     break
#                                 a += 1
#                                 text2 += f"> {mitglied.mention}: {data[1]} {'Minuten' if int(data[1]) > 1 else 'Minute'}\n"
#                     except:
#                         text2 += "Keine Daten"
                       
                    
#                     embed = discord.Embed(colour=await getcolour(self, interaction.user), title=f"<:v_stats:1119583678083895346> Statistiken der aktivsten {art}", description=f"""
# <:v_chat:1119577968457568327> **Aktivste Nutzer in Textkanälen:**
# {text}

# <:v_mikrofon:1119581634216329266> **Aktivste Nutzer in Sprachkanälen:**
# {text2}""")
#                     embed.set_thumbnail(url=interaction.guild.icon)
#                     embed.set_image(url="attachment://stats.png")
#                     embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    
#                     file = discord.File("stats.png", filename="stats.png")
#                     os.remove("stats.png")
#                     return await interaction.channel.send(file=file, embed=embed)
                
                #if art == "Kanäle":
                #    liste1 = []
                #    liste2 = []
                #    legend = []
                #    tod = datetime.datetime.now()
                #    for i in range(0, maxdays):
                #        d = datetime.timedelta(days=maxdays-i)
                #        a = tod - d
                #        liste1.append(f"{a.strftime('%b')} {int(a.__format__('%d'))}")
                #        
                #        await cursor.execute("SELECT anzahl FROM voice WHERE guildID = (%s) AND zeit = (%s)", (interaction.guild.id, a.strftime(f"%d.%m.%Y")))
                #        result = await cursor.fetchall()
                #        if result != ():
                #            anzahl = 0
                #            for stat in result:
                #                anzahl += int(stat[0])
                #            liste2.append(anzahl)
                #        else:
                #            liste2.append(0)

                    #plt.plot(liste1, liste2, color="#0a0a0d", marker=".")
                    
                #    text = ""
                #    b = await getservernachrichtenstats(self, "Kanäle", interaction.guild)
                #    text2 = ""
                #    c = await getservervoicestats(self, "Kanäle", interaction.guild)
                #    try:
                #        a = 0
                #        for data in b:
                #            l = []
                #            mitglied = interaction.guild.get_channel(int(data[0]))
                #            if mitglied != None:
                #                if a == 5:
                #                    break
                #                a += 1
                #                text += f"> {mitglied.mention}: {data[1]} {'Nachrichten' if int(data[1]) > 1 else 'Nachricht'}\n"
                #                legend.append(mitglied.name)
                                
                #                for i in range(0, maxdays):
                #                    d2 = datetime.timedelta(days=maxdays-i)
                #                    ab = tod - d2
                                    
                                    
                #                    await cursor.execute("SELECT anzahl FROM nachrichten WHERE guildID = (%s) AND zeit = (%s) AND channelID = (%s)", (interaction.guild.id, ab.strftime(f"%d.%m.%Y"), mitglied.id))
                #                    result = await cursor.fetchall()
                #                    if result != ():
                #                        anzahl = 0
                #                        for stat in result:
                #                            anzahl += int(stat[0])
                #                        l.append(anzahl)
                #                    else:
                #                        l.append(0)
                #            plt.plot(liste1, l)
                                
                #    except:
                #        text += f"Keine Daten"
                    
                #    try:
                #        a = 0
                #        for data in c:
                #            mitglied = interaction.guild.get_channel(int(data[0]))
                #            if mitglied != None:
                #                if a == 5:
                #                    break
                #                a += 1
                #                text2 += f"> {mitglied.mention}: {data[1]} {'Minuten' if int(data[1]) > 1 else 'Minute'}\n"
                #    except:
                #        text2 += "Keine Daten"
                        
                #    plt.legend(legend)
                #    plt.xticks(rotation=45)
                #    plt.savefig("stats.png")
                #    plt.close()
                #    embed = discord.Embed(colour=await getcolour(self, interaction.user), title=f"<:v_stats:1119583678083895346> Statistiken der aktivsten {art}", description=f"""
#<:v_chat:1119577968457568327> **Aktivste Textkanäle:**
#{text}

#<:v_mikrofon:1119581634216329266> **Aktivste Sprachkanäle:**
#{text2}""")
                #    embed.set_thumbnail(url=interaction.guild.icon)
                #    embed.set_image(url="attachment://stats.png")
                #    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                #    
                #    file = discord.File("stats.png", filename="stats.png")
                #    os.remove("stats.png")
                #    return await interaction.channel.send(file=file, embed=embed)

                    
async def setup(bot):
    await bot.add_cog(Stats(bot))