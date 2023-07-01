import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from info import getcolour

class Dropdown(discord.ui.Select):
    def __init__(self, bot, selectOptions):
        super().__init__(placeholder="Welcher Server soll einen Punkt dazu bekommen?", min_values=1, max_values=1, options=selectOptions, custom_id="Dropdown-Help")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT timestamp FROM event_lastvote WHERE userID = (%s)", (interaction.user.id))
                result = await cursor.fetchone()
                now = datetime.now()
                if result is not None:
                    last_claim_stamp = result[0]
                    last_claim = datetime.fromtimestamp(float(last_claim_stamp))
                    delta = now - last_claim
                    if delta < timedelta(hours=12):
                        return await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Du kannst nur alle 12 Stunden abstimmen. Gedulde dich noch etwas.**", ephemeral=True)
                    else:
                        await cursor.execute("SELECT * FROM event WHERE guildNAME = (%s)", (self.values[0]))
                        r = await cursor.fetchone()
                        await cursor.execute("UPDATE event SET votes = (%s) WHERE guildID = (%s)", (int(r[2]) + 1, r[1]))
                        await cursor.execute("UPDATE event_lastvote SET timestamp = (%s) WHERE userID = (%s)", (str(now.timestamp()), interaction.user.id))
                        await interaction.response.send_message(f"Du hast abgestimmt für {self.values[0]}. Komm in 12 Stunden wieder, um nochmal zu voten.", ephemeral=True)
                if result is None:
                    await cursor.execute("SELECT * FROM event WHERE guildNAME = (%s)", (self.values[0]))
                    r = await cursor.fetchone()
                    await cursor.execute("UPDATE event SET votes = (%s) WHERE guildID = (%s)", (int(r[2]) + 1, r[1]))
                    await cursor.execute("INSERT INTO event_lastvote(userID, timestamp) VALUES(%s, %s)", (interaction.user.id, str(now.timestamp())))
                    await interaction.response.send_message(f"Du hast abgestimmt für {self.values[0]}. Komm in 12 Stunden wieder, um nochmal zu voten.", ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self, bot, selectOptions):
        super().__init__(timeout=None)
        self.add_item(Dropdown(bot, selectOptions))

class abstimmen(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Abstimmen', style=discord.ButtonStyle.grey, custom_id="lkdfqeifouwifb", emoji="<:v_haken:1119579684057907251>")
    async def abstimmen(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT timestamp FROM event_lastvote WHERE userID = (%s)", (interaction.user.id))
                result = await cursor.fetchone()
                now = datetime.now()
                selectOptions = []
                channel = self.bot.get_channel(1072146223605223424)
                async for msg in channel.history(oldest_first=True):
                    embed = msg.embeds[0]
                    guildNAME = embed.title
                    selectOptions.append(discord.SelectOption(label=guildNAME))

                if result is not None:
                    last_claim_stamp = result[0]
                    last_claim = datetime.fromtimestamp(float(last_claim_stamp))
                    delta = now - last_claim
                    if delta > timedelta(hours=12):
                        await interaction.response.send_message("**Du kannst abstimmen.**", view=DropdownView(self.bot, selectOptions), ephemeral=True)
                    else:
                        await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Du kannst nur alle 12 Stunden abstimmen. Gedulde dich noch etwas.**", ephemeral=True)
                if result is None:
                    await interaction.response.send_message("**Du kannst abstimmen.**", view=DropdownView(self.bot, selectOptions), ephemeral=True)


class button(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Loslegen', style=discord.ButtonStyle.grey, custom_id="fwerfgwgw4gwgwrtgfw", emoji="<:v_haken:1119579684057907251>")
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
            return await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Die Servereinladung muss ein Link sein. Beachte, dass `https://discord.gg/` im Link ist.**", ephemeral=True)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT votes FROM event WHERE guildID = (%s)", (interaction.guild.id))
                result = await cursor.fetchone()
                if result:
                    return await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Dieser Server nimmt bereits teil.**", ephemeral=True)
                else:
                    await cursor.execute("INSERT INTO event(guildID, votes, guildNAME, invite, beschreibung, bild) VALUES(%s, %s, %s, %s, %s, %s)", (interaction.guild.id, 0, interaction.guild.name, self.children[0].value, self.children[1].value, self.children[2].value))
                    channel = self.bot.get_channel(1072146041736019978)
                    msg = await channel.fetch_message(1072146165170196490)
                    await msg.edit(view=abstimmen(self.bot))

                    embed = discord.Embed(title=interaction.guild.name, description=self.children[1].value, url=self.children[0].value)
                    embed.set_thumbnail(url=interaction.guild.icon)
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    embed.set_image(url=self.children[2].value if self.children[2].value else interaction.guild.banner)
                    embed.set_footer(text=interaction.guild.id)
                    embed.description += f"\n\n{interaction.guild.member_count} Mitglieder"
                    embed.color = discord.Color.orange()
                    c = self.bot.get_channel(1072146223605223424)
                    await c.send(embed=embed)
                    await interaction.response.send_message("**<:v_haken:1119579684057907251> Die Community stimmt nun ab über deinen Server. Du und deine Community kann ebenso amstimmen, damit du vielleicht gewinnst. Die Abstimmung findet dort statt: https://discord.gg/49jD3VXksp.**", ephemeral=True)
                    
class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=abstimmen(self.bot))

    @app_commands.command()
    @app_commands.guild_only()
    async def teilnehmen(self, interaction: discord.Interaction):
        """Nimm am Event teil."""
        if interaction.guild.owner != interaction.user:
            return await interaction.response.send_message(f"**<:v_kreuz:1119580775411621908> Tut uns Leid, du bist nicht der Owner vom Server. Diesen Befehl kann nur {interaction.guild.owner.mention} ausführen.**", ephemeral=True)
        if int(interaction.guild.member_count) < 10:
            return await interaction.response.send_message(f"**<:v_kreuz:1119580775411621908> Tut uns Leid, dein Server ist zu klein. Du brauchst mindestens 10 Mitglieder.**", ephemeral=True)
        await interaction.response.send_message(f"**<:v_haken:1119579684057907251> Tipp: Nachdem du auf den Button gedrückt hast und schon etwas ausgefüllt hast, dir aber etwas fehlt kannst du einfach raus gehen. Die Texte von dir im Modal bleiben solange dort, bis du es abschickst.**", ephemeral=True, view=button(self.bot))

async def setup(bot):
    await bot.add_cog(event(bot))