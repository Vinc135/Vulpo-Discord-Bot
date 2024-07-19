import discord
from discord.ext import commands
from discord import app_commands
import math
import datetime
from utils.utils import discord_timestamp
from utils.utils import getcolour
from pymongo import MongoClient

class afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = MongoClient('mongodb://localhost:27017/')  # Passe die Verbindungszeichenfolge bei Bedarf an
        self.db = self.client['discord_bot']  # Name der Datenbank
        self.afk_collection = self.db['afk']
        self.afk_nachrichten_collection = self.db['afk_nachrichten']

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild is None or msg.author.bot:
            return
        
        afk_entries = self.afk_collection.find({"guildID": msg.guild.id})
        if afk_entries is None:
            return

        for entry in afk_entries:
            member = msg.guild.get_member(int(entry['userID']))
            if member is None:
                self.afk_nachrichten_collection.delete_many({"userID": entry['userID'], "guildID": msg.guild.id})
                self.afk_collection.delete_one({"userID": entry['userID'], "guildID": msg.guild.id})
                return
            
            if member.id == msg.author.id:
                t2 = datetime.datetime.fromtimestamp(int(entry['time']))
                try:
                    if msg.author.id != msg.guild.owner.id:
                        await msg.author.edit(nick="", reason="Member ist nicht mehr AFK")
                except:
                    pass
                
                afk_nachrichten = self.afk_nachrichten_collection.find({"userID": member.id, "guildID": msg.guild.id})
                
                embed = discord.Embed(title=f"<:v_afk:1119577204712542301> **{member.name}, willkommen zurück**", color=await getcolour(self, msg.author), description=f"""
Ich habe deinen AFK-Status entfernt. AFK gegangen {discord_timestamp(t2, 'R')}.""")
                embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                
                if afk_nachrichten.count() == 0:
                    embed.description += f"\n💬 Während du AFK warst wurdest du hier nicht gepingt."
                    await msg.reply(embed=embed)
                else:
                    text = ""
                    embed.description += f"\n💬 Während du AFK warst wurdest du hier **{afk_nachrichten.count()}** Mal gepingt. \n__Alle Erwähnungen:__"
                    for ping in afk_nachrichten:
                        author = msg.guild.get_member(int(ping['authorID']))
                        channel = msg.guild.get_channel(int(ping['channelID']))
                        if author is None or channel is None:
                            text += "Der Autor oder der Kanal konnte nicht gefunden werden.\n"
                            continue
                        try:
                            msg2 = await channel.fetch_message(int(ping['msgID']))
                        except:
                            text += "Diese Nachricht wurde gelöscht oder konnte nicht gefunden werden.\n"
                            continue
                        t2 = datetime.datetime.fromtimestamp(int(ping['time']))
                        if text == "":
                            text += f"[{author.name}]({msg2.jump_url})"
                        else:
                            text += f", [{author.name}]({msg2.jump_url})"
                    
                    embed.description += f"\n{text}"
                    await msg.reply(embed=embed)
                
                self.afk_nachrichten_collection.delete_many({"userID": member.id, "guildID": msg.guild.id})
                self.afk_collection.delete_one({"userID": member.id, "guildID": msg.guild.id})
                return

            if len(msg.mentions) != 0:
                for mention in msg.mentions:
                    if int(mention.id) == int(member.id):
                        t2 = datetime.datetime.fromtimestamp(int(entry['time']))
                        t1 = math.floor(datetime.datetime.now().timestamp())
                        self.afk_nachrichten_collection.insert_one({
                            "userID": member.id,
                            "guildID": msg.guild.id,
                            "authorID": msg.author.id,
                            "msgID": msg.id,
                            "channelID": msg.channel.id,
                            "time": t1
                        })
                        embed = discord.Embed(title=f"<:v_afk:1119577204712542301> **{mention.name}, ist AFK**", color=await getcolour(self, msg.author), description=f"""
*Grund: {entry['grund']}*
AFK gegangen {discord_timestamp(t2, 'R')}.""")
                        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                        await msg.reply(embed=embed)
                        
    @app_commands.command()
    @app_commands.guild_only()
    async def afk(self, interaction: discord.Interaction, grund: str = "Bitte nicht stören"):
        """Setze dich AFK."""
        afk_entry = self.afk_collection.find_one({"guildID": interaction.guild.id, "userID": interaction.user.id})
        if afk_entry is None:
            t1 = math.floor(datetime.datetime.now().timestamp())
            t2 = datetime.datetime.fromtimestamp(t1)
            self.afk_collection.insert_one({
                "guildID": interaction.guild.id,
                "userID": interaction.user.id,
                "grund": grund,
                "time": t1
            })
            try:
                if interaction.user.id != interaction.guild.owner.id:
                    await interaction.user.edit(nick="", reason="Member ist AFK")
            except:
                pass
            
            embed = discord.Embed(title=f"<:v_afk:1119577204712542301> **{interaction.user.name}, du bist jetzt AFK**", color=await getcolour(self, interaction.user), description=f"""
*Grund: {grund}* 
AFK gegangen {discord_timestamp(t2, 'R')}.
Wenn du wiederkommst, zeige ich dir alle Nachrichten, in denen du gepingt wurdest.""")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            return await interaction.response.send_message(embed=embed)
        
        t2 = datetime.datetime.fromtimestamp(int(afk_entry['time']))
        try:
            if interaction.user.id != interaction.guild.owner.id:
                await interaction.user.edit(nick="", reason="Member ist nicht mehr AFK")
        except:
            pass
        
        afk_nachrichten = self.afk_nachrichten_collection.find({"userID": interaction.user.id, "guildID": interaction.guild.id})
        
        embed = discord.Embed(title=f"<:v_afk:1119577204712542301> **{interaction.user.name}, willkommen zurück**", color=await getcolour(self, interaction.user), description=f"""
Ich habe deinen AFK-Status entfernt. AFK gegangen {discord_timestamp(t2, 'R')}.""")
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        
        if afk_nachrichten.count() == 0:
            embed.description += f"\n💬 Während du AFK warst wurdest du hier nicht gepingt."
            await interaction.response.send_message(embed=embed)
        else:
            text = ""
            embed.description += f"\n💬 Während du AFK warst wurdest du hier **{afk_nachrichten.count()}** Mal gepingt. \n__Alle Erwähnungen:__"
            for ping in afk_nachrichten:
                author = interaction.guild.get_member(int(ping['authorID']))
                channel = interaction.guild.get_channel(int(ping['channelID']))
                if channel is None:
                    continue
                try:
                    msg2 = await channel.fetch_message(int(ping['msgID']))
                    text += f"[{author.name}]({msg2.jump_url})"
                except:
                    text += "Diese Nachricht wurde gelöscht."
                if author is None or channel is None:
                    text += "Diese Nachricht wurde gelöscht."
                else:
                    t2 = datetime.datetime.fromtimestamp(int(ping['time']))
                    if text == "":
                        text += f"[{author.name}]({msg2.jump_url})"
                    else:
                        text += f", [{author.name}]({msg2.jump_url})"
            
            embed.description += f"\n{text}"
            await interaction.response.send_message(embed=embed)
        
        self.afk_nachrichten_collection.delete_many({"userID": interaction.user.id, "guildID": interaction.guild.id})
        self.afk_collection.delete_one({"userID": interaction.user.id, "guildID": interaction.guild.id})

async def setup(bot):
    await bot.add_cog(afk(bot))
