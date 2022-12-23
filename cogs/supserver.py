import asyncio
from discord.ext import commands, tasks
import discord
import random
from discord import app_commands
import datetime
import typing
 
def random_color():
    return discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

class Supserver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_message.start()

    def cog_unload(self):
        self.update_message.cancel()

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot:
            return
        
        if int(msg.channel.id) == 960133645140623390:
            await asyncio.sleep(1800)
            await msg.delete()
                    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 925729625580113951:
            channel = member.guild.get_channel(926224205639467108)
            message = await channel.send(f"<:v_info:1037065915113676891> Hallo {member.mention}, wähle hier deine Rollen aus!")
            await asyncio.sleep(60)
            await message.delete()

    @app_commands.command()
    @app_commands.guild_only()
    async def update(self, interaction: discord.Interaction, inhalt: str, status: typing.Literal["Neu","Bearbeitet","Entfernt"]):
        """Verkünde ein Update von Vulpo + Wochenrückblick."""
        if interaction.user.id != 824378909985341451:
            return await interaction.response.send_message("<:v_kreuz:1049388811353858069> Diesen Befehl kann nur Vinc#6791 ausführen.", ephemeral=True)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT msgID FROM updates")
                result = await cursor.fetchone()
                channel: discord.TextChannel = self.bot.get_channel(964994865484169316)
                msg = await channel.fetch_message(int(result[0]))
                embed = msg.embeds[0]
                #embed.description += "\n "

                if status == "Neu":
                    embed.description += f"\n🟢 - {inhalt}"
                if status == "Bearbeitet":
                    embed.description += f"\n🟠 - {inhalt}"
                if status == "Entfernt":
                    embed.description += f"\n🔴 - {inhalt}"
                await msg.edit(content="", embed=embed)
                await interaction.response.send_message("**<:v_haken:1048677657040134195> Erfolreich hinzugefügt!**")
                
    @tasks.loop(minutes=1)
    async def update_message(self):
        if datetime.datetime.today().weekday() == 6:
            if int(datetime.datetime.now().hour) + 1 == 22 and int(datetime.datetime.now().minute) == 0:
                async with self.bot.pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute("SELECT msgID FROM updates")
                        result = await cursor.fetchone()
                        channel: discord.TextChannel = self.bot.get_channel(964994865484169316)
                        msg = await channel.fetch_message(int(result[0]))
                        
                        await msg.reply("__<@&926212661182623774>__\nDie Änderungen aus **dieser Woche** seht ihr hier.")
                        await  cursor.execute("DELETE FROM updates")

        if datetime.datetime.today().weekday() == 0:
            if int(datetime.datetime.now().hour) + 1 == 10 and int(datetime.datetime.now().minute) == 0:
                async with self.bot.pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        channel: discord.TextChannel = self.bot.get_channel(964994865484169316)
                        current_date = datetime.datetime.today()
                        next_sunday = current_date + datetime.timedelta(days=(6 - current_date.weekday()))

                        embed = discord.Embed(colour=discord.Colour.orange(), title=f"<:v_spa:1037065926929027122> WOCHENRÜCKBLICK [{current_date.day}.{current_date.month}. - {next_sunday.day}.{next_sunday.month}.]", description="🟢 = Hinzugefügt **|** 🟠 = Geändert **|** 🔴 = Entfernt\n\n> <:v_pfeil_rechts:1048677625876459562> Diese Nachricht wird bei jedem Update bearbeitet. Am Ende der Woche wird gepingt.")
                        vulpo = self.bot.get_user(925799559576322078)
                        embed.set_footer(text="Viel Spaß mit dem Update!", icon_url=vulpo.avatar)
                        msg = await channel.send(embed=embed)
                        await cursor.execute("INSERT INTO updates(msgID) VALUES(%s)", (msg.id))
        

async def setup(bot):
    await bot.add_cog(Supserver(bot))