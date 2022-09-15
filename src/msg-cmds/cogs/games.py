import discord
from discord.ext import commands
from info import get_syntax
from discord_together import DiscordTogether

async def tC():
    return await DiscordTogether("VULP0123456787654321")

class MakeLink(discord.ui.View):
    def __init__(self, Link: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="Spiel beitreten!", url=Link))

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="<sketch, youtube, poker, chess, betrayal, fishing, letter-league, word-snack, sketch-heads, spellcast, awkword, checkers>")
    async def play(self, ctx, spiel=None):
        """Spiele im Stream viele Games."""
        if spiel is None:
            return await get_syntax(ctx)
        if spiel == "sketch" or spiel == "youtube" or spiel == "poker" or spiel == "chess" or spiel == "betrayal" or spiel == "fishing" or spiel == "letter-league" or spiel == "word-snack" or spiel == "sketch-heads" or spiel == "spellcast" or spiel == "awkword":
            if ctx.author.voice == None:
                return await ctx.send(f"**❌ {ctx.author.mention}, du musst zuerst einem Sprachkanal beitreten.**")
            try:
                togetherControl = await tC()
                invite_link = togetherControl.create_link(ctx.author.voice.channel.id, str(spiel))
            except discord.HTTPException:
                return await ctx.send(f"**❌ {ctx.author.mention}, du musst zuerst einem Sprachkanal beitreten.**")
            embed = discord.Embed(title=f"Spiel: {spiel}", description=f"{ctx.author.mention} hat ein Spiel in {ctx.author.voice.channel.mention} gestartet.", color=discord.Color.orange())
            embed.add_field(name="Wie spielt man?", value="Es ist wie ein normales Spiel, bloß in einem Sprachkanal. Schau dich im Sprachkanal nach einem Stream um, das ist das Spiel. Tritt nun dem Stream bei und du kannst anfangen zu spielen.")
            await ctx.send(embed=embed, view=MakeLink(invite_link))
        else:
            return await get_syntax(ctx)

async def setup(bot):
    await bot.add_cog(games(bot))