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
        
        await checkAndCorrectDocuments(msg.channel.id, msg.guild.id)
        
        result = await getMongoDataBase()["autoreact"].find({"guildID": str(msg.guild.id), "channelID": str(msg.channel.id)}).to_list(length=None)
        if result == [] or result == None:
            return
        
        for e in result:
            try:
                emoji = discord.PartialEmoji.from_str(e[0])
                if emoji == None:
                    continue
                await msg.add_reaction(emoji)
            except:
                continue

    autoreact = app_commands.Group(name='autoreact', description='Nehme Einstellungen am Autoreactsystem vor.', guild_only=True)

    @autoreact.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.describe(emoji="Für normale emojis: name:id oder für Animierte: a:name:id")
    async def add(self, interaction: discord.Interaction, kanal: discord.TextChannel, emoji: str):
        """Füge ein Emoji für ein Kanal hinzu."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        try:
            emoj = discord.PartialEmoji.from_str(emoji)
            if emoj is None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Der Emoji wurde nicht gefunden. Stelle sicher dass dieses Emoji auf einem Server ist, auf dem ich auch bin und dass du das Format eingehalten hast:\n`Für normale Emojis: name:id oder für Animierte: a:name:id`**", ephemeral=True)
            
            await checkAndCorrectDocuments(kanal.id, str(interaction.guild.id))
            
            existing = await db["autoreact"].find({"guildID": str(str(interaction.guild.id)), "channelID": str(kanal.id)}).to_list(length=None)
            
            for existingEmoji in existing:
                print (existingEmoji["emoji"])
                print (str(emoj))
                if existingEmoji["emoji"] == str(emoj):
                    return await interaction.followup.send("**<:v_x:1264270921452224562> Dieses Emoji wurde bereits hinzugefügt.**", ephemeral=True)
            
            premium = await haspremium_forserver(self, interaction.guild)
            
            if not premium and len(existing) >= 2:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Du kannst keine weiteren Reaktionen für diesen Kanal erstellen, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")

            await db["autoreact"].insert_one({"guildID": str(str(interaction.guild.id)), "channelID": str(kanal.id), "emoji": str(emoj)})
            await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Eintrag erstellt. Jede Nachricht aus dem Kanal {kanal.mention} erhält das Emoji {emoj}.**")
        except discord.errors.NotFound as e:
            print(e)
            return await interaction.followup.send("**<:v_x:1264270921452224562> Der Emoji wurde nicht gefunden. Stelle sicher dass dieses Emoji auf einem Server ist, auf dem ich auch bin und dass du das Format eingehalten hast:\n`Für normale filename: name:id oder für Animierte: a:name:id`**", ephemeral=True)

    @autoreact.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def remove(self, interaction: discord.Interaction, kanal: discord.TextChannel, emoji: str):
        """Entferne Autoreacts eines Kanals."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        await checkAndCorrectDocuments(kanal.id, str(interaction.guild.id))
        
        result = await db["autoreact"].find({"guildID": str(str(interaction.guild.id)), "channelID": str(kanal.id)}).to_list(length=None)
        
        if result == [] or result == None:
            await interaction.followup.send("**<:v_x:1264270921452224562> In dem Kanal ist keine Autoreaktion eingestellt.**", ephemeral=True)
            return
        
        processedEmoji = None
        
        try:
            processedEmoji = discord.PartialEmoji.from_str(emoji)
        except:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Der Emoji wurde nicht gefunden. Stelle sicher dass dieses Emoji auf einem Server ist, auf dem ich auch bin und dass du das Format eingehalten hast:\n`Für normale filename: name:id oder für Animierte: a:name:id`**", ephemeral=True)
        
        if processedEmoji is None:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Der Emoji wurde nicht gefunden. Stelle sicher dass dieses Emoji auf einem Server ist, auf dem ich auch bin und dass du das Format eingehalten hast:\n`Für normale filename: name:id oder für Animierte: a:name:id`**", ephemeral=True)
        
        found = False
        
        for document in result:
            if document["emoji"] == str(processedEmoji):
                found = True
                break
            
        if not found:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Dieser Emoji wurde noch nicht hinzugefügt. Füge ihn mit /autoreact add <emoji> hinzu**", ephemeral=True)
        
        await db["autoreact"].delete_one({"guildID": str(str(interaction.guild.id)), "channelID": str(kanal.id), "emoji": str(emoji)})
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Einträg gelöscht.**")

    @autoreact.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def liste(self, interaction: discord.Interaction):
        """Erhalte eine Liste von den Autoreacts und deren Kanäle."""
        
        await interaction.response.defer()
        
        await checkAndCorrectDocuments(interaction.channel.id, str(interaction.guild.id))

        result = await getMongoDataBase()["autoreact"].find({"guildID": str(str(interaction.guild.id))}).to_list(length=None)
        
        if result == [] or result == None:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Hier gibt es keine autoreacts. Füge eine mit `/autoreact add <kanal> <emoji>` hinzu**", ephemeral=True)

        embed = discord.Embed(title="Alle autoreacts in Kanälen", description="Hier nähere Infos:", color=await getcolour(self, interaction.user))

        for autoreact in result:
            try:
                channel = await interaction.guild.fetch_channel(int(autoreact["channelID"]))
            
                if channel is None or channel.mention is None:
                    continue
        
                emoji = discord.PartialEmoji.from_str(autoreact["emoji"])
                if emoji is None:
                    emoji = "Emoji veraltet"
                embed.add_field(name=channel, value=str(emoji))
            except discord.errors.NotFound as e:
                continue

        await interaction.followup.send(embed=embed)

async def checkAndCorrectDocuments(channelID, guildID):
    db = getMongoDataBase()
    
    result = await db["autoreact"].find_one({"guildID": str(guildID), "channelID": str(channelID)})
    
    if result is None:
        return
    
    emojis = result["emoji"].split(" ")
    
    if len(emojis) > 1:
        await db["autoreact"].delete_one({"guildID": str(guildID), "channelID": str(channelID)})
        for e in emojis:
            await db["autoreact"].insert_one({"guildID": str(guildID), "channelID": str(channelID), "emoji": e}) 

async def setup(bot):
    await bot.add_cog(Autoreact(bot))