import typing
import discord
from discord.ext import commands, tasks
from discord import app_commands
from utils.utils import getcolour
from utils.MongoDB import getMongoDataBase
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
        
        await interaction.response.defer()
        
        getMongoDataBase()["channels"].insert_one({"guildID": interaction.guild.id, "channelID": self.kanal.id, "name": self.name, "username": self.username, "format": self.children[0].value})
        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Youtube Benachrichtigung", description=f"Vulpo wird nun jedes neue Video vom Youtube Kanal mit dem Usernamen `@{self.username}` im Kanal {self.kanal.mention} posten (innerhalb von 60 Sekunden nach der Veröffentlichung eines Videos).")
        
        await interaction.followup.send(embed=embed)
    
async def fetch_videos_from_database(self, channel_name):
    
    document = getMongoDataBase()["videos"].find({"channel_name": channel_name}).to_list(length=None)
    return [doc["video_id"] for doc in document]

async def insert_video_to_database(self, channel_name, video_id):
    getMongoDataBase()["videos"].insert_one({"channel_name": channel_name, "video_id": video_id})

async def check_videos(self):
    try:
        db = getMongoDataBase()
        youtube_channels = await db["channels"].find().to_list()
        for youtube_channel in youtube_channels:
            try:
                videos = scrapetube.get_channel(channel_url=f"https://www.youtube.com/@{youtube_channel['username']}", limit=5)
            except:
                videos = []
            video_ids = [video["videoId"] for video in videos]

        saved_videos = await fetch_videos_from_database(self, youtube_channel["username"])

        for video_id in video_ids:
            if video_id not in saved_videos:
                url = f"https://youtu.be/{video_id}"
                await insert_video_to_database(self, youtube_channel["username"], video_id)

                result = await db["channels"].find({"username": youtube_channel["username"]}).to_list()
                for r in result:
                    guild = await self.bot.fetch_guild(int(r[0]))
                    if guild:
                        channel = await guild.fetch_channel(int(r[1]))
                        if channel:
                            format = r[2]
                            endmsg = format.replace("%ycn", f"{youtube_channel[0]}").replace("%ycun", f"@{youtube_channel['username']}").replace("%link", f"{url}")
                            await channel.send(endmsg)
    except Exception as e:
        try:
            guild = await self.bot.fetch_guild(925729625580113951)
            channel = await guild.fetch_channel(1127157434784432240)
            await channel.send(e)
        except:
            pass

async def check_tickets(self):
    pass
#    async with self.bot.pool.acquire() as conn:
#        async with conn.cursor() as cursor:
#            guild = self.bot.get_guild(925729625580113951)
#            channel = guild.get_channel(1133348936116076636)
#            message = await channel.fetch_message(1133349035508519002)
#            if message.embeds:
#                emb = message.embeds[0]
#            else:
#                emb = None

#            await cursor.execute("SELECT autorname, autorID, ticketID, titel, status, letztes_update FROM w_tickets WHERE status != (%s)", ("Geschlossen"))
#            results = await cursor.fetchall()
#            embed = discord.Embed(title="Aktuelle Tickets", description="Hier siehst du alle Tickets und deren Status. Du kannst dich daran orientieren, wo Support gefragt ist.", color=discord.Color.orange())
#            for result in results:
#                autorname, autorID, ticketID, titel, status, letztes_update = result
#                embed.add_field(name=f"#{ticketID} - {titel}", value=f"<:v_user:1119585450923929672> {autorname}\n<:v_mod:1119581819122241621> {status}\n<:v_zeit:1119585888054296676> Letztes Update: {letztes_update}")
#            embed.set_footer(text="https://vulpo-bot.de/ticketsystem")
#            if emb == None or embed != emb:
#                await message.edit(content="", embed=embed)
            
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
        await check_tickets(self)

    benachrichtigung = app_commands.Group(name='benachrichtigung', description='Lass Benachrichtigungen für neue Videos senden.', guild_only=True)

    @benachrichtigung.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def youtube(self, interaction: discord.Interaction, modus: typing.Literal["Hinzufügen", "Entfernen"], kanal: discord.TextChannel, channelusername: str, channelname: str):
        """Füge hinzu / entferne Youtube Benachrichtigungen."""
        
        db = getMongoDataBase()
        
        if modus == "Hinzufügen":
                    result = await db["channels"].find_one({"guildID": interaction.guild.id, "channelID": kanal.id, "username": channelusername}) 
                    if result is None:
                        try:
                            videos = scrapetube.get_channel(channel_url=f"https://www.youtube.com/@{channelusername}", limit=5)
                            video_ids = [video["videoId"] for video in videos]

                            saved_videos = await fetch_videos_from_database(self, channelusername)
                            if saved_videos == []:
                                for video_id in video_ids:
                                    await insert_video_to_database(self, channelusername, video_id)                            
                            
                            return await interaction.response.send_modal(nachricht(kanal, channelname, channelusername, self.bot))
                        
                        except:
                            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Youtube Benachrichtigung", description=f"Der Youtube Kanal mit dem Usernamen `@{channelusername}` wurde nicht gefunden. Bitte überprüfe den Usernamen und versuche es erneut.")
                            
                            return await interaction.followup.send(embed=embed, ephemeral=True)
                        
                    else:
                        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Youtube Benachrichtigung", description=f"In diesem Kanal erhältst du bereits Benachrichtigungen vom Youtube Kanal mit dem Usernamen `@{channelusername}`.")
                        
                        return await interaction.followup.send(embed=embed, ephemeral=True)
                        
        if modus == "Entfernen":
                    result = await db["channels"].find_one({"guildID": interaction.guild.id, "channelID": kanal.id, "username": channelusername})
                    if result is None:
                        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Youtube Benachrichtigung", description=f"In diesem Kanal erhältst du keine Benachrichtigungen vom Youtube Kanal mit dem Usernamen `@{channelusername}`.")
                        
                        return await interaction.followup.send(embed=embed, ephemeral=True)

                    if result:
                        await db["channels"].delete_one({"guildID": interaction.guild.id, "channelID": kanal.id, "username": channelusername})
                        await db["videos"].delete_many({"channel_name": channelusername})
                        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Youtube Benachrichtigung", description=f"Vulpo wird nun nicht mehr jedes neue Video vom Youtube Kanal mit dem Usernamen `@{channelusername}` im Kanal {kanal.mention} posten.")
                        
                        return await interaction.followup.send(embed=embed)
                    
async def setup(bot):
    await bot.add_cog(notifications(bot))