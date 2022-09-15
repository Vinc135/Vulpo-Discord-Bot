import discord
from discord.ext import commands
from discord import app_commands
import math
import datetime
from info import discord_timestamp

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
                        await cursor.execute("DELETE FROM afk_nachrichten WHERE userID = (%s) AND guildID = (%s)", (member.id, msg.guild.id))
                        return await cursor.execute("DELETE FROM afk WHERE userID = (%s) AND guildID = (%s)", (member.id, msg.guild.id))
                    if member.id == msg.author.id:
                        t2 = datetime.datetime.fromtimestamp(int(r[2]))
                        try:
                            if msg.author.id != msg.guild.owner.id:
                                await msg.author.edit(nick="", reason="Member ist nicht mehr AFK")
                        except:
                            pass
                        await cursor.execute("SELECT authorID, msgID, channelID, time FROM afk_nachrichten WHERE userID = (%s) AND guildID = (%s)", (member.id, msg.guild.id))
                        result2 = await cursor.fetchall()
                        
                        embed = discord.Embed(title=f"<:status_online:944569387900346378> **{member.name}, willkommen zurück**", color=discord.Colour.green(), description=f"""
Ich habe deinen AFK-Status entfernt. AFK gegangen {discord_timestamp(t2, 'R')}.""")
                        
                        if result2 == ():
                            embed.description += f"\n💬 Während du AFK warst wurdest du hier nicht gepingt."
                            await msg.reply(embed=embed)
                        else:
                            text = ""
                            embed.description += f"\n💬 Während du AFK warst wurdest du hier **{len(result2)}** Mal gepingt. \n__Alle Erwähnungen:__"
                            for ping in result2:
                                author = msg.guild.get_member(int(ping[0]))
                                channel = msg.guild.get_channel(int(ping[2]))
                                msg2 = await channel.fetch_message(int(ping[1]))
                                if author == None or channel == None or msg2 == None:
                                    pass
                                else:
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
                                t1 = math.floor(datetime.datetime.utcnow().timestamp())
                                await cursor.execute("INSERT INTO afk_nachrichten(userID, guildID, authorID, msgID, channelID, time) VALUES(%s, %s, %s, %s, %s, %s)", (member.id, msg.guild.id, msg.author.id, msg.id, msg.channel.id, t1))
                                embed = discord.Embed(title=f"<:status_dnd:944569387489316895> **{mention.name}, ist AFK**", color=discord.Colour.red(), description=f"""
*Grund: {r[1]}*
AFK gegangen {discord_timestamp(t2, 'R')}.""")
                                await msg.reply(embed=embed)
                            
    @app_commands.command(name="afk")
    async def afk(self, interaction: discord.Interaction, grund: str="Bitte nicht stören"):
        """Setze dich AFK."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT userID, grund, time FROM afk WHERE guildID = (%s) AND userID = (%s)", (interaction.guild.id, interaction.user.id))
                result = await cursor.fetchone()
                if result == None:
                    t1 = math.floor(datetime.datetime.utcnow().timestamp())
                    t2 = datetime.datetime.fromtimestamp(t1)
                    await cursor.execute("INSERT INTO afk (guildID, userID, grund, time) VALUES (%s, %s, %s, %s)", (interaction.guild.id, interaction.user.id, grund, t1))
                    try:
                        if interaction.user.id != interaction.guild.owner.id:
                            await interaction.user.edit(nick="", reason="Member ist AFK")
                    except:
                        pass
                    
                    embed = discord.Embed(title=f"<:status_dnd:944569387489316895> **{interaction.user.name}, du bist jetzt AFK**", color=discord.Colour.red(), description=f"""
*Grund: {grund}* 
AFK gegangen {discord_timestamp(t2, 'R')}.
Wenn du wiederkommst, zeige ich dir alle Nachrichten, in denen du gepingt wurdest.""")
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
                    
                    embed = discord.Embed(title=f"<:status_online:944569387900346378> **{interaction.user.name}, willkommen zurück**", color=discord.Colour.green(), description=f"""
Ich habe deinen AFK-Status entfernt. AFK gegangen {discord_timestamp(t2, 'R')}.""")
                    
                    if result2 == ():
                        embed.description += f"\n💬 Während du AFK warst wurdest du hier nicht gepingt."
                        await interaction.response.send_message(embed=embed)
                    else:
                        text = ""
                        for ping in result2:
                            author = interaction.guild.get_member(int(ping[0]))
                            channel = interaction.guild.get_channel(int(ping[2]))
                            msg2 = await channel.fetch_message(int(ping[1]))
                            if author == None or channel == None or msg2 == None:
                                pass
                            else:
                                t2 = datetime.datetime.fromtimestamp(int(result[3]))
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