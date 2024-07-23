import discord
from discord.ext import commands
from discord import app_commands
import math
import datetime
from utils.utils import discord_timestamp, getcolour
from utils.MongoDB import getMongoDataBase, getMongoClient

class afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild is None:
            return
        if msg.author.bot:
            return
        
        db = getMongoDataBase()
        afk_collection = db['afk']
        afk_nachrichten_collection = db['afk_nachrichten']
        
        results = await afk_collection.find({"guildID": str(msg.guild.id)}).to_list(length=None)
        if not results:
            return
        
        for r in results:
            member = msg.guild.get_member(int(r['userID']))
            if member is None:
                await afk_nachrichten_collection.delete_many({"userID": str(r['userID']), "guildID": str(msg.guild.id)})
                await afk_collection.delete_one({"userID": str(r['userID']), "guildID": str(msg.guild.id)})
                continue
            if member.id == msg.author.id:
                t2 = datetime.datetime.fromtimestamp(int(r['time']))
                try:
                    if msg.author.id != msg.guild.owner.id:
                        await msg.author.edit(nick="", reason="Member ist nicht mehr AFK")
                except:
                    pass
                result2 = await afk_nachrichten_collection.find({"userID": str(member.id), "guildID": str(msg.guild.id)}).to_list(length=None)
                
                embed = discord.Embed(title=f"<:v_afk:1119577204712542301> **{member.name}, willkommen zurück**", color=await getcolour(self, msg.author), description=f"""
Ich habe deinen AFK-Status entfernt. AFK gegangen {discord_timestamp(t2, 'R')}.""")
                
                if not result2:
                    embed.description += f"\n<:v_chat:1264270959121010728> Während du AFK warst wurdest du hier nicht gepingt."
                    await msg.reply(embed=embed)
                else:
                    text = ""
                    embed.description += f"\n<:v_chat:1264270959121010728> Während du AFK warst wurdest du hier **{len(result2)}** Mal gepingt. \n__Alle Erwähnungen:__"
                    for ping in result2:
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
                await afk_nachrichten_collection.delete_many({"userID": str(member.id), "guildID": str(msg.guild.id)})
                await afk_collection.delete_one({"userID": str(member.id), "guildID": str(msg.guild.id)})
            
            if len(msg.mentions) != 0:
                for mention in msg.mentions:
                    if int(mention.id) == int(member.id):
                        t2 = datetime.datetime.fromtimestamp(int(r['time']))
                        t1 = math.floor(datetime.datetime.now().timestamp())
                        await afk_nachrichten_collection.insert_one({
                            "userID": str(member.id), 
                            "guildID": str(msg.guild.id), 
                            "authorID": str(msg.author.id), 
                            "msgID": str(msg.id), 
                            "channelID": str(msg.channel.id), 
                            "time": t1
                        })
                        embed = discord.Embed(title=f"<:v_afk:1119577204712542301> **{mention.name}, ist AFK**", color=await getcolour(self, msg.author), description=f"""
*Grund: {r['grund']}*
AFK gegangen {discord_timestamp(t2, 'R')}.""")
                                                      
                        await msg.reply(embed=embed)
                            
    @app_commands.command()
    @app_commands.guild_only()
    async def afk(self, interaction: discord.Interaction, grund: str="Bitte nicht stören"):
        """Setze dich AFK."""
        await interaction.response.defer()
        db = getMongoDataBase()
        afk_collection = db['afk']
        afk_nachrichten_collection = db['afk_nachrichten']
        
        result = await afk_collection.find_one({"guildID": str(str(interaction.guild.id)), "userID": str(interaction.user.id)})
        if result is None:
            t1 = math.floor(datetime.datetime.now().timestamp())
            t2 = datetime.datetime.fromtimestamp(t1)
            await afk_collection.insert_one({
                "guildID": str(str(interaction.guild.id)), 
                "userID": str(interaction.user.id), 
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
            
            return await interaction.followup.send(embed=embed)
        
        else:
            t2 = datetime.datetime.fromtimestamp(int(result['time']))
            try:
                if interaction.user.id != interaction.guild.owner.id:
                    await interaction.user.edit(nick="", reason="Member ist nicht mehr AFK")
            except:
                pass
            result2 = await afk_nachrichten_collection.find({"userID": str(interaction.user.id), "guildID": str(str(interaction.guild.id))}).to_list(length=None)
            
            embed = discord.Embed(title=f"<:v_afk:1119577204712542301> **{interaction.user.name}, willkommen zurück**", color=await getcolour(self, interaction.user), description=f"""
Ich habe deinen AFK-Status entfernt. AFK gegangen {discord_timestamp(t2, 'R')}.""")
            
            if not result2:
                embed.description += f"\n<:v_chat:1264270959121010728> Während du AFK warst wurdest du hier nicht gepingt."
                await interaction.followup.send(embed=embed)
            else:
                text = ""
                a = 0
                embed.description += f"\n<:v_chat:1264270959121010728> Während du AFK warst wurdest du hier **{len(result2)}** Mal gepingt. \n__Alle Erwähnungen:__"
                for ping in result2:
                    author = interaction.guild.get_member(int(ping['authorID']))
                    channel = interaction.guild.get_channel(int(ping['channelID']))
                    if channel is None:
                        continue
                    try:
                        msg2 = await channel.fetch_message(int(ping['msgID']))
                        a = 1
                    except:
                        text += "Diese Nachricht wurde gelöscht."
                        a = 1
                    if author is None or channel is None:
                        text += "Diese Nachricht wurde gelöscht."
                        a = 1
                    if a == 0:
                        t2 = datetime.datetime.fromtimestamp(int(ping['time']))
                        if text == "":
                            text += f"[{author.name}]({msg2.jump_url})"
                        else:
                            text += f", [{author.name}]({msg2.jump_url})"
                        embed.description += f"\n<:v_chat:1264270959121010728> Während du AFK warst wurdest du hier **{len(result2)}** Mal gepingt. \n__Alle Erwähnungen:__\n{text}"
                await interaction.followup.send(embed=embed)
            await afk_nachrichten_collection.delete_many({"userID": str(interaction.user.id), "guildID": str(str(interaction.guild.id))})
            await afk_collection.delete_one({"userID": str(interaction.user.id), "guildID": str(str(interaction.guild.id))})

async def setup(bot):
    await bot.add_cog(afk(bot))
