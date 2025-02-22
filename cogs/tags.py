import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import getcolour, haspremium_forserver
from utils.MongoDB import getMongoDataBase

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    tag = app_commands.Group(name='tag', description='Erstelle und lösche Tags.', guild_only=True)

    @tag.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add(self, interaction: discord.Interaction, name: str, output: str):
        """Füge einen Tag hinzu."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        a = await db['tags'].find({"guildID": str(interaction.guild.id)}).to_list(length=None)
        
        if len(a) >= 3:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Du kannst keine weiteren Befehle erstellen, da du das Limit erreicht hast**")

        result = db['tags'].find_one({"guildID": str(interaction.guild.id), "name": name})
        
        if result != None:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Dieser Tag existiert bereits. Wähle bitte einen anderen Namen.**")
        
        db['tags'].insert_one({"guildID": str(interaction.guild.id), "name": name, "output": output})
        
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Tag erstellt. Wenn jemand `v!{name}` schreibt, kommt dieser Text:**\n*{output}*.")

    @tag.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def delete(self, interaction: discord.Interaction, name: str):
        """Entferne einen Tag."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = db['tags'].find_one({"guildID": str(interaction.guild.id), "name": name})
        
        if result == None:
            await interaction.followup.send("**<:v_x:1264270921452224562> Dieser Tag existiert nicht. Füge einen Tag mit `/tag add <name> <output>` hinzu.", ephemeral=True)
            return
        
        db['tags'].delete_one({"guildID": str(interaction.guild.id), "name": name})
        
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Tag gelöscht.**")

    @tag.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def liste(self, interaction: discord.Interaction):
        """Erhalte eine Liste von den Tags."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = await db['tags'].find({"guildID": str(interaction.guild.id)}).to_list(length=None)
        
        if result == None:
            await interaction.followup.send("**<:v_x:1264270921452224562> Hier wurden keine Tags gefunden. Füge einen Tag mit `/tag add <name> <output>` hinzu**", ephemeral=True)
            return
        
        embed = discord.Embed(title="Alle Tags des Servers", description="Hier nähere Infos:", color=await getcolour(self, interaction.user))
        
        for i in result:
            embed.add_field(name=i['name'], value=f"Antwort: *{i['output']}*")
            
        await interaction.followup.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot:
            return
        
        db = getMongoDataBase()
        
        result = await db['tags'].find({"guildID": str(msg.guild.id)}).to_list(length=None)
        
        if result is None or len(result) == 0:
            return
        
        for message in result:
            if message is None:
                return
            
            if f"v!{str(message['name']).lower()}" == msg.content.lower():
                embed = discord.Embed(title=f"__{message['name'].upper()}__", description=message['output'], color=await getcolour(self, msg.author))
                
                embed.set_thumbnail(url=msg.guild.icon)
                embed.set_author(name=msg.author, icon_url=msg.author.avatar)
                await msg.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Tags(bot))