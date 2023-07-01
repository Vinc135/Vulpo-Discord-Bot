import typing
import discord
from discord.ext import commands, tasks
from discord import app_commands
from info import getcolour, haspremium_forserver
import asyncio

async def update_all(self):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM banner")
            result = await cursor.fetchall()
            for eintrag in result:
                guildID = eintrag[0]
                channelID = eintrag[1]
                guild = self.bot.get_guild(int(guildID))
                if guild is None:
                    continue
                channel = guild.get_channel(int(channelID))
                if channel is None:
                    continue
                
                await cursor.execute("SELECT userID, anzahl FROM nachrichten WHERE guildID = (%s) AND zeit = (%s) ORDER BY anzahl DESC", (guild.id, f"{discord.utils.utcnow().__format__('%d')}.{discord.utils.utcnow().__format__('%m')}.{discord.utils.utcnow().__format__('%Y')}"))
                result = await cursor.fetchone()
                id = result[0]
                aktivster_user_des_tages = guild.get_member(int(id))

async def neuer_banner(self, guild, channel):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM banner WHERE guildID = (%s)", (guild.id))
            result = await cursor.fetchone()
            if result == None:
                await cursor.execute("INSERT INTO banner(guildID, channelID, +++) VALUES(%s, %s, +++)", (guild.id, channel.id))
                return
            await cursor.execute("UPDATE channelID FROM banner WHERE guildID = (%s)", (guild.id))
            return True
        
async def delete_banner(self, guild):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM banner WHERE guildID = (%s)", (guild.id))
            return True

class Banner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_load(self):
        self.banner_update.start()
        
    def cog_unload(self):
        self.banner_update.cancel()
        
    @tasks.loop(minutes=10)
    async def banner_update(self):
        await update_all(self)

    banner = app_commands.Group(name='banner', description='Nehme Einstellungen am Banner-System vor.', guild_only=True)

    @banner.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def verwalten(self, interaction: discord.Interaction, modus: typing.Literal["Einstellen", "Ausschalten"], kanal: discord.TextChannel):
        """Lege einen Kanal fest, indem der Banner des aktivsten User des Tages gepostet wird."""
        if modus == "Einstellen":
            await neuer_banner(self, interaction.guild, kanal)
            return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Der Kanal {kanal.mention} ist nun der Banner-Kanal.**")
        if modus == "Ausschalten":
            await delete_banner(self, interaction.guild)
            return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Das Banner-System wurde auf diesem Server deaktiviert.**")

    @banner.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def anpassen(self, interaction: discord.Interaction, datei: discord.Attachment, kanal: discord.TextChannel):
        """Lade einen neuen Hintergrund oder Schriftart hoch."""
        if not datei.content_type.startswith("file/") or not datei.content_type.startswith("image/"):
            return await interaction.response.send_message("❌ **Das Attachment ist keine Bilddatei oder .ttf Datei.**", ephemeral=True)

        #do stuff
    
async def setup(bot):
    await bot.add_cog(Banner(bot))