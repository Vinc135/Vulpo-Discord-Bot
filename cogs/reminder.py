import discord
from discord.ext import commands
from info import reminder_end, convert, discord_timestamp
from discord import app_commands
import typing
import asyncio
import math
import datetime

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    erinnerung = app_commands.Group(name='erinnerung', description='Nehme Einstellungen an deinen Erinnerungen vor.')

    @erinnerung.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def erstellen(self, interaction: discord.Interaction, beschreibung: str, minuten: typing.Literal["1m","15m","30m","45m"]=None, stunden: typing.Literal["1h","2h","3h","4h","5h","6h","7h","8h","9h","10h","11h","12h","13h","14h","15h","16h","17h","18h","19h","20h","21h","22h","23h"]=None, tage: typing.Literal["1d","2d","3d","4d","5d","6d","7d","14d"]=None):
        """Erstelle dir eine Erinnerung für eine bestimmte Uhrzeit."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                #endzeit umwandeln in timestamp
                zeit_als_string = ""
                if tage:
                    zeit_als_string += f" {tage}"
                if stunden:
                    zeit_als_string += f" {stunden}"
                if minuten:
                    zeit_als_string += f" {minuten}"
                if zeit_als_string == "":
                    return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du musst auch eine Zeit angeben, wann du erinnert werden möchtest ;D**", ephemeral=True)
                zeit = convert(zeit_als_string)
                t1 = math.floor(datetime.datetime.utcnow().timestamp() + zeit)
                t2 = datetime.datetime.fromtimestamp(int(t1))
                await cursor.execute("SELECT id FROM erinnerungen ORDER BY id DESC")
                result = await cursor.fetchone()
                if result == None:
                    id = 0
                if result != None:
                    id = result[0] + 1
                
                await cursor.execute("INSERT INTO erinnerungen(userID, endtime, beschreibung, id) VALUES(%s, %s, %s, %s)", (interaction.user.id, t1, beschreibung, id))
                
                embed = discord.Embed(color=discord.Colour.green(), title=f"Erinnerung gestellt (ID {id})", description=f"""
<:v_info:1037065915113676891> Erinnerung gesetzt auf {discord_timestamp(t2, 'f')}
<:v_play:1037065922134945853> {beschreibung}""")
                asyncio.create_task(reminder_end(t2, self.bot, interaction.user.id, id), name=f"Erinnerung - {id}")
                await interaction.response.send_message(embed=embed)
        
    @erinnerung.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def löschen(self, interaction: discord.Interaction, id: int):
        """Entfernt eine Erinnerung."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT beschreibung FROM erinnerungen WHERE userID = (%s) AND id = (%s)", (interaction.user.id, id))
                result = await cursor.fetchone()
                if result is None:
                    await interaction.response.send_message(f"**<:v_kreuz:1049388811353858069> Die Erinnerung mit der ID {id} von dir wurde nicht gefunden.**", ephemeral=True)
                    return
                await cursor.execute("DELETE FROM erinnerungen WHERE userID = (%s) AND id = (%s)", (interaction.user.id, id))
                for task in asyncio.all_tasks():
                    name = str(task.get_name())
                    if name == f"Erinnerung - {id}":
                        task.cancel()
                        return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Die Erinnerung mit der ID {id} von dir wurde entfernt.**")
                    
                await interaction.response.send_message(f"**<:v_kreuz:1049388811353858069> Die Erinnerung mit der ID {id} von dir wurde nicht gefunden.**", ephemeral=True)
        
    @erinnerung.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def anzeigen(self, interaction: discord.Interaction):
        """Bekomme eine Liste von deinen Erinnerungen."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT beschreibung, id, endtime FROM erinnerungen WHERE userID = (%s)", (interaction.user.id))
                result = await cursor.fetchall()
                if result == ():
                    return await interaction.response.send_message(f"**<:v_kreuz:1049388811353858069> Du hast keine Erninnerungen gestellt.**", ephemeral=True) 
                embed = discord.Embed(colour=discord.Colour.blurple(), title=f"Alle Erinnerungen von {interaction.user}.")
                embed.set_thumbnail(url=interaction.user.avatar)
                for er in result:
                    t2 = datetime.datetime.fromtimestamp(int(er[2]))
                    embed.add_field(name=f"ID {er[1]}", value=f"<:v_play:1037065922134945853> {er[0]}\n<:v_info:1037065915113676891> Ende: {discord_timestamp(t2, 'f')}", inline=False)
                await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Reminder(bot))