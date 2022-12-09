import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Autoreact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT emoji FROM autoreact WHERE guildID = (%s) AND channelID = (%s)", (msg.guild.id, msg.channel.id))
                result = await cursor.fetchall()
                if result == None or result == "()":
                    return
                for e in result:
                    try:
                        emoji = discord.PartialEmoji.from_str(e[0])
                        if emoji == None:
                            return
                        await msg.add_reaction(emoji)
                    except:
                        return

    autoreact = app_commands.Group(name='autoreact', description='Nehme Einstellungen am Autoreactsystem vor.')

    @autoreact.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.describe(emoji="Für normale Emojis: name:id oder für Animierte: a:name:id")
    async def add(self, interaction: discord.Interaction, kanal: discord.TextChannel, emoji: str):
        """Füge ein Emoji für ein Kanal hinzu."""
        try:
            await interaction.response.defer()
            emoj = discord.PartialEmoji.from_str(emoji)
            if emoj is None:
                return await interaction.followup.send("**<:v_kreuz:1049388811353858069> Der Emoji wurde nicht gefunden. Stelle sicher dass dieses Emoji auf einem Server ist, auf dem ich auch bin und dass du das Format eingehalten hast:\n`Für normale Emojis: name:id oder für Animierte: a:name:id`**", ephemeral=True)
            msg = await interaction.channel.send("**⚡️ Ich überprüfe die Verfügbarkeit des Emojis.**")
            await msg.add_reaction(emoj)
            await msg.delete()
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO autoreact(guildID, channelID, emoji) VALUES(%s,%s,%s)", (interaction.guild.id, kanal.id, emoji))
                    await interaction.followup.send(f"**<:v_haken:1048677657040134195> Eintrag erstellt. Jede Nachricht aus dem Kanal {kanal.mention} erhält das Emoji {emoj}.**")
        except:
            await msg.delete()
            return await interaction.followup.send("**<:v_kreuz:1049388811353858069> Der Emoji wurde nicht gefunden. Stelle sicher dass dieses Emoji auf einem Server ist, auf dem ich auch bin und dass du das Format eingehalten hast:\n`Für normale Emojis: name:id oder für Animierte: a:name:id`**", ephemeral=True)

    @autoreact.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def delete(self, interaction: discord.Interaction, kanal: discord.TextChannel):
        """Entferne Autoemojis eines Kanals."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT emoji FROM autoreact WHERE guildID = (%s) AND channelID = (%s)", (interaction.guild.id, kanal.id))
                result = await cursor.fetchall()
                if result == None or result == "()":
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> In dem Kanal ist keine Autoreaktion eingestellt.**", ephemeral=True)
                    return
                await cursor.execute("DELETE FROM autoreact WHERE guildID = (%s) AND channelID = (%s)", (interaction.guild.id, kanal.id))
                await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Einträge gelöscht.**")

    @autoreact.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def liste(self, interaction: discord.Interaction):
        """Erhalte eine Liste von den Autoemojis und deren Kanäle."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT emoji, channelID FROM autoreact WHERE guildID = (%s)", (interaction.guild.id))
                result = await cursor.fetchall()
                if result == ():
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Hier gibt es keine autoemojis. Füge eine mit `/autoreact add <kanal> <emoji>` hinzu**", ephemeral=True)
                    return
                embed = discord.Embed(title="Alle automatische Emojis in Kanälen", description="Hier nähere Infos:", color=discord.Color.orange())
                for i in result:
                    k = interaction.guild.get_channel(int(i[1]))
                    if k is not None:
                        channel = k
                    if k is None:
                        k = "Kanal veraltet"
                    emoj = discord.PartialEmoji.from_str(i[0])
                    if emoj is None:
                        emoj = "Emoji veraltet"
                    embed.add_field(name=channel.mention, value=emoj)
                await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Autoreact(bot))