import discord
from discord.ext import commands
from discord import app_commands
from info import getcolour
#########
class Modal(discord.ui.Modal, title="Modal"):
    def __init__(self, dict=None, id=None, bot=None):
        super().__init__(custom_id=str(id))
        self.dict = dict
        self.id = id
        self.bot = bot
        for item in dict:
            self.add_item(discord.ui.TextInput(label=item, style=discord.TextStyle.short, required=True, placeholder=dict[item]))

    async def on_submit(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT channelID FROM modals WHERE id = (%s) AND guildID = (%s)", (self.id, interaction.guild.id))
                result = await cursor.fetchone()
                channel = interaction.guild.get_channel(int(result[0]))
                if channel:
                    embed = discord.Embed(color=await getcolour(self, interaction.user), title="Neues Formular", description=f"Das Formular wurde gesendet von {interaction.user.mention} ({interaction.user.id}).")
                    for answer in self.children:
                        embed.add_field(name=answer.label, value=answer.value, inline=False)
                    embed.set_thumbnail(url=interaction.user.avatar)
                    await channel.send(embed=embed)
                    await interaction.response.send_message("**<:v_haken:1048677657040134195> Dein Formular wurde gesendet.**", ephemeral=True)
                else:
                    return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Der festgelegte Kanal zum Senden der Formulare existiert nicht mehr. Bitte informiere einen Admin.**", ephemeral=True)

class CounterButton(discord.ui.Button):
    def __init__(self, dict=None, id=None, bot=None):
        super().__init__(label="Modal anzeigen", custom_id=str(id))
        self.dict = dict
        self.id = id
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Modal(self.dict, self.id, self.bot))

class CounterButtonView(discord.ui.View):
    def __init__(self, dict=None, id=None, bot=None):
        super().__init__(timeout=None)
        self.add_item(CounterButton(dict, id, bot))
        
class fertig(discord.ui.Modal, title="Erstelle ein Embed"):
    def __init__(self, bot=None, kanal=None):
        self.bot = bot
        self.kanal = kanal
        super().__init__(custom_id="sdcdfvdgsrgw")
        self.add_item(discord.ui.TextInput(label="Embed Titel", style=discord.TextStyle.short, required=True))
        self.add_item(discord.ui.TextInput(label="Embed Beschreibung", style=discord.TextStyle.short, required=True))
        self.add_item(discord.ui.TextInput(label="Embed Thumbnail", style=discord.TextStyle.short, required=False))
        self.add_item(discord.ui.TextInput(label="Embed Image", style=discord.TextStyle.short, required=False))

    async def on_submit(self, interaction: discord.Interaction):
        emb = interaction.message.embeds[0]
        if emb.fields == []:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du musst zuerst ein paar Optionen festlegen.**", ephemeral=True)
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=await getcolour(self, interaction.user))
        if self.children[2].value:
            embed.set_thumbnail(url=self.children[2].value)
        if self.children[3].value:
            embed.set_image(url=self.children[3].value)
        
        dict = {}
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT id FROM modals")
                result4 = await cursor.fetchall()
                if result4 == ():
                    summe = "1modal"
                else:
                    summe = f"{int(str(result4[len(result4) - 1][0]).replace('modal', '')) + 1}modal"
                    
                for field in emb.fields:
                    dict[field.name] = field.value
                    await cursor.execute("INSERT INTO modals (label, beschreibung, guildID, id, channelID) VALUES (%s, %s, %s, %s, %s)", (field.name, field.value, interaction.guild.id, summe, self.kanal))
                    
        await interaction.message.delete()
        await interaction.channel.send(embed=embed, view=CounterButtonView(dict, summe, self.bot))
        await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Setup erfolgreich beendet.**", ephemeral=True)
        
class frage_hinzufügen(discord.ui.Modal, title="Füge eine Frage hinzu"):
    def __init__(self, bot=None):
        self.bot = bot
        super().__init__(custom_id="cgqeifzkwvrefhil")
        self.add_item(discord.ui.TextInput(label="Frage", style=discord.TextStyle.short, required=True))
        self.add_item(discord.ui.TextInput(label="Kurze Beschreibung", style=discord.TextStyle.short, required=True))

    async def on_submit(self, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        embed.add_field(name=self.children[0].value, value=self.children[1].value)
        embed.color = await getcolour(self, interaction.user)
        await interaction.message.edit(content="", embed=embed)
        await interaction.response.send_message("**<:v_haken:1048677657040134195> Frage wurde hinzugefügt.**", ephemeral=True)
                
class setup_select(discord.ui.View):
    def __init__(self, bot=None, user=None, kanal=None):
        super().__init__(timeout=None)
        self.bot = bot
        self.user = user
        self.kanal = kanal

    @discord.ui.button(label="Frage hinzufügen", style=discord.ButtonStyle.grey, custom_id="ergwrtgwrtgwrtg", emoji="➕")
    async def eins(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.send_modal(frage_hinzufügen(self.bot))

    @discord.ui.button(label="Fertig", style=discord.ButtonStyle.green, custom_id="egwrgwrgwrgwrt", emoji="<:v_haken:1048677657040134195>")
    async def zwei(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.send_modal(fertig(self.bot, self.kanal))
    
    @discord.ui.button(label="Abbrechen", style=discord.ButtonStyle.red, custom_id="trhetzurturzjhrzt", emoji="🗑")
    async def drei(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.edit_message(content="**<:v_kreuz:1049388811353858069> Vorgang abbgebrochen**", view=None, embed=None)
    
class modal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=setup_select(self.bot, None))
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT id, label, beschreibung, guildID FROM modals")
                result = await cursor.fetchall()
                if result != []:
                    for i in range(len(result)):
                        dict1 = {}
                        await cursor.execute("SELECT label, beschreibung, guildID FROM modals WHERE id = (%s)", (f"{i}modal"))
                        result2 = await cursor.fetchall()
                        if result2 == []:
                            continue
                        for eintrag in result2:
                            dict1[eintrag[0]] = eintrag[1]
                        
                        self.bot.add_view(view=CounterButtonView(dict1, f"{i}modal", self.bot))
                                                
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def modal(self, interaction: discord.Interaction, empfangskanal: discord.TextChannel):
        """Erstelle Modals."""
        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Modal Setup", description="Hier kannst du mithilfe von Buttons, Fragen zum Modal hinzufügen.")
        await interaction.response.send_message(embed=embed, view=setup_select(self.bot, interaction.user, empfangskanal.id))

async def setup(bot):
    await bot.add_cog(modal(bot))