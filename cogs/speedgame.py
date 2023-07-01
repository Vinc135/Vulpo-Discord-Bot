import discord
from discord.ext import commands
from discord import app_commands
from info import random_color
import random
import asyncio
import time
from info import getcolour

async def function(self, interaction, farbe, t_1, t_3):
    if self.user.id != interaction.user.id:
        return await interaction.response.defer(thinking=False, ephemeral=True)
    
    if str(self.farbe) != str(farbe):
        embed = discord.Embed(colour=discord.Colour.red(), title="⏱ Teste deine Schnelligkeit", description=f"""
**{interaction.user.mention}, zu ungenau!** 
> Du warst wahrscheinlich zu schnell und hast die falsche Farbe angetippt. Versuche es später noch einmal.""")
        embed.set_thumbnail(url=interaction.user.avatar)
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        return await interaction.message.edit(content="", embed=embed, view=None)

    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT zeit FROM speedgame WHERE userID = (%s)", (interaction.user.id))
            result = await cursor.fetchone()
            t_2 = time.perf_counter()
            t_4 = time.perf_counter()
            time_delta1 = round(((t_2 - t_1) - round(t_4 - t_3)) * 1000)
            time_delta2 = round((t_4 - t_3) * 1000)
            if result is None:
                await cursor.execute("INSERT INTO speedgame(userID, zeit, guildID) VALUES(%s, %s, %s)", (interaction.user.id, time_delta1, interaction.guild.id))
                
                
                embed = discord.Embed(colour=await getcolour(self, interaction.user), title="⏱ Teste deine Schnelligkeit", description=f"""
                                    
`🤖 Gespielt mit einem Ping von {time_delta2}ms`
                        
**{interaction.user.mention}, richtig getippt!** 
> Du hast die richtige Farbe ausgewählt. Deine Zeit liegt bei `{time_delta1}ms`. **Neuer Rekord!**""")
                embed.set_thumbnail(url=interaction.user.avatar)
                embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                return await interaction.message.edit(content="", embed=embed, view=None)
            else:
                if int(result[0]) > int(time_delta1):
                    await cursor.execute("UPDATE speedgame SET zeit = (%s) WHERE userID = (%s)", (time_delta1, interaction.user.id))
                    await cursor.execute("UPDATE speedgame SET guildID = (%s) WHERE userID = (%s)", (interaction.guild.id, interaction.user.id))
                    
                    embed = discord.Embed(colour=await getcolour(self, interaction.user), title="⏱ Teste deine Schnelligkeit", description=f"""
                                        
`🤖 Gespielt mit einem Ping von {time_delta2}ms`
                            
**{interaction.user.mention}, richtig getippt!** 
> Du hast die richtige Farbe ausgewählt. Deine Zeit liegt bei `{time_delta1}ms`. **Neuer Rekord!**""")
                    embed.set_thumbnail(url=interaction.user.avatar)
                    embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                    return await interaction.message.edit(content="", embed=embed, view=None)
                else:
                    
                    embed = discord.Embed(colour=await getcolour(self, interaction.user), title="⏱ Teste deine Schnelligkeit", description=f"""
                                        
`🤖 Gespielt mit einem Ping von {time_delta2}ms`
                            
**{interaction.user.mention}, richtig getippt!** 
> Du hast die richtige Farbe ausgewählt. Deine Zeit liegt bei `{time_delta1}ms`. **Leider kein neuer Rekord.**""")
                    embed.set_thumbnail(url=interaction.user.avatar)
                    embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                    return await interaction.message.edit(content="", embed=embed, view=None)
                
class speedgame_setup(discord.ui.View):
    def __init__(self, bot=None, user: discord.User=None, farbe=None, t_1=None, modus=None):
        super().__init__(timeout=None)
        self.bot = bot
        self.user = user
        self.farbe = farbe
        self.t_1 = t_1
        if modus == "An":
            for item in self.children:
                item.disabled = False
        
        if modus == "Aus":
            for item in self.children:
                item.disabled = True

    @discord.ui.button(emoji="\U000026ab", style=discord.ButtonStyle.grey, custom_id="wegehgegetzhrz5h")
    async def schwarz(self, interaction: discord.Interaction, button: discord.ui.Button):
        await function(self, interaction, ":black_circle:", self.t_1, time.perf_counter())

    @discord.ui.button(emoji="\U0001f535", style=discord.ButtonStyle.grey, custom_id="qergwergwergwe")
    async def blau(self, interaction: discord.Interaction, button: discord.ui.Button):
        await function(self, interaction, ":blue_circle:", self.t_1, time.perf_counter())
    
    @discord.ui.button(emoji="\U0001f7e4", style=discord.ButtonStyle.grey, custom_id="ergqergwrge6h")
    async def braun(self, interaction: discord.Interaction, button: discord.ui.Button):
        await function(self, interaction, ":brown_circle:", self.t_1, time.perf_counter())
    
    @discord.ui.button(emoji="\U0001f7e2", style=discord.ButtonStyle.grey, custom_id="qef67654grwefae")
    async def grün(self, interaction: discord.Interaction, button: discord.ui.Button):
        await function(self, interaction, ":green_circle:", self.t_1, time.perf_counter())
    
    @discord.ui.button(emoji="\U0001f7e0", style=discord.ButtonStyle.grey, custom_id="wrgerthz465wgf")
    async def orange(self, interaction: discord.Interaction, button: discord.ui.Button):
        await function(self, interaction, ":orange_circle:", self.t_1, time.perf_counter())
    
    @discord.ui.button(emoji="\U0001f7e3", style=discord.ButtonStyle.grey, custom_id="w45zezhgrwze5hg")
    async def lila(self, interaction: discord.Interaction, button: discord.ui.Button):
        await function(self, interaction, ":purple_circle:", self.t_1, time.perf_counter())
    
    @discord.ui.button(emoji="\U0001f534", style=discord.ButtonStyle.grey, custom_id="werze456h7weterte")
    async def rot(self, interaction: discord.Interaction, button: discord.ui.Button):
        await function(self, interaction, ":red_circle:", self.t_1, time.perf_counter())
    
    @discord.ui.button(emoji="\U000026aa", style=discord.ButtonStyle.grey, custom_id="rwzegete5he5he5hrtg")
    async def weiss(self, interaction: discord.Interaction, button: discord.ui.Button):
        await function(self, interaction, ":white_circle:", self.t_1, time.perf_counter())
    
    @discord.ui.button(emoji="\U0001f7e1", style=discord.ButtonStyle.grey, custom_id="qregwrgwrgwrgwgwrg")
    async def gelb(self, interaction: discord.Interaction, button: discord.ui.Button):
        await function(self, interaction, ":yellow_circle:", self.t_1, time.perf_counter())
    
    @discord.ui.button(emoji="\U0001f36a", style=discord.ButtonStyle.grey, custom_id="regerthgerthetrhethe")
    async def cookie(self, interaction: discord.Interaction, button: discord.ui.Button):
        await function(self, interaction, ":cookie:", self.t_1, time.perf_counter())
    
                
class Speedgame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=speedgame_setup(self.bot, None, None, None, None))

    speedgame = app_commands.Group(name="speedgame", description="Das Minispiel Speedgame.", guild_only=True)
    
    @speedgame.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id)) 
    async def start(self, interaction: discord.Interaction):
        """Teste deine Schnelligkeit und steige Ränge auf."""
        farben = [":black_circle:", ":blue_circle:", ":brown_circle:", ":green_circle:", ":orange_circle:", ":purple_circle:", ":red_circle:", ":white_circle:", ":yellow_circle:", ":cookie:"]
        farbe = random.choice(farben)
        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="⏱ Teste deine Schnelligkeit", description="")
        embed.set_thumbnail(url=interaction.user.avatar)
        embed.description = f"""
**{interaction.user.mention}, es geht jetzt los, sei schnell und geschickt!** 
> Tippe das Emoji {farbe} an."""
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        await interaction.response.send_message(embed=embed, view=speedgame_setup(self.bot, interaction.user, farbe, time.perf_counter(), "An"))
        
    @speedgame.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id)) 
    async def profil(self, interaction: discord.Interaction, member: discord.Member=None):
        """Zeigt deine Bestzeit."""
        if member == None:
            member = interaction.user
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT zeit FROM speedgame WHERE userID = (%s)", (member.id))
                result = await cursor.fetchone()
                if result == None:
                    if member == interaction.user:
                        return await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Du hast noch kein Match gespielt. Aufgrund dessen hast du auch keine Bestzeit. Du musst zuerst ein Match spielen.**", ephemeral=True)
                    return await interaction.response.send_message(f"**<:v_kreuz:1119580775411621908> {member.mention} hat noch kein Match gespielt. Aufgrund dessen hat er/sie auch keine Bestzeit. Er/Sie muss zuerst ein Match spielen.**", ephemeral=True)
                else:
                    embed = discord.Embed(color=await getcolour(self, interaction.user), title="⚡️ **| __Speedgame Stats__ |** 💨", description=f"""
Aktuelle Stats von {member.mention}
**Bestzeit**: `{result[0]}ms`""")
                    embed.set_thumbnail(url=member.avatar)
                    embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                    await interaction.response.send_message(embed=embed)
                
async def setup(bot):
    await bot.add_cog(Speedgame(bot))