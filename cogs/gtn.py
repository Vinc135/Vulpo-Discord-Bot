import asyncio
import random
import typing
import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import random_color, getcolour
from utils.MongoDB import getMongoDataBase
from cogs.economy import open_acc, update_account

async def check_channel(self, msg):
    result = await getMongoDataBase()["gtn"].find_one({"guildID": str(msg.guild.id)})
    if result is None:
        return False
    else:
        if int(result["channelID"]) == int(msg.channel.id):
            return True
        else:
            return False

async def check_number(self, msg: discord.Message):
    db = getMongoDataBase()
    
    result = await db["gtncurrent"].find_one({"guildID": str(msg.guild.id)})
    
    if result is None:
        return False
    try:
        if int(result["number"]) == int(msg.content):
            await db["gtncurrent"].delete_one({"guildID": str(msg.guild.id)})
            return True
        else:
            return False
    except:
        pass
                
async def answer_correct(self, msg):
    await msg.channel.send(f"{msg.author.mention} hat die gesuchte Zahl erraten. (+10 🍪)")
    await update_account(self, msg.author, "rucksack", 10, 0)

    a = random.randint(20, 100)
    b = random.randint(1, a)
    embed = discord.Embed(color=await getcolour(self, msg.author), title="Guess the number", description=f"Ich habe mir eine Zahl zwischen **1** und **{a}** ausgedacht. Kannst du sie erraten?")
    embed.set_footer(text=f"Die letzte Zahl wurde erraten von {msg.author}.", icon_url=msg.author.avatar)
    await asyncio.sleep(2)
    m2 = await msg.channel.send(embed=embed)
    
    await getMongoDataBase()["gtncurrent"].insert_one({"guildID": str(msg.guild.id), "zahl": b, "msgID": m2.id})

async def answer_incorrect(self, msg):
    pass
            
class Guessthenumber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.guild == None:
            return
        if msg.author.bot:
            return
        tf1 = await check_channel(self, msg)
        if tf1 == False:
            return
        else:
            tf2 = await check_number(self, msg)
            if tf2 == True:
                await answer_correct(self, msg)
            else:
                await answer_incorrect(self, msg)
    
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def guessthenumber(self, interaction: discord.Interaction, modus: typing.Literal["Anschalten", "Ausschalten"], kanal: typing.Union[discord.TextChannel, discord.ForumChannel, discord.Thread]):
        """Verwalte das Minispiel 'Guess the number' auf deinem Server."""
        
        await interaction.response.defer()
        
        a = random.randint(20, 100)
        b = random.randint(1, a)
        
        db = getMongoDataBase()
        
        if modus == "Anschalten":
            
            result = await db["gtn"].find_one({"guildID": interaction.guild.id})
            if result is None:
                db["gtn"].insert_one({"guildID": interaction.guild.id, "channelID": kanal.id})
                embed = discord.Embed(color=await getcolour(self, interaction.user), title="Guess the number", description=f"Ich habe mir eine Zahl zwischen **1** und **{a}** ausgedacht. Kannst du sie erraten?")
                
                m2 = await kanal.send(embed=embed)
                db["gtncurrent"].insert_one({"guildID": interaction.guild.id, "zahl": b, "msgID": m2.id})
                return await interaction.followup.send(f"**<:v_haken:1119579684057907251> Guess the number wurde gestartet in {kanal.mention}.**", ephemeral=True)
            if result is not None:
                db["gtn"].update_one({"guildID": interaction.guild.id}, {"$set": {"channelID": kanal.id}})
                embed = discord.Embed(color=await getcolour(self, interaction.user), title="Guess the number", description=f"Ich habe mir eine Zahl zwischen **1** und **{a}** ausgedacht. Kannst du sie erraten?")
                
                m2 = await kanal.send(embed=embed)
                db["gtncurrent"].update_one({"guildID": interaction.guild.id}, {"$set": {"zahl": b, "msgID": m2.id}})
                return await interaction.followup.send(f"**<:v_haken:1119579684057907251> Guess the number wurde neu gestartet in {kanal.mention}.**", ephemeral=True)
                    
        if modus == "Ausschalten":
            await db["gtn"].find_one({"guildID": interaction.guild.id})
            if result is None:
                return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Guess the number ist nicht in diesem Server aktiviert.**", ephemeral=True)
            
            await db["gtn"].delete_one({"guildID": interaction.guild.id})
            return await interaction.followup.send(f"**<:v_haken:1119579684057907251> Guess the number wurde in diesem Server ausgeschalten.**", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Guessthenumber(bot))