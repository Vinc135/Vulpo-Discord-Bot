import datetime
import typing
import discord
from discord.ext import commands
import random
from discord import app_commands
from easy_pil import Editor, load_image_async, Font
from utils.utils import getcolour
from utils.MongoDB import getMongoDataBase


class Willkommensnachricht(discord.ui.Modal, title="Willkommensnachricht"):
    def __init__(self, kanal: discord.TextChannel=None, bot=None, alte_nachricht: str=None):
        super().__init__(custom_id="wWk766We676e6Wwe274kwW")
        self.kanal = kanal
        self.bot = bot
        self.alte_nachricht = alte_nachricht
        self.add_item(discord.ui.TextInput(label="Nachricht", style=discord.TextStyle.paragraph, required=True, placeholder="%member-Member#0000 | %name-Member | %mention-@Member | %guild-Servername | %usercount-Memberanzahl", default=str(self.alte_nachricht).replace("B9xV123", "")))
        self.add_item(discord.ui.TextInput(label="Mit Willkommens-Bild?", style=discord.TextStyle.short, required=True, placeholder="Antworte mit 'Ja' oder 'Nein'."))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        db = getMongoDataBase()
        
        if str(self.alte_nachricht) == "%member-Member#0000 | %name-Member | %mention-@Member | %guild-Servername | %usercount-Memberanzahl":
            if str(self.children[1].value).lower() == "ja":
                await db['welcome'].insert_one({"guildID": str(interaction.guild.id), "channelID": self.kanal.id, "msg": f"{self.children[0].value} B9xV123"})
                return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Willkommensnachricht ist nun aktiv.**")
            if str(self.children[1].value).lower() == "nein":
                await db['welcome'].insert_one({"guildID": str(interaction.guild.id), "channelID": self.kanal.id, "msg": f"{self.children[0].value}"})
                return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Willkommensnachricht ist nun aktiv.**")
            else:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Gib beim nächsten Mal deine Antwort beim Feld '**Mit Bild?**' mit einem klaren 'Ja' oder 'Nein' wider.**", ephemeral=True)
                    
                
        if str(self.children[1].value).lower() == "ja":
            await db['welcome'].update_one({"guildID": str(interaction.guild.id)}, {"$set": {"channelID": self.kanal.id, "msg": f"{self.children[0].value} B9xV123"}})
            return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Willkommensnachricht ist nun geändert.**")
        if str(self.children[1].value).lower() == "nein":
            await db['welcome'].update_one({"guildID": str(interaction.guild.id)}, {"$set": {"channelID": self.kanal.id, "msg": f"{self.children[0].value}"}})
            return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Willkommensnachricht ist nun geändert.**")
        else:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Gib beim nächsten Mal deine Antwort beim Feld '**Mit Bild?**' mit einem klaren 'Ja' oder 'Nein' wider.**", ephemeral=True)
                

class Verlassensnachricht(discord.ui.Modal, title="Verlassensnachricht"):
    def __init__(self, kanal: discord.TextChannel=None, bot=None, alte_nachricht: str=None):
        super().__init__(custom_id="2Byyy55BNyly55lylm5ml2")
        self.kanal = kanal
        self.bot = bot
        self.alte_nachricht = alte_nachricht
        self.add_item(discord.ui.TextInput(label="Nachricht", style=discord.TextStyle.paragraph, required=True, placeholder="%member-Member#0000 | %name-Member | %mention-@Member | %guild-Servername | %usercount-Memberanzahl", default=self.alte_nachricht))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        db = getMongoDataBase()
        if str(self.alte_nachricht) == "%member-Member#0000 | %name-Member | %mention-@Member | %guild-Servername | %usercount-Memberanzahl":
            await db['leavemsg'].insert_one({"guildID": str(interaction.guild.id), "channelID": self.kanal.id, "msg": self.children[0].value})
            return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Verlassensnachricht ist nun aktiv.**")
        db["leavemsg"].update_one({"guildID": str(interaction.guild.id)}, {"$set": {"channelID": self.kanal.id, "msg": self.children[0].value}})
        return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Verlassensnachricht ist nun geändert.**")

##########

def random_color():
    return discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

async def sendWelcomeMessage(self, member):
    db = getMongoDataBase()
    
    result = await db['welcome'].find_one({"guildID": str(member.guild.id)})
    
    if result == None:
        return
    
    try:
        ch = await member.guild.fetch_channel(int(result["channelID"]))
    
        if "B9xV123" not in str(result["msg"]):
            finalmsg = result["msg"].replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
            try:
                embed = discord.Embed(color=await getcolour(self, member), description=finalmsg)
                
                await ch.send(finalmsg)
            except discord.errors.HTTPException and discord.errors.Forbidden:
                pass
        else:
            finalmsg = result["msg"].replace("B9xV123", "").replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
        
        embed = discord.Embed(color=await getcolour(self, member), description=finalmsg)
        
        background = Editor("willkommen.png")
        profile = await load_image_async(str(member.avatar))
        profile = Editor(profile).resize((415, 415)).circle_image()
        background.paste(profile.image, (112, 252))
        background.text((1100, 475), str(member), color="#ffffff")
        current_datetime = datetime.datetime.now()
        account_created_at = member.created_at.replace(tzinfo=None)
        time_difference = current_datetime - account_created_at
        days_difference = time_difference.days
        output_message = f"Account vor {days_difference} Tagen erstellt."
        background.text((1100, 570), output_message, color="#ffffff")
        background.text((1550, 800), str(member.guild.member_count), color="#ffffff")
        background.text((2150, 850), str(member.guild.name), color="#ffffff")
        file = discord.File(fp=background.image_bytes, filename="willkommen.png")
        embed.set_image(url="attachment://willkommen.png")
        await ch.send(embed=embed, file=file)
    except discord.errors.HTTPException and discord.errors.Forbidden:
        pass
    
async def sendLeaveMessage(self, member):
    result = await getMongoDataBase()['leavemsg'].find_one({"guildID": str(member.guild.id)})
        
    if result == None:
        return
    
    try:
        ch = await member.guild.fetch_channel(int(result["channelID"]))
    except discord.errors.NotFound:
        return
    
    finalmsg = result[1].replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
    
    try:
        embed = discord.Embed(color=await getcolour(self, member), description=finalmsg)
        
        await ch.send(embed=embed)
    except discord.errors.HTTPException and discord.errors.Forbidden:
        pass
    

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await sendWelcomeMessage(self, member)
                

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def testjoin(self, interaction: discord.Interaction):
        """Sendet die Willkommensnachricht an den Kanal, um zu sehen ob sie funktioniert."""
        member = interaction.user
        
        await interaction.response.defer()
                
        await sendWelcomeMessage(self, member)
        
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Die Test-Willkommensnachricht wurde gesendet.**")
                

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def joinmsg(self, interaction: discord.Interaction, argument: typing.Literal["Einrichten (Kanal muss mit angegeben werden)","Anzeigen","Ausschalten"], kanal: discord.TextChannel=None):
        """Stelle die Willkommensnachricht ein."""
        
        db = getMongoDataBase()
        
        if argument == "Ausschalten":
            result = await db['welcome'].find_one({"guildID": str(interaction.guild.id)})
            if result == None:
                return await interaction.response.send_message("**<:v_x:1264270921452224562> Auf diesem Server ist keine Willkommensnachricht eingerichtet.**", ephemeral=True)
            db['welcome'].delete_one({"guildID": str(interaction.guild.id)})
            return await interaction.response.send_message("**<:v_checkmark:1264271011818242159> Die Willkommensnachricht wurde ausgeschaltet.**")
        if argument == "Einrichten (Kanal muss mit angegeben werden)":
            if kanal == None:
                return await interaction.response.send_message("**<:v_x:1264270921452224562> Beim Einrichten ist auch eine Kanal-Angabe erforderlich.**", ephemeral=True)

            result = await db['welcome'].find_one({"guildID": str(interaction.guild.id)})

            alte_nachricht = ""
            if result:
                alte_nachricht += result["msg"]
            else:
                alte_nachricht += "%member-Member#0000 | %name-Member | %mention-@Member | %guild-Servername | %usercount-Memberanzahl"
            await interaction.response.send_modal(Willkommensnachricht(kanal, self.bot, alte_nachricht))
        if argument == "Anzeigen":                    
            wel = await db['welcome'].find_one({"guildID": str(interaction.guild.id)})
            
            try:
                ch = await interaction.guild.fetch_channel(int(wel["channelID"]))
            except:
                return await interaction.response.send_message("**<:v_x:1264270921452224562> Der Kanal der Willkommensnachricht existiert nicht mehr. Bitte deaktiviere die Willkommensnachricht und richte sie erneut ein.**", ephemeral=True)

            embed = discord.Embed(title="Willkommensnachricht", description=f"Die aktuelle Willkommensnachricht:", color=await getcolour(self, interaction.user))
            
            embed.add_field(name="Kanal", value=ch.mention, inline=False)
            embed.add_field(name="Nachricht", value=wel['msg'], inline=False)
            await interaction.response.send_message(embed=embed)

#leave message
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await sendLeaveMessage(self, member)
        
            
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def testleave(self, interaction: discord.Interaction):
        """Sendet die Verlassensnachricht an den Kanal, um zu sehen ob sie funktioniert."""
        
        await interaction.response.defer()
        
        member = interaction.user
        
        result = await getMongoDataBase()['leavemsg'].find_one({"guildID": str(interaction.guild.id)})
        
        if result == None:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Auf diesem Server ist keine Verlassensnachricht eingerichtet. Deaktiviere diese zuerst!**", ephemeral=True)
        
        await sendLeaveMessage(self, member)
        
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Die Test-Verlassensnachricht wurde gesendet.**")

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def leavemsg(self, interaction: discord.Interaction, argument: typing.Literal["Einrichten (Kanal muss mit angegeben werden)","Anzeigen","Ausschalten"], kanal: discord.TextChannel=None):
        """Stelle die Verlassensnachricht ein."""
        
        db = getMongoDataBase()
        
        if argument == "Ausschalten":
            result = await db['leavemsg'].find_one({"guildID": str(interaction.guild.id)})
            
            if result == None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Auf diesem Server ist keine Verlassensnachricht eingerichtet.**", ephemeral=True)
            await db['leavemsg'].delete_one({"guildID": str(interaction.guild.id)})
            return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Verlassensnachricht wurde ausgeschaltet.**")
        if argument == "Einrichten (Kanal muss mit angegeben werden)":
            if kanal == None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Beim Einrichten ist auch eine Kanal-Angabe erforderlich.**", ephemeral=True)
            result = await db['leavemsg'].find_one({"guildID": str(interaction.guild.id)})
            alte_nachricht = ""
            if result:
                alte_nachricht += result[1]
            else:
                alte_nachricht += "%member-Member#0000 | %name-Member | %mention-@Member | %guild-Servername | %usercount-Memberanzahl"
            await interaction.response.send_modal(Verlassensnachricht(kanal, self.bot, alte_nachricht))
        if argument == "Anzeigen":
            await interaction.response.defer()
            
            wel = await db['leavemsg'].find_one({"guildID": str(interaction.guild.id)})
            try:
                ch = await interaction.guild.fetch_channel(int(wel["channelID"]))
            except:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Der Kanal der Verlassensnachricht existiert nicht mehr. Bitte deaktiviere die Verlassensnachricht und richte sie erneut ein.**", ephemeral=True)
            embed = discord.Embed(title="Verlassensnachricht", description=f"Die aktuelle Verlassensnachricht:", color=await getcolour(self, interaction.user))
            embed.add_field(name="Kanal", value=ch.mention, inline=False)
            embed.add_field(name="Nachricht", value=wel["msg"], inline=False)
            
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(message(bot))