import asyncio
import datetime
import random
import typing
import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import random_color, getcolour
from utils.MongoDB import getMongoDataBase 
from cogs.economy import open_acc, update_account
import time

class buttons(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Nächstes Wort', style=discord.ButtonStyle.grey, custom_id="jqvefkghwkcvh", emoji="⏩")
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        acc = await open_acc(self, interaction.user)
        rucksack = int(acc["rucksack"])
        if 20 > int(rucksack):
            return await interaction.followup.send(f"<:v_9:1264264656831119462> Du hast nicht **20 🍪** in deinem Rucksack. Es fehlen dir **{20 - rucksack} 🍪**. Entweder überweise dir die Cookies von deiner Bank in dein Rucksack oder gehe zuerst arbeiten oder betteln. Alle Commands siehst du mit `/help`.", ephemeral=True)

        await update_account(self, interaction.user, "rucksack", 0, 20)
        
        await interaction.response.defer(thinking=False, ephemeral=True)
        m = await interaction.channel.send(f"{interaction.user.mention} hat den Begriff übersprungen. (-20 🍪)")
        
        db = getMongoDataBase()
        
        result = await db["eq_begriffe"].aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Emojiquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
        embed.add_field(name="❓ Gesuchter Begriff", value=result[0]["emojis"])
        embed.add_field(name="❗️ Tipp", value=f"||{result[0]['tipp']}||")
        embed.set_footer(text=f"Das letzte Quiz wurde übersprungen von {interaction.user}.", icon_url=interaction.user.avatar)
        m2 = await interaction.channel.send(embed=embed, view=buttons(self.bot))
        await db["eqcurrent"].delete_one({"guildID": interaction.guild.id})
        await db["eqcurrent"].insert_one({"guildID": interaction.guild.id, "lösung": result[0]['begriff'], "msgID": m2.id})
    
    @discord.ui.button(label='Anfangsbuchstabe', style=discord.ButtonStyle.grey, custom_id="dvekzlfdigqwjvliz", emoji="💡")
    async def letter(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = getMongoDataBase()["eqcurrent"].find_one({"guildID": interaction.guild.id})
        if result is not None:
            return await interaction.followup.send(f"💡 Der erste Buchstabe des gesuchten Wortes ist __**{result['begriff'][0]}**__. Mehr Tipps gebe ich aber nicht.", ephemeral=True)
        await interaction.followup.send(f"❌ Es gibt aktuell keine Lösung. Das Emojiquiz wurde wahrscheinlich auf diesem Sevrer ausgeschalten.", ephemeral=True)

async def updateLeaderbord(bot, userid):
    db = getMongoDataBase()
    
    r = await db["eq_leaderboard"].find_one({"userID": userid})
    if r != None:
        await db["eq_leaderboard"].update_one(
            {"userID": userid},
            {"$set": {"anzahl": int(r[0]) + 1}}
        )
    if r == None:
        await db["eq_leaderboard"].insert_one({"userID": userid, "anzahl": 1})

async def check_channel(self, msg):
    result = getMongoDataBase()["eq"].find_one({"guildID": msg.guild.id})
    if result is None:
        return False
    else:
        if int(result["channelID"]) == int(msg.channel.id):
            return True
        else:
            return False

async def check_word(self, msg: discord.Message):
    db = getMongoDataBase()
    
    result = await db["eqcurrent"].find_one({"guildID": msg.guild.id})
    
    if result is None:
        return False
    if result["begriff"].lower() == msg.content.lower():
        await db["eqcurrent"].delete_one({"guildID": msg.guild.id})
        return True
    elif result["begriff"].lower() != msg.content.lower():
        return False
                
async def answer_correct(self, msg):
    try:
        await msg.channel.send(f"{msg.author.mention} hat den gesuchten Begriff erraten. (+10 🍪)")
        await update_account(self, msg.author, "rucksack", 10, 0)
        
        db = getMongoDataBase()
        
        result = await db["eq_begriffe"].aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
        
        embed = discord.Embed(color=await getcolour(self, msg.author), title="Emojiquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
        embed.add_field(name="❓ Gesuchter Begriff", value=result[0]["emojis"])
        embed.add_field(name="❗️ Tipp", value=f"||{result[0]['tipp']}||")
        embed.set_footer(text=f"Das letzte Quiz wurde gelöst von {msg.author}.", icon_url=msg.author.avatar)
        m2 = await msg.channel.send(embed=embed, view=buttons(self.bot))
        
        
        await db["eqcurrent"].insert_one({"guildID": msg.guild.id, "lösung": result[0]['begriff'], "msgID": m2.id})
        await updateLeaderbord(self.bot, msg.author.id)
    except:
        pass


async def answer_incorrect(self, msg):
    try:
        await msg.add_reaction("<:v_9:1264264656831119462>")
    except: 
        pass
            
class Emojiquiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=buttons(self.bot))
        
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        tf1 = await check_channel(self, msg)
        if tf1 == False:
            return
        else:
            if msg.guild == None:
                return
            if msg.author.bot:
                return
            user_age = (datetime.datetime.now(datetime.timezone.utc) - msg.author.created_at).days
            if user_age < 30:
                return await msg.add_reaction("🧐")
            tf2 = await check_word(self, msg)
            if tf2 == True:
                if msg:
                    await answer_correct(self, msg)
            else:
                if msg:
                    await answer_incorrect(self, msg)
    
    @app_commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.has_permissions(kick_members=True)
    async def emojiquiz(self, interaction: discord.Interaction, modus: typing.Literal["Anschalten", "Ausschalten"], kanal: typing.Union[discord.TextChannel, discord.ForumChannel, discord.Thread]):
        """Verwalte das Emoji-Quiz deines Servers."""

        await interaction.response.defer()

        # Check Server-Anforderungen
        #server = interaction.guild
        #server_age = (datetime.datetime.now(datetime.timezone.utc) - server.created_at).days
        #user_age = (datetime.datetime.now(datetime.timezone.utc) - interaction.user.created_at).days
        #owner_age = (datetime.datetime.now(datetime.timezone.utc) - interaction.guild.owner.created_at).days


        #if server_age < 10:
        #    return await interaction.followup.send("Der Server muss mindestens 10 Tage alt sein, um das Emoji-Quiz zu verwenden.", ephemeral=True)
        #non_bot_members = sum(not member.bot for member in server.members)
        #if non_bot_members < 10:
        #    return await interaction.followup.send("Es müssen mindestens 10 Servermitglieder ohne Bots vorhanden sein, um das Emoji-Quiz zu verwenden.", ephemeral=True)
        #if owner_age < 30:
        #    return await interaction.followup.send("Der Account vom Serverowner muss mindestens 30 Tage alt sein, um das Emoji-Quiz zu verwenden.", ephemeral=True)
        #if user_age < 30:
        #    return await interaction.followup.send("Dein Account muss mindestens 30 Tage alt sein, um das Emoji-Quiz zu verwenden.", ephemeral=True)
        
        db = getMongoDataBase()

        if modus == "Anschalten":
            result = await db["eq"].find_one({"guildID": interaction.guild.id})
            if result is None:
                await db["eq"].insert_one({"guildID": interaction.guild.id, "channelID": kanal.id})
                result = await db["eq_begriffe"].aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
               
                embed = discord.Embed(color=await getcolour(self, interaction.user), title="Emojiquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                embed.add_field(name="❓ Gesuchter Begriff", value=result[0]["emojis"])
                embed.add_field(name="❗️ Tipp", value=f"||{result[0]['tipp']}||")
                embed.set_footer(text=f"Das letzte Quiz wurde übersprungen von {interaction.user}.", icon_url=interaction.user.avatar)
                m2 = await interaction.channel.send(embed=embed, view=buttons(self.bot))
                await db["eqcurrent"].delete_one({"guildID": interaction.guild.id})
                await db["eqcurrent"].insert_one({"guildID": interaction.guild.id, "lösung": result[0]['begriff'], "msgID": m2.id})
            if result is not None:
                await db["eq"].update_one({"guildID": interaction.guild.id}, {"$set": {"channelID": kanal.id}})
                
                result = await db["eq_begriffe"].aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
                
                embed = discord.Embed(color=await getcolour(self, interaction.user), title="Emojiquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                embed.add_field(name="❓ Gesuchter Begriff", value=result[0]["emojis"])
                embed.add_field(name="❗️ Tipp", value=f"||{result[0]['tipp']}||")
                embed.set_footer(text=f"Das letzte Quiz wurde übersprungen von {interaction.user}.", icon_url=interaction.user.avatar)
                m2 = await interaction.channel.send(embed=embed, view=buttons(self.bot))
                await db["eqcurrent"].delete_one({"guildID": interaction.guild.id})
                await db["eqcurrent"].insert_one({"guildID": interaction.guild.id, "lösung": result[0]["begriff"], "msgID": m2.id})
        if modus == "Ausschalten":
            result = await db["eq"].find_one({"guildID": interaction.guild.id})
            if result is None:
                return await interaction.followup.send("**<:v_9:1264264656831119462> Das Emojiquiz ist nicht in diesem Server aktiviert.**", ephemeral=True)
            await db["eq"].delete_one({"guildID": interaction.guild.id})
            return await interaction.followup.send(f"**<:v_158:1264268251916009553> Das Emojiquiz wurde in diesem Server ausgeschaltet.**", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Emojiquiz(bot))