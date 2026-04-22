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

        self.add_item(discord.ui.TextInput(
            label="Nachricht",
            style=discord.TextStyle.paragraph,
            required=True,
            placeholder="%ycn - Name | %ycun - @Username | %link - Video Link"
        ))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()

        await getMongoDataBase()["channels"].insert_one({
            "guildID": str(interaction.guild.id),
            "channelID": str(self.kanal.id),
            "name": self.name,
            "username": self.username,
            "format": self.children[0].value
        })

        embed = discord.Embed(
            color=await getcolour(self, interaction.user),
            title="Youtube Benachrichtigung",
            description=f"Neue Videos von @{self.username} werden in {self.kanal.mention} gepostet."
        )

        await interaction.followup.send(embed=embed)


async def fetch_videos_from_database(self, channel_name):
    docs = await getMongoDataBase()["videos"].find({
        "channel_name": channel_name
    }).to_list(length=None)

    return [doc["video_id"] for doc in docs]


async def insert_video_to_database(self, channel_name, video_id):
    await getMongoDataBase()["videos"].insert_one({
        "channel_name": channel_name,
        "video_id": video_id
    })


async def check_videos(self):
    try:
        db = getMongoDataBase()
        youtube_channels = await db["channels"].find().to_list(length=None)

        for youtube_channel in youtube_channels:
            try:
                videos = list(scrapetube.get_channel(
                    channel_url=f"https://www.youtube.com/@{youtube_channel['username']}",
                    limit=5
                ))
            except Exception as e:
                print("scrapetube error:", e)
                continue

            video_ids = [video["videoId"] for video in videos]
            saved_videos = await fetch_videos_from_database(self, youtube_channel["username"])

            for video_id in video_ids:
                if video_id not in saved_videos:
                    url = f"https://youtu.be/{video_id}"
                    await insert_video_to_database(self, youtube_channel["username"], video_id)

                    result = await db["channels"].find({
                        "username": youtube_channel["username"]
                    }).to_list(length=None)

                    for r in result:
                        try:
                            guild = await self.bot.fetch_guild(int(r["guildID"]))
                            channel = await guild.fetch_channel(int(r["channelID"]))

                            msg = r["format"] \
                                .replace("%ycn", r["name"]) \
                                .replace("%ycun", f"@{r['username']}") \
                                .replace("%link", url)

                            await channel.send(msg)
                        except Exception as e:
                            print("send error:", e)
                            continue

    except Exception as e:
        print("GLOBAL ERROR:", e)


class notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_load(self):
        self.check.start()

    def cog_unload(self):
        self.check.cancel()

    @tasks.loop(seconds=60)
    async def check(self):
        await check_videos(self)

    benachrichtigung = app_commands.Group(
        name='benachrichtigung',
        description='Youtube Notifications',
        guild_only=True
    )

    @benachrichtigung.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def youtube(
        self,
        interaction: discord.Interaction,
        modus: typing.Literal["Hinzufügen", "Entfernen"],
        kanal: discord.TextChannel,
        channelusername: str,
        channelname: str
    ):
        await interaction.response.defer()
        db = getMongoDataBase()

        # ================= ADD =================
        if modus == "Hinzufügen":
            result = await db["channels"].find_one({
                "guildID": str(interaction.guild.id),
                "channelID": str(kanal.id),
                "username": channelusername
            })

            if result:
                return await interaction.followup.send(
                    f"Bereits aktiv für @{channelusername}",
                    ephemeral=True
                )

            try:
                videos = list(scrapetube.get_channel(
                    channel_url=f"https://www.youtube.com/@{channelusername}",
                    limit=1
                ))

                if not videos:
                    raise Exception("No videos")

            except Exception as e:
                print("YouTube check error:", e)
                return await interaction.followup.send(
                    f"Kanal @{channelusername} nicht gefunden.",
                    ephemeral=True
                )

            # initial speichern
            video_ids = [video["videoId"] for video in videos]
            saved_videos = await fetch_videos_from_database(self, channelusername)

            if not saved_videos:
                for vid in video_ids:
                    await insert_video_to_database(self, channelusername, vid)

            return await interaction.response.send_modal(
                nachricht(kanal, channelname, channelusername, self.bot)
            )

        # ================= REMOVE =================
        if modus == "Entfernen":
            result = await db["channels"].find_one({
                "guildID": str(interaction.guild.id),
                "channelID": str(kanal.id),
                "username": channelusername
            })

            if not result:
                return await interaction.followup.send(
                    f"Nicht aktiv für @{channelusername}",
                    ephemeral=True
                )

            await db["channels"].delete_one({
                "guildID": str(interaction.guild.id),
                "channelID": str(kanal.id),
                "username": channelusername
            })

            await db["videos"].delete_many({
                "channel_name": channelusername
            })

            return await interaction.followup.send(
                f"Entfernt für @{channelusername}"
            )


async def setup(bot):
    await bot.add_cog(notifications(bot))
