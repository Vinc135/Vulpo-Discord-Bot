import discord
from discord.ext import commands
from discord import app_commands
from googleapiclient.discovery import build
from google.oauth2.credentials import OAuth2Credentials

async def check_all_channels(self):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT name, latest_video, channelID, guildID FROM youtube")
            channels = await cursor.fetchall()

        for channel in channels:
            channel_name = channel[0]
            latest_video = channel[1]
            new_video = check_new_videos(channel_name, latest_video)

            if new_video and new_video != latest_video:
                async with conn.cursor() as cursor:
                    await cursor.execute("UPDATE youtube SET latest_video = (%s) WHERE name = (%s) AND guildID = (%s)", (new_video, channel_name, channel[3]))
                chan = self.bot.get_channel(int(channel[2]))
                await chan.send(f"__Neues Video von {channel_name}__\nhttps://youtube.com/watch?v={new_video}")

def check_new_videos(channel_name, latest_video):
    CLIENT_ID = '55839731236-3pcbgeorr8h4vca6c45d5181kitd5ngj.apps.googleusercontent.com'
    CLIENT_SECRET = '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'
    REFRESH_TOKEN = 'YOUR_REFRESH_TOKEN'
    creds = OAuth2Credentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        refresh_token=REFRESH_TOKEN
    )
    service = build('youtube', 'v3', credentials=creds)

    API_KEY = "AIzaSyBAnd9nr8cF0mV-5yScIcSdQv5TpCOlJ24"
    request = service.search().list(
        part='id',
        channelId=channel_name,
        type='video',
        eventType='live',
        order='date',
        maxResults=1,
        key=API_KEY
    )
    response = request.execute()

    # Get the video ID of the latest video
    latest_video = response['items'][0]['id']['videoId']

    # Return the video ID
    return latest_video

class youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def check(self, ctx):
        await check_all_channels(self)

    youtube = app_commands.Group(name='youtube', description='Erstelle und lösche YT-Ankündigungen.', guild_only=True)

    @youtube.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add(self, interaction: discord.Interaction, ytkanalname: str, kanal: discord.TextChannel):
        """Füge eine YT-Ankündigung hinzu."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT name, channelID FROM youtube WHERE guildID = (%s) AND name = (%s)", (interaction.guild.id, ytkanalname))
                result = await cursor.fetchone()
                if result != None:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Dieser YT Kanal existiert bereits auf der Ankündigungsliste.**", ephemeral=True)
                    return
                await cursor.execute("INSERT INTO youtube(guildID, name, channelID) VALUES(%s,%s,%s)", (interaction.guild.id, ytkanalname, kanal.id))
                
                await interaction.response.send_message(f"**<:v_haken:1048677657040134195> YT Kanalankündigung erstellt in {kanal.mention}.**")

    @youtube.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def delete(self, interaction: discord.Interaction, ytkanalname: str):
        """Entferne eine YT-Ankündigung."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT name, channelID FROM youtube WHERE guildID = (%s) AND name = (%s)", (interaction.guild.id, ytkanalname))
                result = await cursor.fetchone()
                if result != None:
                    await cursor.execute("DELETE FROM youtube WHERE guildID = (%s) AND name = (%s)", (interaction.guild.id, ytkanalname))
                    await interaction.response.send_message(f"**<:v_haken:1048677657040134195> YT Kanalankündigung gelöscht für {ytkanalname}.**")
                    return
                await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Dieser YT Kanal existiert nicht auf der Ankündigungsliste.**", ephemeral=True)

    @youtube.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def liste(self, interaction: discord.Interaction):
        """Erhalte eine Liste von den YT-Ankündigungen."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT name, channelID FROM youtube WHERE guildID = (%s)", (interaction.guild.id))
                result = await cursor.fetchall()
                if result == None:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Hier wurden keine YT Ankündigungen gefunden. Füge einen Tag mit `/youtube add` hinzu**", ephemeral=True)
                    return
                embed = discord.Embed(title="Alle YT Ankündigungen des Servers", description="Hier nähere Infos:", color=await getcolour(self, interaction.user))
                for i in result:
                    embed.add_field(name=i[0], value=f"Kanal: <#{i[1]}>")
                await interaction.response.send_message(embed=embed)
                
async def setup(bot):
    await bot.add_cog(youtube(bot))