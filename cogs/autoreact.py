import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import getcolour
from utils.MongoDB import getMongoDataBase

class Autoreact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild is None:
            return

        if msg.author.bot:
            return

        await checkAndCorrectDocuments(msg.channel.id, msg.guild.id)

        result = await getMongoDataBase()["autoreact"].find({
            "guildID": str(msg.guild.id),
            "channelID": str(msg.channel.id)
        }).to_list(length=None)

        if not result:
            return

        for e in result:
            try:
                emoji = discord.PartialEmoji.from_str(e["emoji"])
                if emoji is None:
                    continue
                await msg.add_reaction(emoji)
            except:
                continue

        await self.bot.process_commands(msg)

    autoreact = app_commands.Group(
        name='autoreact',
        description='Nehme Einstellungen am Autoreactsystem vor.',
        guild_only=True
    )

    @autoreact.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.describe(emoji="Für normale emojis: name:id oder für Animierte: a:name:id")
    async def add(self, interaction: discord.Interaction, kanal: discord.TextChannel, emoji: str):
        """Füge ein Emoji für einem Kanal hinzu."""

        await interaction.response.defer()

        db = getMongoDataBase()

        try:
            emoj = discord.PartialEmoji.from_str(emoji)
            if emoj is None:
                return await interaction.followup.send(
                    "**<:v_x:1264270921452224562> Emoji ungültig. Format: name:id oder a:name:id**",
                    ephemeral=True
                )

            await checkAndCorrectDocuments(kanal.id, interaction.guild.id)

            existing = await db["autoreact"].find({
                "guildID": str(interaction.guild.id),
                "channelID": str(kanal.id)
            }).to_list(length=None)

            for existingEmoji in existing:
                if existingEmoji["emoji"] == str(emoj):
                    return await interaction.followup.send(
                        "**<:v_x:1264270921452224562> Emoji bereits vorhanden.**",
                        ephemeral=True
                    )

            await db["autoreact"].insert_one({
                "guildID": str(interaction.guild.id),
                "channelID": str(kanal.id),
                "emoji": str(emoj)
            })

            await interaction.followup.send(
                f"**<:v_checkmark:1264271011818242159> Autoreact gesetzt für {kanal.mention}: {emoj}**"
            )

        except:
            return await interaction.followup.send(
                "**<:v_x:1264270921452224562> Fehler beim Emoji.**",
                ephemeral=True
            )

    @autoreact.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def remove(self, interaction: discord.Interaction, kanal: discord.TextChannel, emoji: str):
        """Entferne Autoreacts eines Kanals."""

        await interaction.response.defer()

        db = getMongoDataBase()

        await checkAndCorrectDocuments(kanal.id, interaction.guild.id)

        result = await db["autoreact"].find({
            "guildID": str(interaction.guild.id),
            "channelID": str(kanal.id)
        }).to_list(length=None)

        if not result:
            return await interaction.followup.send(
                "**<:v_x:1264270921452224562> Keine Autoreacts vorhanden.**",
                ephemeral=True
            )

        try:
            processedEmoji = discord.PartialEmoji.from_str(emoji)
        except:
            return await interaction.followup.send(
                "**<:v_x:1264270921452224562> Emoji ungültig.**",
                ephemeral=True
            )

        if processedEmoji is None:
            return await interaction.followup.send(
                "**<:v_x:1264270921452224562> Emoji ungültig.**",
                ephemeral=True
            )

        found = False

        for document in result:
            if document["emoji"] == str(processedEmoji):
                found = True
                break

        if not found:
            return await interaction.followup.send(
                "**<:v_x:1264270921452224562> Emoji nicht gefunden.**",
                ephemeral=True
            )

        await db["autoreact"].delete_one({
            "guildID": str(interaction.guild.id),
            "channelID": str(kanal.id),
            "emoji": str(processedEmoji)
        })

        await interaction.followup.send(
            "**<:v_checkmark:1264271011818242159> Autoreact entfernt.**"
        )

    @autoreact.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def liste(self, interaction: discord.Interaction):
        """Liste aller Autoreacts."""

        await interaction.response.defer()

        result = await getMongoDataBase()["autoreact"].find({
            "guildID": str(interaction.guild.id)
        }).to_list(length=None)

        if not result:
            return await interaction.followup.send(
                "**<:v_x:1264270921452224562> Keine Autoreacts vorhanden.**",
                ephemeral=True
            )

        embed = discord.Embed(
            title="Autoreacts",
            description="Übersicht:",
            color=await getcolour(self, interaction.user)
        )

        for autoreact in result:
            try:
                channel = await interaction.guild.fetch_channel(int(autoreact["channelID"]))
                emoji = discord.PartialEmoji.from_str(autoreact["emoji"])
                embed.add_field(
                    name=channel.mention,
                    value=str(emoji),
                    inline=False
                )
            except:
                continue

        await interaction.followup.send(embed=embed)


async def checkAndCorrectDocuments(channelID, guildID):
    db = getMongoDataBase()

    result = await db["autoreact"].find_one({
        "guildID": str(guildID),
        "channelID": str(channelID)
    })

    if result is None:
        return

    emojis = result["emoji"].split(" ")

    if len(emojis) > 1:
        await db["autoreact"].delete_one({
            "guildID": str(guildID),
            "channelID": str(channelID)
        })

        for e in emojis:
            await db["autoreact"].insert_one({
                "guildID": str(guildID),
                "channelID": str(channelID),
                "emoji": e
            })


async def setup(bot):
    await bot.add_cog(Autoreact(bot))
