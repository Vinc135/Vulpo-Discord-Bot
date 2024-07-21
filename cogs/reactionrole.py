import typing
import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import getcolour, haspremium_forserver
from utils.MongoDB import getMongoDataBase
#########

class Dropdown(discord.ui.Select):
    def __init__(self, dict=None, id=None):
        selectOptions = []
        self.dict = dict
        for item in dict:
            selectOptions.append(discord.SelectOption(label=item))
        
        super().__init__(placeholder="Wähle Optionen aus", min_values=0, max_values=len(selectOptions), options=selectOptions, custom_id=str(id))
    async def callback(self, interaction: discord.Interaction):
        
        await interaction.response.defer()
        
        text = ""
        for item in self.dict:
            rolle = interaction.guild.get_role(int(self.dict[str(item)]))
            if str(item) in self.values:
                if rolle not in interaction.user.roles:
                    await interaction.user.add_roles(rolle)
                    text += f"\n<:v_24:1264264867511144479> Du hast die Rolle {rolle.mention} erhalten."
            else:
                if rolle in interaction.user.roles:
                    await interaction.user.remove_roles(rolle)
                    text += f"\n<:v_24:1264264867511144479> Dir wurde die Rolle {rolle.mention} entzogen."

        if text != "":
            return await interaction.followup.send(text, ephemeral=True)
        await interaction.response.defer(thinking=False, ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self, dict=None, id=None):
        super().__init__(timeout=None)
        self.add_item(Dropdown(dict,id))
        
class fertig(discord.ui.Modal, title="Erstelle ein Embed"):
    def __init__(self, bot=None):
        self.bot = bot
        super().__init__(custom_id="cgqeifzkwvrefhil")
        self.add_item(discord.ui.TextInput(label="Embed Titel", style=discord.TextStyle.short, required=True))
        self.add_item(discord.ui.TextInput(label="Embed Beschreibung", style=discord.TextStyle.long, required=True))
        self.add_item(discord.ui.TextInput(label="Embed Thumbnail", style=discord.TextStyle.short, required=False))
        self.add_item(discord.ui.TextInput(label="Embed Image", style=discord.TextStyle.short, required=False))

    async def on_submit(self, interaction: discord.Interaction):
        
        await interaction.response.defer()
        
        emb = interaction.message.embeds[0]
        if emb.fields == []:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du musst zuerst ein paar Optionen festlegen.**", ephemeral=True)
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=await getcolour(self, interaction.user))
        
        if self.children[2].value:
            embed.set_thumbnail(url=self.children[2].value)
        if self.children[3].value:
            embed.set_image(url=self.children[3].value)
        
        dict = {}
        id = 0
        
        db = getMongoDataBase()
        
        id = await db['rr_select'].count_documents({}) + 1
            
        for field in emb.fields:
            dict[field.name] = field.value
            await db['rr_select'].insert_one({"label": field.name, "roleID": field.value, "guildID": interaction.guild.id, "id": id})
                    
        await interaction.message.delete()
        await interaction.channel.send(embed=embed, view=DropdownView(dict, id))
        await interaction.followup.send(f"**<:v_158:1264268251916009553> Setup erfolgreich beendet.**", ephemeral=True)

class select_role1(discord.ui.RoleSelect):
    def __init__(self, bot=None):
        super().__init__(placeholder="Wähle eine Rolle aus", min_values=0, max_values=1, custom_id="lkefgdouehifohbek")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(option_hinzufügen(self.bot, self.values[0].id))
 
class option_hinzufügen(discord.ui.Modal, title="Füge eine Option hinzu"):
    def __init__(self, bot=None, roleID=None):
        self.bot = bot
        self.roleID = roleID
        super().__init__(custom_id="cgqeifzkwvrefhil")
        self.add_item(discord.ui.TextInput(label="Spalten-Name", style=discord.TextStyle.short, required=True))

    async def on_submit(self, interaction: discord.Interaction):
        
        await interaction.response.defer()
        
        embed = interaction.message.embeds[0]
        
        premium_status = await haspremium_forserver(self, interaction.guild)
        
        if premium_status == False and len(embed.fields) >= 3:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du kannst keine weiteren Optionen erstellen, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")

        embed.add_field(name=self.children[0].value, value=self.roleID)
        embed.color = await getcolour(self, interaction.user)
        await interaction.message.edit(content="", embed=embed)
        await interaction.followup.send("**<:v_158:1264268251916009553> Option wurde hinzugefügt.**", ephemeral=True)
                
class setup_select(discord.ui.View):
    def __init__(self, bot=None, user=None):
        super().__init__(timeout=None)
        self.bot = bot
        self.user = user

    @discord.ui.button(label="Fertig", style=discord.ButtonStyle.green, custom_id="iuchouflgeiuhvcwoghjdk", emoji="<:v_158:1264268251916009553>")
    async def zwei(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.send_modal(fertig(self.bot))
    
    @discord.ui.button(label="Abbrechen", style=discord.ButtonStyle.red, custom_id="d3öfihweirhflgkherufk", emoji="🗑")
    async def drei(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.edit_message(content="**<:v_9:1264264656831119462> Vorgang abbgebrochen**", view=None, embed=None)


####################################################################################################

class select_role2(discord.ui.RoleSelect):
    def __init__(self, bot=None):
        super().__init__(placeholder="Wähle eine Rolle aus", min_values=0, max_values=1, custom_id="lkefgdouehifohbek")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(option_hinzufügen_2(self.bot, self.values[0].id))

class setup_buttons(discord.ui.View):
    def __init__(self, bot=None, user=None):
        super().__init__(timeout=None)
        self.bot = bot
        self.user = user

    @discord.ui.button(label="Fertig", style=discord.ButtonStyle.green, custom_id="wrtwrtwrgwrgw4tg", emoji="<:v_158:1264268251916009553>")
    async def zwei(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.send_modal(fertig2(self.bot))
    
    @discord.ui.button(label="Abbrechen", style=discord.ButtonStyle.red, custom_id="zj56uj4e56wuzat3", emoji="🗑")
    async def drei(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.edit_message(content="**<:v_9:1264264656831119462> Vorgang abbgebrochen**", view=None, embed=None)

class option_hinzufügen_2(discord.ui.Modal, title="Füge eine Option hinzu"):
    def __init__(self, bot=None, roleID=None):
        self.bot = bot
        self.roleID = roleID
        super().__init__(custom_id="g235gw53gwgewggt53")
        self.add_item(discord.ui.TextInput(label="Button-Name", style=discord.TextStyle.short, required=True))

    async def on_submit(self, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        
        premium_status = await haspremium_forserver(self, interaction.guild)
        
        if premium_status == False and len(embed.fields) >= 3:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du kannst keine weiteren Optionen erstellen, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")

        embed.add_field(name=self.children[0].value, value=self.roleID)
        embed.color = await getcolour(self, interaction.user)
        await interaction.message.edit(content="", embed=embed)
        await interaction.followup.send("**<:v_158:1264268251916009553> Option wurde hinzugefügt.**", ephemeral=True)

class fertig2(discord.ui.Modal, title="Erstelle ein Embed"):
    def __init__(self, bot=None):
        self.bot = bot
        super().__init__(custom_id="gwtgwgte4wg34f")
        self.add_item(discord.ui.TextInput(label="Embed Titel", style=discord.TextStyle.short, required=True))
        self.add_item(discord.ui.TextInput(label="Embed Beschreibung", style=discord.TextStyle.long, required=True))
        self.add_item(discord.ui.TextInput(label="Embed Thumbnail", style=discord.TextStyle.short, required=False))
        self.add_item(discord.ui.TextInput(label="Embed Image", style=discord.TextStyle.short, required=False))

    async def on_submit(self, interaction: discord.Interaction):
        emb = interaction.message.embeds[0]
        if emb.fields == []:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du musst zuerst ein paar Optionen festlegen.**", ephemeral=True)
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=await getcolour(self, interaction.user))
        
        if self.children[2].value:
            embed.set_thumbnail(url=self.children[2].value)
        if self.children[3].value:
            embed.set_image(url=self.children[3].value)
        
        id = 0
        custom_id = 0
        view = view_for_buttons()
        
        db = getMongoDataBase()
        
        id = await db['rr_buttons'].count_documents({}) + 1
            
        for field in emb.fields:
            custom_id += 1
            view.add_item(item=CounterButton(field.name, field.value, custom_id))
            await db['rr_buttons'].insert_one({"label": field.name, "roleID": field.value, "guildID": interaction.guild.id, "id": id, "custom_id": custom_id})
                    
        await interaction.message.delete()
        await interaction.channel.send(embed=embed, view=view)
        await interaction.followup.send(f"**<:v_158:1264268251916009553> Setup erfolgreich beendet.**", ephemeral=True)

class CounterButton(discord.ui.Button):
    def __init__(self, label, role, id):
        super().__init__(label=label, custom_id=str(id))
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        rolle = interaction.guild.get_role(int(self.role))
        if rolle not in interaction.user.roles:
            await interaction.user.add_roles(rolle)
            return await interaction.followup.send(f"<:v_24:1264264867511144479> Du hast die Rolle {rolle.mention} erhalten.", ephemeral=True)

        if rolle in interaction.user.roles:
            await interaction.user.remove_roles(rolle)
            await interaction.followup.send(f"<:v_24:1264264867511144479> Dir wurde die Rolle {rolle.mention} entzogen", ephemeral=True)
                
class view_for_buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
class reactionrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=setup_select(self.bot, None))
        
        db = getMongoDataBase()
        
        result = await db['rr_select'].find().to_list(length=None)
        if result != []:
            i = 0
            for a in result:
                i += 1
                dict1 = {}
                result2 = await db['rr_select'].find_one({"id": i})
                if result2 == []:
                    continue
                for eintrag in result2:
                    dict1[eintrag[0]] = eintrag[1]
                self.bot.add_view(view=DropdownView(dict1, i))
        
        result = await db["rr_buttons"].find({}).to_list(length=None)
        
        if len(result) != 0:
            i = 0
            for a in result:
                i += 1
                view = view_for_buttons()
                result2 = await db["rr_buttons"].find_one({"id": i})
                if result2 == []:
                    continue
                for eintrag in result2:
                    view.add_item(item=CounterButton(eintrag[0], eintrag[1], eintrag[3]))
                self.bot.add_view(view=view)
        
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def reactionrole(self, interaction: discord.Interaction, erscheinungsbild: typing.Literal["Select Menü", "Buttons"]):
        """Lege Reaktionsrollen fest."""
        
        await interaction.response.defer()
        
        if erscheinungsbild == "Select Menü":
            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Reaktionsrollen Setup", description="Hier kannst du mithilfe von Buttons, Reaktionsrollen dem Select Menü hinzufügen.")
            
            view = setup_select(self.bot, interaction.user)
            view.add_item(select_role1(self.bot))
            await interaction.followup.send(embed=embed, view=view)
        if erscheinungsbild == "Buttons":
            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Reaktionsrollen Setup", description="Hier kannst du mithilfe von Buttons, Reaktionsrollen als Buttons hinzufügen.")
            
            view = setup_buttons(self.bot, interaction.user)
            view.add_item(select_role2(self.bot))
            await interaction.followup.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(reactionrole(bot))