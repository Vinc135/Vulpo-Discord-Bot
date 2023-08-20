import discord
from discord.ext import commands
from discord import app_commands
import math
import datetime
from info import discord_timestamp
from info import getcolour

class afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot:
            return
        
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT userID, grund, time FROM afk WHERE guildID = (%s)", (msg.guild.id))
                result = await cursor.fetchall()
                if result == None:
                    return
                for r in result:
                    member = msg.guild.get_member(int(r[0]))
                    if member == None:
                        await cursor.execute("DELETE FROM afk_nachrichten WHERE userID = (%s) AND guildID = (%s)", (r[0], msg.guild.id))
                        return await cursor.execute("DELETE FROM afk WHERE userID = (%s) AND guildID = (%s)", (r[0], msg.guild.id))
                    if member.id == msg.author.id:
                        t2 = datetime.datetime.fromtimestamp(int(r[2]))
                        try:
                            if msg.author.id != msg.guild.owner.id:
                                await msg.author.edit(nick="", reason="Member ist nicht mehr AFK")
                        except:
                            pass
                        await cursor.execute("SELECT authorID, msgID, channelID, time FROM afk_nachrichten WHERE userID = (%s) AND guildID = (%s)", (member.id, msg.guild.id))
                        result2 = await cursor.fetchall()
                        
                        embed = discord.Embed(title=f"<:v_afk:1119577204712542301> **{member.name}, willkommen zurück**", color=await getcolour(self, msg.author), description=f"""
Ich habe deinen AFK-Status entfernt. AFK gegangen {discord_timestamp(t2, 'R')}.""")
                        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                        if result2 == ():
                            embed.description += f"\n💬 Während du AFK warst wurdest du hier nicht gepingt."
                            await msg.reply(embed=embed)
                        else:
                            text = ""
                            embed.description += f"\n💬 Während du AFK warst wurdest du hier **{len(result2)}** Mal gepingt. \n__Alle Erwähnungen:__"
                            for ping in result2:
                                author = msg.guild.get_member(int(ping[0]))
                                channel = msg.guild.get_channel(int(ping[2]))
                                if author is None or channel is None:
                                    text += "Der Autor oder der Kanal konnte nicht gefunden werden.\n"
                                    continue
                                try:
                                    msg2 = await channel.fetch_message(int(ping[1]))
                                except:
                                    text += "Diese Nachricht wurde gelöscht oder konnte nicht gefunden werden.\n"
                                    continue
                                t2 = datetime.datetime.fromtimestamp(int(ping[3]))
                                if text == "":
                                    text += f"[{author.name}]({msg2.jump_url})"
                                else:
                                    text += f", [{author.name}]({msg2.jump_url})"

                            embed.description += f"\n{text}"
                            await msg.reply(embed=embed)
                        await cursor.execute("DELETE FROM afk_nachrichten WHERE userID = (%s) AND guildID = (%s)", (member.id, msg.guild.id))
                        return await cursor.execute("DELETE FROM afk WHERE userID = (%s) AND guildID = (%s)", (member.id, msg.guild.id))
                    
                    if len(msg.mentions) != 0:
                        for mention in msg.mentions:
                            if int(mention.id) == int(member.id):
                                t2 = datetime.datetime.fromtimestamp(int(r[2]))
                                t1 = math.floor(datetime.datetime.now().timestamp())
                                await cursor.execute("INSERT INTO afk_nachrichten(userID, guildID, authorID, msgID, channelID, time) VALUES(%s, %s, %s, %s, %s, %s)", (member.id, msg.guild.id, msg.author.id, msg.id, msg.channel.id, t1))
                                embed = discord.Embed(title=f"<:v_afk:1119577204712542301> **{mention.name}, ist AFK**", color=await getcolour(self, msg.author), description=f"""
*Grund: {r[1]}*
AFK gegangen {discord_timestamp(t2, 'R')}.""")
                                                      
                                embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                                await msg.reply(embed=embed)
                            
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.guild_only()
    async def afk(self, interaction: discord.Interaction, grund: str="Bitte nicht stören"):
        """Setze dich AFK."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT userID, grund, time FROM afk WHERE guildID = (%s) AND userID = (%s)", (interaction.guild.id, interaction.user.id))
                result = await cursor.fetchone()
                if result == None:
                    t1 = math.floor(datetime.datetime.now().timestamp())
                    t2 = datetime.datetime.fromtimestamp(t1)
                    await cursor.execute("INSERT INTO afk (guildID, userID, grund, time) VALUES (%s, %s, %s, %s)", (interaction.guild.id, interaction.user.id, grund, t1))
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
                
                if result != None:
                    t2 = datetime.datetime.fromtimestamp(int(result[2]))
                    try:
                        if interaction.user.id != interaction.guild.owner.id:
                            await interaction.user.edit(nick="", reason="Member ist nicht mehr AFK")
                    except:
                        pass
                    await cursor.execute("SELECT authorID, msgID, channelID, time FROM afk_nachrichten WHERE userID = (%s) AND guildID = (%s)", (interaction.user.id, interaction.guild.id))
                    result2 = await cursor.fetchall()
                    
                    embed = discord.Embed(title=f"<:v_afk:1119577204712542301> **{interaction.user.name}, willkommen zurück**", color=await getcolour(self, interaction.user), description=f"""
Ich habe deinen AFK-Status entfernt. AFK gegangen {discord_timestamp(t2, 'R')}.""")
                    embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                    if result2 == ():
                        embed.description += f"\n💬 Während du AFK warst wurdest du hier nicht gepingt."
                        await interaction.response.send_message(embed=embed)
                    else:
                        text = ""
                        a = 0
                        embed.description += f"\n💬 Während du AFK warst wurdest du hier **{len(result2)}** Mal gepingt. \n__Alle Erwähnungen:__"
                        for ping in result2:
                            author = interaction.guild.get_member(int(ping[0]))
                            channel = interaction.guild.get_channel(int(ping[2]))
                            if channel == None:
                                continue
                            try:
                                msg2 = await channel.fetch_message(int(ping[1]))
                                a = 1
                            except:
                                text += "Diese Nachricht wurde gelöscht."
                                a = 1
                            if author == None or channel == None:
                                text += "Diese Nachricht wurde gelöscht."
                                a = 1
                            if a == 0:
                                t2 = datetime.datetime.fromtimestamp(int(ping[3]))
                                if text == "":
                                    text += f"[{author.name}]({msg2.jump_url})"
                                else:
                                    text += f", [{author.name}]({msg2.jump_url})"
                                embed.description += f"\n💬 Während du AFK warst wurdest du hier **{len(result2)}** Mal gepingt. \n__Alle Erwähnungen:__\n{text}"
                        await interaction.response.send_message(embed=embed)
                    await cursor.execute("DELETE FROM afk_nachrichten WHERE userID = (%s) AND guildID = (%s)", (interaction.user.id, interaction.guild.id))
                    return await cursor.execute("DELETE FROM afk WHERE userID = (%s) AND guildID = (%s)", (interaction.user.id, interaction.guild.id))

async def setup(bot):
    await bot.add_cog(afk(bot))