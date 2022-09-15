import discord
from discord.ext import commands
from discord import app_commands
from discord_together import DiscordTogether
import typing

class MakeLink(discord.ui.View):
    def __init__(self, Link: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="Spiel beitreten!", url=Link))

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.cooldown(3, 60, key=lambda i: (i.guild_id, i.user.id))
    async def spielen(self, interaction: discord.Interaction, spiel: typing.Literal["youtube", "poker", "chess", "letter-league", "word-snack", "sketch-heads", "spellcast", "awkword", "checkers", "blazing-8s", "land-io", "putt-party", "bobble-league", "ask-away"]):
        """Spiele im Stream viele Games."""
        if interaction.user.voice == None:
            return await interaction.response.send_message(f"**❌ {interaction.user.mention}, du musst zuerst einem Sprachkanal beitreten.**", ephemeral=True)
        try:
            togetherControl = await DiscordTogether("OTI1Nzk5NTU5NTc2MzIyMDc4.G1pfSR.RNwGXR2kWHPhVs2d6MLFbjL33Q9lHYT7GcnRVU")
            invite_link = await togetherControl.create_link(interaction.user.voice.channel.id, str(spiel))
        except discord.HTTPException:
            return await interaction.response.send_message(f"**❌ {interaction.user.mention}, du musst zuerst einem Sprachkanal beitreten.**", ephemeral=True)
        embed = discord.Embed(title=f"Spiel: {spiel}", description=f"{interaction.user.mention} hat ein Spiel in {interaction.user.voice.channel.mention} gestartet.", color=discord.Color.orange())
        embed.add_field(name="Wie spielt man?", value="Es ist wie ein normales Spiel, bloß in einem Sprachkanal. Schau dich im Sprachkanal nach einem Stream um, das ist das Spiel. Tritt nun dem Stream bei und du kannst anfangen zu spielen.")
        embed.set_thumbnail(url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed, view=MakeLink(invite_link))

async def setup(bot):
    await bot.add_cog(games(bot))