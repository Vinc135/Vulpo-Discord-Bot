import typing
import discord
from discord.ext import commands, tasks
from discord import app_commands
from info import getcolour
import scrapetube

class nachricht(discord.ui.Modal, title="Eigene Nachricht"):
    def __init__(self, kanal: discord.TextChannel=None, name=None, username=None, bot=None):
        super().__init__(custom_id="fwrgfe45gfe5gfew5")
        self.kanal = kanal
        self.bot = bot
        self.name = name
        self.username = username
        self.add_item(discord.ui.TextInput(label="Nachricht", style=discord.TextStyle.paragraph, required=True, placeholder="%ycn - Youtubekanal Name | %ycun - Youtubekanal Username(@...) | %link - Link zum Video"))

    async def on_submit(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("INSERT INTO channels(guildID, channelID, name, username, format) VALUES(%s, %s, %s, %s, %s)", (interaction.guild.id, self.kanal.id, self.name, self.username, self.children[0].value))
                embed = discord.Embed(color=await getcolour(self, interaction.user), title="Youtube Benachrichtigung", description=f"Vulpo wird nun jedes neue Video vom Youtube Kanal mit dem Usernamen `@{self.username}` im Kanal {self.kanal.mention} posten (innerhalb von 60 Sekunden nach der Veröffentlichung eines Videos).")
                embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                await interaction.response.send_message(embed=embed)
    
async def fetch_videos_from_database(self, channel_name):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT video_id FROM videos WHERE channel_name = %s", (channel_name,))
                rows = await cur.fetchall()
                return [row[0] for row in rows]

async def insert_video_to_database(self, channel_name, video_id):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO videos(channel_name, video_id) VALUES (%s, %s)", (channel_name, video_id))

async def check_videos(self):
    try:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT name, username FROM channels")
                youtube_channels = await cur.fetchall()
                for youtube_channel in youtube_channels:
                    try:
                        videos = scrapetube.get_channel(channel_url=f"https://www.youtube.com/@{youtube_channel[1]}", limit=5)
                    except:
                        videos = []
                    video_ids = [video["videoId"] for video in videos]

                    saved_videos = await fetch_videos_from_database(self, youtube_channel[1])

                    for video_id in video_ids:
                        if video_id not in saved_videos:
                            url = f"https://youtu.be/{video_id}"
                            await insert_video_to_database(self, youtube_channel[1], video_id)

                            await cur.execute("SELECT guildID, channelID, format FROM channels WHERE username = (%s)", (youtube_channel[1]))
                            result = await cur.fetchall()
                            for r in result:
                                guild = self.bot.get_guild(int(r[0]))
                                if guild:
                                    channel = guild.get_channel(int(r[1]))
                                    if channel:
                                        format = r[2]
                                        endmsg = format.replace("%ycn", f"{youtube_channel[0]}").replace("%ycun", f"@{youtube_channel[1]}").replace("%link", f"{url}")
                                        await channel.send(endmsg)
    except Exception as e:
        guild = self.bot.get_guild(925729625580113951)
        channel = guild.get_channel(1127157434784432240)
        await channel.send(e)

async def check_tickets(self):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            guild = self.bot.get_guild(925729625580113951)
            channel = guild.get_channel(1133348936116076636)
            message = await channel.fetch_message(1133349035508519002)
            if message.embeds:
                emb = message.embeds[0]
            else:
                emb = None

            await cursor.execute("SELECT autorname, autorID, ticketID, titel, status, letztes_update FROM w_tickets WHERE status != (%s)", ("Geschlossen"))
            results = await cursor.fetchall()
            embed = discord.Embed(title="Aktuelle Tickets", description="Hier siehst du alle Tickets und deren Status. Du kannst dich daran orientieren, wo Support gefragt ist.", color=discord.Color.orange())
            for result in results:
                autorname, autorID, ticketID, titel, status, letztes_update = result
                embed.add_field(name=f"#{ticketID} - {titel}", value=f"<:v_user:1119585450923929672> {autorname}\n<:v_mod:1119581819122241621> {status}\n<:v_zeit:1119585888054296676> Letztes Update: {letztes_update}")
            embed.set_footer(text="https://vulpo-bot.de/ticketsystem")
            if emb == None or embed != emb:
                await message.edit(content="", embed=embed)
            
class notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_load(self):
        self.check.start()
        self.check_tickets.start()
        
    def cog_unload(self):
        self.check.cancel()
        self.check_tickets.cancel()

    
    @tasks.loop(seconds=60)
    async def check(self):
        await check_videos(self)

    @tasks.loop(seconds=60)
    async def check_tickets(self):
        try:
            await check_tickets(self)
        except:
            pass

    benachrichtigung = app_commands.Group(name='benachrichtigung', description='Lass Benachrichtigungen für neue Videos senden.', guild_only=True)

    @benachrichtigung.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def youtube(self, interaction: discord.Interaction, modus: typing.Literal["Hinzufügen", "Entfernen"], kanal: discord.TextChannel, channelusername: str, channelname: str):
        """Füge hinzu / entferne Youtube Benachrichtigungen."""
        if modus == "Hinzufügen":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelID FROM channels WHERE guildID = (%s) AND channelID = (%s) AND username = (%s)", (interaction.guild.id, kanal.id, channelusername))
                    result = await cursor.fetchone()
                    if result is None:
                        try:
                            videos = scrapetube.get_channel(channel_url=f"https://www.youtube.com/@{channelusername}", limit=5)
                            video_ids = [video["videoId"] for video in videos]

                            saved_videos = await fetch_videos_from_database(self, channelusername)
                            if saved_videos == []:
                                for video_id in video_ids:
                                    await insert_video_to_database(self, channelusername, video_id)                            
                            
                            return await interaction.response.send_modal(nachricht(kanal, channelname, channelusername, self.bot))
                        
                        except Exception as e:
                            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Youtube Benachrichtigung", description=f"Der Youtube Kanal mit dem Usernamen `@{channelusername}` wurde nicht gefunden.\nFehler: {e}")
                            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                            return await interaction.response.send_message(embed=embed, ephemeral=True)
                        
                    else:
                        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Youtube Benachrichtigung", description=f"In diesem Kanal erhältst du bereits Benachrichtigungen vom Youtube Kanal mit dem Usernamen `@{channelusername}`.")
                        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                        return await interaction.response.send_message(embed=embed, ephemeral=True)
                        
        if modus == "Entfernen":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelID FROM channels WHERE guildID = (%s) AND channelID = (%s) AND username = (%s)", (interaction.guild.id, kanal.id, channelusername))
                    result = await cursor.fetchone()
                    if result is None:
                        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Youtube Benachrichtigung", description=f"In diesem Kanal erhältst du keine Benachrichtigungen vom Youtube Kanal mit dem Usernamen `@{channelusername}`.")
                        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                        return await interaction.response.send_message(embed=embed, ephemeral=True)

                    if result:
                        await cursor.execute("DELETE FROM channels WHERE guildID = (%s) AND channelID = (%s) AND username = (%s)", (interaction.guild.id, kanal.id, channelusername))
                        await cursor.execute("DELETE FROM videos WHERE channel_name = (%s)", (channelusername))
                        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Youtube Benachrichtigung", description=f"Vulpo wird nun nicht mehr jedes neue Video vom Youtube Kanal mit dem Usernamen `@{channelusername}` im Kanal {kanal.mention} posten.")
                        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                        return await interaction.response.send_message(embed=embed)
                    
async def setup(bot):
    await bot.add_cog(notifications(bot))