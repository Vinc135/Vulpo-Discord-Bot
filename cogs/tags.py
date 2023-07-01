import discord
from discord.ext import commands
from discord import app_commands
from info import getcolour, haspremium_forserver

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    tag = app_commands.Group(name='tag', description='Erstelle und lösche Tags.', guild_only=True)

    @tag.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add(self, interaction: discord.Interaction, name: str, output: str):
        """Füge einen Tag hinzu."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT name FROM tags WHERE guildID = (%s)", (interaction.guild.id))
                a = await cursor.fetchall()
                premium_status = await haspremium_forserver(self, interaction.guild)
                if premium_status == False:
                    if len(a) >= 3:
                        return await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Du kannst keine weiteren Befehle erstellen, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")

                await cursor.execute("SELECT name FROM tags WHERE guildID = (%s) AND name = (%s)", (interaction.guild.id, name))
                result = await cursor.fetchone()
                if result != None:
                    await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Dieser Tag existiert bereits. Wähle bitte einen anderen Namen.**", ephemeral=True)
                    return
                await cursor.execute("INSERT INTO tags(guildID, name, output) VALUES(%s,%s,%s)", (interaction.guild.id, name, output))
                
                await interaction.response.send_message(f"**<:v_haken:1119579684057907251> Tag erstellt. Wenn jemand `!tag {name}` schreibt, kommt dieser Text:**\n*{output}*.")

    @tag.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def delete(self, interaction: discord.Interaction, name: str):
        """Entferne einen Tag."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT name FROM tags WHERE guildID = (%s) AND name = (%s)", (interaction.guild.id, name))
                result = await cursor.fetchone()
                if result == None:
                    await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Dieser Tag existiert nicht. Füge einen Tag mit `/tag add <name> <output>` hinzu.", ephemeral=True)
                    return
                await cursor.execute("DELETE FROM tags WHERE guildID = (%s) AND name = (%s)", (interaction.guild.id, name))
                
                await interaction.response.send_message(f"**<:v_haken:1119579684057907251> Tag gelöscht.**")

    @tag.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def liste(self, interaction: discord.Interaction):
        """Erhalte eine Liste von den Tags."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT name, output FROM tags WHERE guildID = (%s)", (interaction.guild.id))
                result = await cursor.fetchall()
                if result == None:
                    await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Hier wurden keine Tags gefunden. Füge einen Tag mit `/tag add <name> <output>` hinzu**", ephemeral=True)
                    return
                embed = discord.Embed(title="Alle Tags des Servers", description="Hier nähere Infos:", color=await getcolour(self, interaction.user))
                embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                for i in result:
                    embed.add_field(name=i[0], value=f"Output: *{i[1]}*")
                await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot:
            return
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT name, output FROM tags WHERE guildID = (%s)", (msg.guild.id))
                result = await cursor.fetchall()
                if result is None or result == "()":
                    return
                for message in result:
                    if message is None or message == "()":
                        return
                    if f"!tag {str(message[0]).lower()}" == msg.content.lower():
                        embed = discord.Embed(title=f"__{message[0].upper()}__", description=message[1], color=await getcolour(self, msg.author))
                        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                        embed.set_thumbnail(url=msg.guild.icon)
                        embed.set_author(name=msg.author, icon_url=msg.author.avatar)
                        await msg.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Tags(bot))