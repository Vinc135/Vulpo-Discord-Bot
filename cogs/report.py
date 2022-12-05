#`/reportlog` Lege einen Kanal fest für gemeldete Nachrichten von Usern.
import typing
import discord
from discord.ext import commands
import random
from discord import app_commands

class report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def reportlog(self, interaction: discord.Interaction, argument: typing.Literal["Einrichten (Kanal muss mit angegeben werden)","Anzeigen","Ausschalten"], kanal: discord.TextChannel=None):
        """Lege einen Kanal fest für gemeldete Nachrichten von Usern."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if argument == "Ausschalten":
                    await cursor.execute(f"SELECT channelID FROM reportlog WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    if result == None:
                        return await interaction.response.send_message("**❌ Auf diesem Server ist kein Reportlog eingerichtet.**", ephemeral=True)
                    await cursor.execute("DELETE FROM reportlog WHERE guildID = (%s)", (interaction.guild.id))
                    return await interaction.response.send_message("**✅ Der Reportlog wurde ausgeschaltet.**")
                if argument == "Einrichten (Kanal muss mit angegeben werden)":
                    if kanal == None:
                        return await interaction.response.send_message("**❌ Beim Einrichten ist auch eine Kanal-Angabe erforderlich.**", ephemeral=True)

                    await cursor.execute(f"SELECT channelID FROM reportlog WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    if result:
                        await cursor.execute("UPDATE reportlog SET channelID = (%s) WHERE guildID = (%s)", (kanal.id, interaction.guild.id))
                    else:
                        await cursor.execute("INSERT INTO reportlog(guildID, channelID) VALUES(%s, %s)", (interaction.guild.id, kanal.id))
                    await interaction.response.send_message(f"**✅ Der Reportlog ist nun aktiv in {kanal.mention}.**")
                if argument == "Anzeigen":
                    await cursor.execute(f"SELECT channelID FROM reportlog WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    try:
                        channel = interaction.guild.get_channel(int(result[0]))
                    except:
                        return await interaction.response.send_message("**❌ Der Kanal des Reportlogs existiert nicht mehr. Bitte deaktiviere den Reportlog und richte ihn erneut ein.**", ephemeral=True)

                    embed = discord.Embed(title="Reportlog", description=f"Der aktuelle Reportlog ist aktiv in {channel.mention}", color=discord.Color.orange())
                    await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(report(bot))