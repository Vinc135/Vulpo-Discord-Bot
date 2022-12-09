import typing
import discord
from discord.ext import commands
from discord import app_commands
#########
class Dropdown(discord.ui.Select):
    def __init__(self, dict=None, id=None):
        selectOptions = []
        self.dict = dict
        for item in dict:
            selectOptions.append(discord.SelectOption(label=item))
        
        super().__init__(placeholder="Wähle Optionen aus", min_values=0, max_values=len(selectOptions), options=selectOptions, custom_id=str(id))
    async def callback(self, interaction: discord.Interaction):
        text = ""
        for item in self.dict:
            rolle = interaction.guild.get_role(int(self.dict[str(item)]))
            if str(item) in self.values:
                if rolle not in interaction.user.roles:
                    await interaction.user.add_roles(rolle)
                    text += f"\n<:v_play:1037065922134945853> Du hast die Rolle {rolle.mention} erhalten."
            else:
                if rolle in interaction.user.roles:
                    await interaction.user.remove_roles(rolle)
                    text += f"\n<:v_play:1037065922134945853> Dir wurde die Rolle {rolle.mention} entzogen."

        if text != "":
            return await interaction.response.send_message(text, ephemeral=True)
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
        emb = interaction.message.embeds[0]
        if emb.fields == []:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du musst zuerst ein paar Optionen festlegen.**", ephemeral=True)
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=discord.Color.orange())
        if self.children[2].value:
            embed.set_thumbnail(url=self.children[2].value)
        if self.children[3].value:
            embed.set_image(url=self.children[3].value)
        
        dict = {}
        id = 0
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT id FROM rr_select")
                result = await cursor.fetchall()
                if result == ():
                    id = 1
                else:
                    id = len(result) + 1
                    
                for field in emb.fields:
                    dict[field.name] = field.value
                    await cursor.execute("INSERT INTO rr_select (label, roleID, guildID, id) VALUES (%s, %s, %s, %s)", (field.name, field.value, interaction.guild.id, id))
                    
        await interaction.message.delete()
        await interaction.channel.send(embed=embed, view=DropdownView(dict, id))
        await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Setup erfolgreich beendet.**", ephemeral=True)
        
class option_hinzufügen(discord.ui.Modal, title="Füge eine Option hinzu"):
    def __init__(self, bot=None):
        self.bot = bot
        super().__init__(custom_id="cgqeifzkwvrefhil")
        self.add_item(discord.ui.TextInput(label="Rollen-ID", style=discord.TextStyle.short, required=True))
        self.add_item(discord.ui.TextInput(label="Spalten-Name", style=discord.TextStyle.short, required=True))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            rolle = interaction.guild.get_role(int(self.children[0].value))
            if rolle == None:
                return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Die Rolle wurde nicht gefunden. Stelle sicher dass es sich um eine Rollen ID gehandelt hat.**", ephemeral=True)
        except:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Die Rolle wurde nicht gefunden. Stelle sicher dass es sich um eine Rollen ID gehandelt hat.**", ephemeral=True)
        embed = interaction.message.embeds[0]
        embed.add_field(name=self.children[1].value, value=rolle.id)
        embed.color = discord.Color.green()
        await interaction.message.edit(content="", embed=embed)
        await interaction.response.send_message("**<:v_haken:1048677657040134195> Option wurde hinzugefügt.**", ephemeral=True)
                
class setup_select(discord.ui.View):
    def __init__(self, bot=None, user=None):
        super().__init__(timeout=None)
        self.bot = bot
        self.user = user

    @discord.ui.button(label="Option hinzufügen", style=discord.ButtonStyle.grey, custom_id="fqefwegwgwrgrtwgrgw", emoji="➕")
    async def eins(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.send_modal(option_hinzufügen(self.bot))

    @discord.ui.button(label="Fertig", style=discord.ButtonStyle.green, custom_id="iuchouflgeiuhvcwoghjdk", emoji="<:v_haken:1048677657040134195>")
    async def zwei(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.send_modal(fertig(self.bot))
    
    @discord.ui.button(label="Abbrechen", style=discord.ButtonStyle.red, custom_id="d3öfihweirhflgkherufk", emoji="🗑")
    async def drei(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.edit_message(content="**<:v_kreuz:1049388811353858069> Vorgang abbgebrochen**", view=None, embed=None)


####################################################################################################


class setup_buttons(discord.ui.View):
    def __init__(self, bot=None, user=None):
        super().__init__(timeout=None)
        self.bot = bot
        self.user = user

    @discord.ui.button(label="Option hinzufügen", style=discord.ButtonStyle.grey, custom_id="aegrtgwrtgrwtgwrt", emoji="➕")
    async def eins(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.send_modal(option_hinzufügen_2(self.bot))

    @discord.ui.button(label="Fertig", style=discord.ButtonStyle.green, custom_id="wrtwrtwrgwrgw4tg", emoji="<:v_haken:1048677657040134195>")
    async def zwei(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.send_modal(fertig2(self.bot))
    
    @discord.ui.button(label="Abbrechen", style=discord.ButtonStyle.red, custom_id="zj56uj4e56wuzat3", emoji="🗑")
    async def drei(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return
        await interaction.response.edit_message(content="**<:v_kreuz:1049388811353858069> Vorgang abbgebrochen**", view=None, embed=None)

class option_hinzufügen_2(discord.ui.Modal, title="Füge eine Option hinzu"):
    def __init__(self, bot=None):
        self.bot = bot
        super().__init__(custom_id="g235gw53gwgewggt53")
        self.add_item(discord.ui.TextInput(label="Rollen-ID", style=discord.TextStyle.short, required=True))
        self.add_item(discord.ui.TextInput(label="Button-Name", style=discord.TextStyle.short, required=True))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            rolle = interaction.guild.get_role(int(self.children[0].value))
            if rolle == None:
                return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Die Rolle wurde nicht gefunden. Stelle sicher dass es sich um eine Rollen ID gehandelt hat.**", ephemeral=True)
        except:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Die Rolle wurde nicht gefunden. Stelle sicher dass es sich um eine Rollen ID gehandelt hat.**", ephemeral=True)
        embed = interaction.message.embeds[0]
        embed.add_field(name=self.children[1].value, value=rolle.id)
        embed.color = discord.Color.green()
        await interaction.message.edit(content="", embed=embed)
        await interaction.response.send_message("**<:v_haken:1048677657040134195> Option wurde hinzugefügt.**", ephemeral=True)

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
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du musst zuerst ein paar Optionen festlegen.**", ephemeral=True)
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=discord.Color.orange())
        if self.children[2].value:
            embed.set_thumbnail(url=self.children[2].value)
        if self.children[3].value:
            embed.set_image(url=self.children[3].value)
        
        id = 0
        custom_id = 0
        view = view_for_buttons()
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT id FROM rr_buttons")
                result = await cursor.fetchall()
                if result == []:
                    id = 1
                    custom_id = 1
                else:
                    id = len(result) + 1
                    custom_id = len(result) + 1
                    
                for field in emb.fields:
                    custom_id += 1
                    view.add_item(item=CounterButton(field.name, field.value, custom_id))
                    await cursor.execute("INSERT INTO rr_buttons (label, roleID, guildID, id, custom_id) VALUES (%s, %s, %s, %s, %s)", (field.name, field.value, interaction.guild.id, id, custom_id))
                    
        await interaction.message.delete()
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Setup erfolgreich beendet.**", ephemeral=True)

class CounterButton(discord.ui.Button):
    def __init__(self, label, role, id):
        super().__init__(label=label, custom_id=str(id))
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        rolle = interaction.guild.get_role(int(self.role))
        if rolle not in interaction.user.roles:
            await interaction.user.add_roles(rolle)
            return await interaction.response.send_message(f"<:v_play:1037065922134945853> Du hast die Rolle {rolle.mention} erhalten.", ephemeral=True)

        if rolle in interaction.user.roles:
            await interaction.user.remove_roles(rolle)
            await interaction.response.send_message(f"<:v_play:1037065922134945853> Dir wurde die Rolle {rolle.mention} entzogen", ephemeral=True)
                
class view_for_buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
class reactionrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=setup_select(self.bot, None))
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT id, label, roleID, guildID FROM rr_select")
                result = await cursor.fetchall()
                if result != []:
                    for i in range(len(result)):
                        dict1 = {}
                        await cursor.execute("SELECT label, roleID, guildID FROM rr_select WHERE id = (%s)", (i))
                        result2 = await cursor.fetchall()
                        if result2 == []:
                            continue
                        for eintrag in result2:
                            dict1[eintrag[0]] = eintrag[1]
                        self.bot.add_view(view=DropdownView(dict1, i))
                ##########
                
                await cursor.execute("SELECT id, label, roleID, guildID, custom_id FROM rr_buttons")
                result = await cursor.fetchall()
                if result != []:
                    for i in range(len(result)):
                        view = view_for_buttons()
                        await cursor.execute("SELECT label, roleID, guildID, custom_id FROM rr_buttons WHERE id = (%s)", (i))
                        result2 = await cursor.fetchall()
                        if result2 == []:
                            continue
                        for eintrag in result2:
                            view.add_item(item=CounterButton(eintrag[0], eintrag[1], eintrag[3]))
                        self.bot.add_view(view=view)
        
    @app_commands.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def reactionrole(self, interaction: discord.Interaction, erscheinungsbild: typing.Literal["Select Menü", "Buttons"]):
        """Lege Reaktionsrollen fest."""
        if erscheinungsbild == "Select Menü":
            embed = discord.Embed(color=discord.Color.gold(), title="Reaktionsrollen Setup", description="Hier kannst du mithilfe von Buttons, Reaktionsrollen dem Select Menü hinzufügen.")
            await interaction.response.send_message(embed=embed, view=setup_select(self.bot, interaction.user))
        if erscheinungsbild == "Buttons":
            embed = discord.Embed(color=discord.Color.gold(), title="Reaktionsrollen Setup", description="Hier kannst du mithilfe von Buttons, Reaktionsrollen als Buttons hinzufügen.")
            await interaction.response.send_message(embed=embed, view=setup_buttons(self.bot, interaction.user))

async def setup(bot):
    await bot.add_cog(reactionrole(bot))