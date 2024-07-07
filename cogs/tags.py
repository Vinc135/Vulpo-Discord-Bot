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
        
        a = await db['tags'].find({"guildID": interaction.guild.id}).to_list()
        
        if len(a) >= 3:
            return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Du kannst keine weiteren Befehle erstellen, da du das Limit erreicht hast**")

        result = db['tags'].find_one({"guildID": interaction.guild.id, "name": name})
        
        if result != None:
            return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Dieser Tag existiert bereits. Wähle bitte einen anderen Namen.**")
        
        db['tags'].insert_one({"guildID": interaction.guild.id, "name": name, "output": output})
        
        await interaction.followup.send(f"**<:v_haken:1119579684057907251> Tag erstellt. Wenn jemand `v!{name}` schreibt, kommt dieser Text:**\n*{output}*.")

    @tag.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def delete(self, interaction: discord.Interaction, name: str):
        """Entferne einen Tag."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = db['tags'].find_one({"guildID": interaction.guild.id, "name": name})
        
        if result == None:
            await interaction.followup.send("**<:v_kreuz:1119580775411621908> Dieser Tag existiert nicht. Füge einen Tag mit `/tag add <name> <output>` hinzu.", ephemeral=True)
            return
        
        db['tags'].delete_one({"guildID": interaction.guild.id, "name": name})
        
        await interaction.followup.send(f"**<:v_haken:1119579684057907251> Tag gelöscht.**")

    @tag.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def liste(self, interaction: discord.Interaction):
        """Erhalte eine Liste von den Tags."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = db['tags'].find({"guildID": interaction.guild.id})
        
        if result == None:
            await interaction.followup.send("**<:v_kreuz:1119580775411621908> Hier wurden keine Tags gefunden. Füge einen Tag mit `/tag add <name> <output>` hinzu**", ephemeral=True)
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
        
        result = db['tags'].find({"guildID": msg.guild.id}).to_list()
        
        if result is None or len(result) == 0:
            return
        
        for message in result:
            if message is None:
                return
            
            if f"v!{str(message[0]).lower()}" == msg.content.lower():
                embed = discord.Embed(title=f"__{message[0].upper()}__", description=message[1], color=await getcolour(self, msg.author))
                
                embed.set_thumbnail(url=msg.guild.icon)
                embed.set_author(name=msg.author, icon_url=msg.author.avatar)
                await msg.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Tags(bot))