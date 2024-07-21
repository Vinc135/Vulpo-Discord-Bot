import discord
from discord.ext import commands
from utils.utils import reminder_end, convert, discord_timestamp
from discord import app_commands
import typing
import asyncio
import math
import datetime
from utils.utils import getcolour
from utils.MongoDB import getMongoDataBase

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    erinnerung = app_commands.Group(name='erinnerung', description='Nehme Einstellungen an deinen Erinnerungen vor.', guild_only=True)

    @erinnerung.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def erstellen(self, interaction: discord.Interaction, beschreibung: str, minuten: typing.Literal["1m","15m","30m","45m"]=None, stunden: typing.Literal["1h","2h","3h","4h","5h","6h","7h","8h","9h","10h","11h","12h","13h","14h","15h","16h","17h","18h","19h","20h","21h","22h","23h"]=None, tage: typing.Literal["1d","2d","3d","4d","5d","6d","7d","14d"]=None):
        """Erstelle dir eine Erinnerung für eine bestimmte Uhrzeit."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        zeit_als_string = ""
        if tage:
            zeit_als_string += f" {tage}"
        if stunden:
            zeit_als_string += f" {stunden}"
        if minuten:
            zeit_als_string += f" {minuten}"
        if zeit_als_string == "":
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du musst auch eine Zeit angeben, wann du erinnert werden möchtest ;D**", ephemeral=True)
                
        zeit = convert(zeit_als_string)
        t1 = math.floor(datetime.datetime.now().timestamp() + zeit)
        t2 = datetime.datetime.fromtimestamp(int(t1))
        id = await db['erinnerungen'].count_documents({}) + 1
        
        await db['erinnerungen'].insert_one({"userID": interaction.user.id, "endtime": t1, "zeit": zeit, "beschreibung": beschreibung, "id": id})
        
        embed = discord.Embed(color=await getcolour(self, interaction.user), title=f"Erinnerung gestellt (ID {id})", description=f"""
<:v_12:1264264683427336259> Erinnerung gesetzt auf {discord_timestamp(t2, 'f')}
<:v_24:1264264867511144479> {beschreibung}""")
                
        asyncio.create_task(reminder_end(t2, self.bot, interaction.user.id, id), name=f"Erinnerung - {id}")
        await interaction.followup.send(embed=embed)
        
    @erinnerung.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def löschen(self, interaction: discord.Interaction, id: int):
        """Entfernt eine Erinnerung."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = await db['erinnerungen'].find_one({"userID": interaction.user.id, "id": id})
        
        if result is None:
            await interaction.followup.send(f"**<:v_9:1264264656831119462> Die Erinnerung mit der ID {id} von dir wurde nicht gefunden.**", ephemeral=True)
            return
        await db['erinnerungen'].delete_one({"userID": interaction.user.id, "id": id})
        for task in asyncio.all_tasks():
            name = str(task.get_name())
            if name == f"Erinnerung - {id}":
                task.cancel()
                return await interaction.followup.send(f"**<:v_158:1264268251916009553> Die Erinnerung mit der ID {id} von dir wurde entfernt.**")
            
        await interaction.followup.send(f"**<:v_9:1264264656831119462> Die Erinnerung mit der ID {id} von dir wurde nicht gefunden.**", ephemeral=True)
        
    @erinnerung.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def anzeigen(self, interaction: discord.Interaction):
        """Bekomme eine Liste von deinen Erinnerungen.""" 
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = await db['erinnerungen'].find({"userID": interaction.user.id}).to_list(length=None)
        
        if result == []:
            return await interaction.followup.send(f"**<:v_9:1264264656831119462> Du hast keine Erninnerungen gestellt.**", ephemeral=True) 
        embed = discord.Embed(colour=await getcolour(self, interaction.user), title=f"Alle Erinnerungen von {interaction.user}.")
        embed.set_thumbnail(url=interaction.user.avatar)
        
        for er in result:
            t2 = datetime.datetime.fromtimestamp(int(er["endtime"]))
            embed.add_field(name=f"ID {er['id']}", value=f"<:v_24:1264264867511144479> {er['beschreibung']}\n<:v_12:1264264683427336259> Ende: {discord_timestamp(t2, 'f')}", inline=False)
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Reminder(bot))