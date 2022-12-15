import typing
import discord
from discord.ext import commands
import random
from discord import app_commands

class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def starboard(self, interaction: discord.Interaction, argument: typing.Literal["Einrichten (Kanal muss mit angegeben werden)","Anzeigen","Ausschalten"], kanal: discord.TextChannel=None):
        """Lege einen Kanal fest für Nachrichten mit 5 Sternen von Usern."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if argument == "Ausschalten":
                    await cursor.execute(f"SELECT channelID FROM starboard WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    if result == None:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Auf diesem Server ist kein Starboard eingerichtet.**", ephemeral=True)
                    await cursor.execute("DELETE FROM starboard WHERE guildID = (%s)", (interaction.guild.id))
                    return await interaction.response.send_message("**<:v_haken:1048677657040134195> Das Starboard wurde ausgeschaltet.**")
                if argument == "Einrichten (Kanal muss mit angegeben werden)":
                    if kanal == None:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Beim Einrichten ist auch eine Kanal-Angabe erforderlich.**", ephemeral=True)

                    await cursor.execute(f"SELECT channelID FROM starboard WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    if result:
                        await cursor.execute("UPDATE starboard SET channelID = (%s) WHERE guildID = (%s)", (kanal.id, interaction.guild.id))
                    else:
                        await cursor.execute("INSERT INTO starboard(guildID, channelID) VALUES(%s, %s)", (interaction.guild.id, kanal.id))
                    await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Das Starboard ist nun aktiv in {kanal.mention}.**")
                if argument == "Anzeigen":
                    await cursor.execute(f"SELECT channelID FROM starboard WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    try:
                        channel = interaction.guild.get_channel(int(result[0]))
                    except:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Der Kanal des Starboards existiert nicht mehr. Bitte deaktiviere das Starboard und richte ihn erneut ein.**", ephemeral=True)

                    embed = discord.Embed(title="Starboard", description=f"Das aktuelle Starboard ist aktiv in {channel.mention}", color=discord.Color.orange())
                    await interaction.response.send_message(embed=embed)
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        if str(reaction.emoji) == "⭐":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelID FROM starboard WHERE guildID = (%s)", (reaction.message.guild.id))
                    channel_id = await cursor.fetchone()
                    if channel_id:
                        await cursor.execute("SELECT channelID, starboardID FROM starboard_msg WHERE msgID = (%s)", (reaction.message.id))
                        result = await cursor.fetchone()
                        if result:
                            channel: discord.TextChannel = self.bot.get_channel(int(result[0]))
                            if channel:
                                msg: discord.Message = await channel.fetch_message(int(result[1]))
                                if msg:
                                    embed = msg.embeds[0]
                                    embed.set_footer(text=f"{reaction.count} ⭐️-Reaktionen")
                        else:
                            channel = self.bot.get_channel(int(channel_id[0]))
                            if channel:
                                embed = discord.Embed(title="⭐️ Nachricht ausgezeichnet! ⭐️", description=f"'{reaction.message.content}' - {reaction.message.author.mention}", color=discord.Color.orange())
                                embed.set_author(name=reaction.message.author, icon_url=reaction.message.author.avatar)
                                for attachment in reaction.message.attachments:
                                    embed.set_image(url=attachment.url)
                                embed.set_footer(text=f"{reaction.count} ⭐️-Reaktionen")
                                msg = await channel.send(embed=embed)
                                await cursor.execute("INSERT INTO starboard_msg(guildID, channelID, msgID, starboardID) VALUES(%s, %s, %s, %s)", (reaction.message.guild.id, channel.id, reaction.message.id, msg.id))

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.emoji == "⭐️":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelD, starboardID FROM starboard_msg WHERE msgID = (%s)", (reaction.message.id))
                    result = await cursor.fetchone()
                    if result:
                        channel: discord.TextChannel = self.bot.get_channel(int(result[0]))
                        if channel:
                            msg: discord.Message = await channel.fetch_message(int(result[1]))
                            if msg:
                                embed = msg.embeds[0]
                                embed.set_footer(text=f"{reaction.count} ⭐️-Reaktionen")

async def setup(bot):
    await bot.add_cog(starboard(bot))