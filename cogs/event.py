import discord
from discord.ext import commands
from discord import app_commands

class Modal(discord.ui.Modal, title="Formular"):
    def __init__(self, bot=None, guild: discord.Guild=None):
        super().__init__(custom_id="dheiwdgouewhvifdzg3eviuh")
        self.bot = bot
        self.guild = guild
        self.add_item(discord.ui.TextInput(label="Einladung zum Server", style=discord.TextStyle.short, required=True))
        self.add_item(discord.ui.TextInput(label="Server Beschreibung", style=discord.TextStyle.long, required=True))
        self.add_item(discord.ui.TextInput(label="Bild Link 1", style=discord.TextStyle.short, required=True))
        self.add_item(discord.ui.TextInput(label="Bild Link 2", style=discord.TextStyle.short, required=True))
        self.add_item(discord.ui.TextInput(label="Bild Link 3", style=discord.TextStyle.short, required=True))

    async def on_submit(self, interaction: discord.Interaction):
        if "https://discord.gg/" not in str(self.children[0].value):
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Die Serverinladung muss ein Link sein. Beachte, dass `https://discord.gg/` im Link ist.**", ephemeral=True)
        embed = discord.Embed(title=self.guild.name, beschreibung=self.children[1].value, url=self.children[0].value)
        embed.description += f"\n\n{self.children[2].value}\n{self.children[3].value}\n{self.children[4].value}"
        embed.set_thumbnail(url=self.guild.icon)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        guild = self.bot.get_guild(925729625580113951)
        channel = guild.get_channel(1050746410699603998)
        await channel.send(embed=embed)
        await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Community stimmt nun ab über deinen Server. Du und deine Community kann ebenso amstimmen, damit du vielleicht gewinnst. Die Abstimmung findet dort statt: https://discord.gg/49jD3VXksp.**", ephemeral=True)

class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def teilnehmen(self, interaction: discord.Interaction):
        if interaction.guild.owner != interaction.user:
            return await interaction.response.send_message(f"**<:v_kreuz:1049388811353858069> Tut uns Leid, du bist nicht der Owner vom Server. Diesen Befehl kann nur {interaction.guild.owner.mention} ausführen.**", ephemeral=True)
        await interaction.response.send_modal(Modal(self.bot, interaction.guild))

async def setup(bot):
    await bot.add_cog(event(bot))