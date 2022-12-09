import discord
from discord.ext import commands
from discord import app_commands

class button(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Loslegen', style=discord.ButtonStyle.grey, custom_id="fwerfgwgw4gwgwrtgfw", emoji="<:v_haken:1048677657040134195>")
    async def loslegen(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Modal(self.bot))

class Modal(discord.ui.Modal, title="Formular"):
    def __init__(self, bot=None):
        super().__init__(custom_id="dheiwdgouewhvifdzg3eviuh")
        self.bot = bot
        self.add_item(discord.ui.TextInput(label="Einladung zum Server", style=discord.TextStyle.short, required=True))
        self.add_item(discord.ui.TextInput(label="Server Beschreibung", style=discord.TextStyle.long, required=True))
        self.add_item(discord.ui.TextInput(label="Bild Link", style=discord.TextStyle.short, required=False))

    async def on_submit(self, interaction: discord.Interaction):
        if "https://discord.gg/" not in str(self.children[0].value):
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Die Serverinladung muss ein Link sein. Beachte, dass `https://discord.gg/` im Link ist.**", ephemeral=True)
        embed = discord.Embed(title=interaction.guild.name, description=self.children[1].value, url=self.children[0].value)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_image(url=self.children[2].value if self.children[2].value else interaction.guild.banner)
        embed.description += f"\n\n{interaction.guild.member_count} Mitglieder"
        embed.color = discord.Color.orange()
        guild = self.bot.get_guild(925729625580113951)
        channel = guild.get_channel(1050746410699603998)
        await channel.send(embed=embed)
        await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Community stimmt nun ab über deinen Server. Du und deine Community kann ebenso amstimmen, damit du vielleicht gewinnst. Die Abstimmung findet dort statt: https://discord.gg/49jD3VXksp.**", ephemeral=True)

class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def teilnehmen(self, interaction: discord.Interaction):
        """Nimm am riesen Event Teil!!!"""
        if interaction.guild.owner != interaction.user:
            return await interaction.response.send_message(f"**<:v_kreuz:1049388811353858069> Tut uns Leid, du bist nicht der Owner vom Server. Diesen Befehl kann nur {interaction.guild.owner.mention} ausführen.**", ephemeral=True)
        if int(interaction.guild.member_count) < 100:
            return await interaction.response.send_message(f"**<:v_kreuz:1049388811353858069> Tut uns Leid, dein Server ist zu klein. Du brauchst mindestens 100 Mitglieder.**", ephemeral=True)
        await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Tipp: Nachdem du auf den Button gedrückt hast und schon etwas ausgefüllt hast, dir aber etwas fehlt kannst du einfach raus gehen. Die Texte von dir im Modal bleiben solange dort, bis du es abschickst.**", ephemeral=True, view=button(self.bot))

async def setup(bot):
    await bot.add_cog(event(bot))