import typing
import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import getcolour
from utils.MongoDB import getMongoDataBase

class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def starboard(self, interaction: discord.Interaction, argument: typing.Literal["Einrichten (Kanal muss mit angegeben werden)","Anzeigen","Ausschalten"], kanal: discord.TextChannel=None):
                """Lege einen Kanal fest für Nachrichten, welche 5 Sternen von Usern bekommen haben."""
        
                await interaction.response.defer()
                
                db = getMongoDataBase()
        
                if argument == "Ausschalten":
                    result = await db['starboard'].find_one({"guildID": interaction.guild.id})
                    if result == None:
                        return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Auf diesem Server ist kein Starboard eingerichtet.**", ephemeral=True)
                    await db["starboard"].delete_one({"guildID": interaction.guild.id})
                    return await interaction.followup.send("**<:v_haken:1119579684057907251> Das Starboard wurde ausgeschaltet.**")
                if argument == "Einrichten (Kanal muss mit angegeben werden)":
                    if kanal == None:
                        return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Beim Einrichten ist auch eine Kanal-Angabe erforderlich.**", ephemeral=True)

                    result = await db['starboard'].find_one({"guildID": interaction.guild.id})
                    if result:
                        await db["starboard"].update_one({"guildID": interaction.guild.id}, {"$set": {"channelID": kanal.id}})
                    else:
                        await db["starboard"].insert_one({"guildID": interaction.guild.id, "channelID": kanal.id})
                    await interaction.followup.send(f"**<:v_haken:1119579684057907251> Das Starboard ist nun aktiv in {kanal.mention}.**")
                if argument == "Anzeigen":
                    result = await db['starboard'].find_one({"guildID": interaction.guild.id})
                    try:
                        channel = await interaction.guild.fetch_channel(int(result["channelID"]))
                    except:
                        return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Der Kanal des Starboards existiert nicht mehr. Bitte deaktiviere das Starboard und richte ihn erneut ein.**", ephemeral=True)

                    embed = discord.Embed(title="Starboard", description=f"Das aktuelle Starboard ist aktiv in {channel.mention}", color=discord.Color.orange())
                    
                    await interaction.followup.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        if str(reaction.emoji) == "⭐":
                    db = getMongoDataBase()
                    channel_id = await db['starboard'].find_one({"guildID": reaction.message.guild.id})
                    
                    if not channel_id:
                        return
                    
                    result = await db['starboard_msg'].find_one({"msgID": reaction.message.id})
                    if result:
                        channel: discord.TextChannel = await self.bot.fetch_channel(int(result["channelID"]))
                        if channel:
                            msg: discord.Message = await channel.fetch_message(int(result[1]))
                            if msg is None:
                                embed = discord.Embed(title="⭐️ Nachricht ausgezeichnet! ⭐️", description=reaction.message.content, color=discord.Color.orange())
                                
                                embed.description += f"\n\n**[Springe zur Nachricht]({reaction.message.jump_url})**"
                                embed.set_author(name=reaction.message.author, icon_url=reaction.message.author.avatar)
                                for attachment in reaction.message.attachments:
                                    embed.set_image(url=attachment.url)
                                await channel.send(embed=embed)
                    else:
                        if reaction.count < 3:
                            return
                        channel = await self.bot.fetch_channel(int(channel_id[0]))
                        if channel:
                            embed = discord.Embed(title="⭐️ Nachricht ausgezeichnet! ⭐️", description=reaction.message.content, color=discord.Color.orange())
                            
                            embed.description += f"\n\n**[Springe zur Nachricht]({reaction.message.jump_url})**"
                            embed.set_author(name=reaction.message.author, icon_url=reaction.message.author.avatar)
                            for attachment in reaction.message.attachments:
                                embed.set_image(url=attachment.url)
                            msg = await channel.send(embed=embed)
                            
                            await db['starboard_msg'].insert_one({"guildID": reaction.message.guild.id, "channelID": channel.id, "msgID": reaction.message.id, "starboardID": msg.id})

async def setup(bot):
    await bot.add_cog(starboard(bot))