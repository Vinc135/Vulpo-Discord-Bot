import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import getcolour, haspremium_forserver
from utils.MongoDB import getMongoDataBase

class Autoreact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        
        
        result = getMongoDataBase()["autoreact"].find_one({"guildID": str(msg.guild.id), "channelID": str(msg.channel.id)})
        
        if result == None or result == "()":
            return
        for e in result:
            try:
                emoji = discord.PartialEmoji.from_str(e[0])
                if emoji == None:
                    return
                await msg.add_reaction(emoji)
            except:
                return

    autoreact = app_commands.Group(name='autoreact', description='Nehme Einstellungen am Autoreactsystem vor.', guild_only=True)

    @autoreact.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.describe(emoji="Für normale filename: name:id oder für Animierte: a:name:id")
    async def add(self, interaction: discord.Interaction, kanal: discord.TextChannel, emoji: str):
        """Füge ein Emoji für ein Kanal hinzu."""
        
        await interaction.response.defer()
        db = getMongoDataBase()
        
        try:
            await interaction.response.defer()
            emoj = discord.PartialEmoji.from_str(emoji)
            if emoj is None:
                return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Der Emoji wurde nicht gefunden. Stelle sicher dass dieses Emoji auf einem Server ist, auf dem ich auch bin und dass du das Format eingehalten hast:\n`Für normale filename: name:id oder für Animierte: a:name:id`**", ephemeral=True)
            
            
            existing = await db["autoreact"].find({"guildID": str(interaction.guild.id), "channelID": str(kanal.id)}).to_list(length=None)
            
            premium = await haspremium_forserver(self, interaction.guild)
            
            if not premium and len(existing) >= 2:
                return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Du kannst keine weiteren Reaktionen für diesen Kanal erstellen, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")

            await db["autoreact"].insert_one({"guildID": str(interaction.guild.id), "channelID": str(kanal.id), "emoji": str(emoji)})
            await interaction.followup.send(f"**<:v_haken:1119579684057907251> Eintrag erstellt. Jede Nachricht aus dem Kanal {kanal.mention} erhält das Emoji {emoj}.**")
        except:
            return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Der Emoji wurde nicht gefunden. Stelle sicher dass dieses Emoji auf einem Server ist, auf dem ich auch bin und dass du das Format eingehalten hast:\n`Für normale filename: name:id oder für Animierte: a:name:id`**", ephemeral=True)

    @autoreact.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def delete(self, interaction: discord.Interaction, kanal: discord.TextChannel):
        """Entferne Autofilename eines Kanals."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = db["autoreact"].find_one({"guildID": str(interaction.guild.id), "channelID": str(kanal.id)})
        if result == None or result == "()":
            await interaction.followup.send("**<:v_kreuz:1119580775411621908> In dem Kanal ist keine Autoreaktion eingestellt.**", ephemeral=True)
            return
        await db["autoreact"].delete_one({"guildID": str(interaction.guild.id), "channelID": str(kanal.id)})
        await interaction.followup.send(f"**<:v_haken:1119579684057907251> Einträge gelöscht.**")

    @autoreact.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def liste(self, interaction: discord.Interaction):
        """Erhalte eine Liste von den Autofilename und deren Kanäle."""
        
        await interaction.response.defer()
        
        result = getMongoDataBase()["autoreact"].find({"guildID": str(interaction.guild.id)})
        if result == ():
            await interaction.followup.send("**<:v_kreuz:1119580775411621908> Hier gibt es keine autofilename. Füge eine mit `/autoreact add <kanal> <emoji>` hinzu**", ephemeral=True)
            return
        embed = discord.Embed(title="Alle automatische filename in Kanälen", description="Hier nähere Infos:", color=await getcolour(self, interaction.user))
        
        for i in result:
            k = interaction.guild.get_channel(int(i[1]))
            if k is not None:
                channel = k
            if k is None:
                k = "Kanal veraltet"
            emoj = discord.PartialEmoji.from_str(i[0])
            if emoj is None:
                emoj = "Emoji veraltet"
            embed.add_field(name=channel.mention, value=emoj)
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Autoreact(bot))