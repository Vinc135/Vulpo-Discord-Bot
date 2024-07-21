import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import getcolour
from utils.MongoDB import getMongoDataBase, getMongoClient

class Modal(discord.ui.Modal, title="Modal"):
    def __init__(self, dict=None, id=None, bot=None):
        super().__init__(custom_id=str(id))
        self.dict = dict
        self.id = id
        self.bot = bot
        for item in dict:
            self.add_item(discord.ui.TextInput(label=item, style=discord.TextStyle.short, required=True, placeholder=dict[item]))

    async def on_submit(self, interaction: discord.Interaction):
        db = getMongoDataBase()
        result = await db['modals'].find_one({"id": self.id, "guildID": interaction.guild.id})
        if result:
            channel = interaction.guild.get_channel(int(result['channelID']))
            if channel:
                embed = discord.Embed(color=await getcolour(self, interaction.user), title="Neues Formular", description=f"Das Formular wurde gesendet von {interaction.user.mention} ({interaction.user.id}).")
                for answer in self.children:
                    embed.add_field(name=answer.label, value=answer.value, inline=False)
                embed.set_thumbnail(url=interaction.user.avatar.url)
                
                await channel.send(embed=embed)
                await interaction.response.send_message("**<:v_158:1264268251916009553> Dein Formular wurde gesendet.**", ephemeral=True)
            else:
                await interaction.response.send_message("**<:v_9:1264264656831119462> Der festgelegte Kanal zum Senden der Formulare existiert nicht mehr. Bitte informiere einen Admin.**", ephemeral=True)

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
        if not emb.fields:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du musst zuerst ein paar Optionen festlegen.**", ephemeral=True)
        
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=await getcolour(self, interaction.user))
        if self.children[2].value:
            embed.set_thumbnail(url=self.children[2].value)
        if self.children[3].value:
            embed.set_image(url=self.children[3].value)
        
        dict = {}
        db = getMongoDataBase()
        result4 = await db["modals"].find().sort([("id", -1)]).limit(1).to_list(length=1)
        summe = f"{int(result4[0]['id'].replace('modal', '')) + 1}modal" if result4 else "1modal"

        for field in emb.fields:
            dict[field.name] = field.value
            await db["modals"].insert_one({"label": field.name, "beschreibung": field.value, "guildID": interaction.guild.id, "id": summe, "channelID": self.kanal})
        
        await interaction.message.delete()
        await interaction.channel.send(embed=embed, view=CounterButtonView(dict, summe, self.bot))
        await interaction.response.send_message(f"**<:v_158:1264268251916009553> Setup erfolgreich beendet.**", ephemeral=True)

class frage_hinzufügen(discord.ui.Modal, title="Füge eine Frage hinzu"):
    def __init__(self, bot=None):
        self.bot = bot
        super().__init__(custom_id="cgqeifzkwvrefhil")
        self.add_item(discord.ui.TextInput(label="Frage", style=discord.TextStyle.short, required=True))
        self.add_item(discord.ui.TextInput(label="Kurze Beschreibung", style=discord.TextStyle.short, required=True))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            embed = interaction.message.embeds[0]
            embed.add_field(name=self.children[0].value, value=self.children[1].value)
            embed.color = await getcolour(self, interaction.user)
            await interaction.message.edit(content="", embed=embed)
            await interaction.response.send_message("**<:v_158:1264268251916009553> Frage wurde hinzugefügt.**", ephemeral=True)
        except:
            await interaction.response.send_message("❌ Dein angegebener Text ist zu lang.")
                
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

    @discord.ui.button(label="Fertig", style=discord.ButtonStyle.green, custom_id="egwrgwrgwrgwrt", emoji="<:v_158:1264268251916009553>")
    async def zwei(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.send_modal(fertig(self.bot, self.kanal))
    
    @discord.ui.button(label="Abbrechen", style=discord.ButtonStyle.red, custom_id="trhetzurturzjhrzt", emoji="🗑")
    async def drei(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.edit_message(content="**<:v_9:1264264656831119462> Vorgang abbgebrochen**", view=None, embed=None)
    
class modal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=setup_select(self.bot, None))
        db = getMongoDataBase()
        results = await db['modals'].find().to_list(length=None)
        for result in results:
            dict1 = {}
            id = result['id']
            result2 = await db['modals'].find({"id": id}).to_list(length=None)
            if not result2:
                continue
            for entry in result2:
                dict1[entry['label']] = entry['beschreibung']
            self.bot.add_view(view=CounterButtonView(dict1, id, self.bot))
                                                
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def modal(self, interaction: discord.Interaction, empfangskanal: discord.TextChannel):
        """Erstelle Modals."""
        await interaction.response.defer()
        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Modal Setup", description="Hier kannst du mithilfe von Buttons, Fragen zum Modal hinzufügen.")
        
        await interaction.followup.send(embed=embed, view=setup_select(self.bot, interaction.user, empfangskanal.id))

async def setup(bot):
    await bot.add_cog(modal(bot))
