import asyncio
import datetime
import random
import typing
import discord
from discord.ext import commands
from discord import app_commands
from info import random_color
from info import getcolour
import os
from PIL import Image
from io import BytesIO

class buttons(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Nächste Flagge', style=discord.ButtonStyle.grey, custom_id="FlagenQuizNext", emoji="⏩")
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=False, ephemeral=True)
        acc = await open_acc(self, interaction.user)
        rucksack = int(acc[0])
        if 20 > int(rucksack):
            return await interaction.followup.send(f"<:v_kreuz:1119580775411621908> Du hast nicht **20 🍪** in deinem Rucksack. Es fehlen dir **{20 - rucksack} 🍪**. Entweder überweise dir die Cookies von deiner Bank in dein Rucksack oder gehe zuerst arbeiten oder betteln. Alle Commands siehst du mit `/help`.", ephemeral=True)

        await update_acc(self, interaction.user, "rucksack", 0, 20)
        
        m = await interaction.channel.send(f"{interaction.user.mention} hat die Flagge übersprungen. (-20 🍪)")
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                result = None
                file = False
                while file == False:
                    await cursor.execute("SELECT filename, lösung FROM fq_flaggen ORDER BY RAND() LIMIT 1")
                    result = await cursor.fetchone()
                    file = await getFile(result[0])
                embed = discord.Embed(color=await getcolour(self, interaction.user), title="Flaggenquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                embed.set_footer(text=f"Das letzte Quiz wurde übersprungen von {interaction.user}.", icon_url=interaction.user.avatar)
                embed.set_image(url=f"attachment://Flagge.png")       
                m2 = await interaction.channel.send(embed=embed, file=file, view=buttons(self.bot))
                await cursor.execute("DELETE FROM fqcurrent WHERE guildID = (%s)", (interaction.guild.id))
                await cursor.execute("INSERT INTO fqcurrent(guildID, lösung, msgID) VALUES(%s, %s, %s)", (interaction.guild.id, result[1], m2.id))

    @discord.ui.button(label='Anfangsbuchstabe', style=discord.ButtonStyle.grey, custom_id="FirstLetterFlaggenQuiz", emoji="💡")
    async def letter(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT lösung FROM fqcurrent WHERE guildID = (%s)", (interaction.guild.id))
                result = await cursor.fetchone()
                if result is not None:
                    return await interaction.followup.send(f"💡 Der erste Buchstabe der gesuchten Flagge ist __**{result[0][0]}**__. Mehr Tipps gebe ich aber nicht.", ephemeral=True)
                await interaction.followup.send(f"❌ Es gibt aktuell keine Lösung. Das Flaggenquiz wurde wahrscheinlich auf diesem Server ausgeschalten.", ephemeral=True)

async def open_acc(self, user):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SELECT rucksack, bank, job, stunden FROM economy WHERE userID = {user.id}")
            result = await cursor.fetchone()
            if result is None:
                await cursor.execute("INSERT INTO economy(rucksack, bank, job, stunden, userID) VALUES(%s, %s, %s, %s, %s)",("0", "0", "Kein Job", "0", user.id))
                
                liste = ["0","0","Kein Job","0",user.id]
                return liste
            else:
                return result

async def update_acc(self, user, mode, sum, dif):
    acc = await open_acc(self, user)
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            if mode == "rucksack":
                bal = acc[0]
                new = int(bal) + int(sum) - int(dif)
                await cursor.execute("UPDATE economy SET rucksack = (%s) WHERE userID = (%s)", (new, user.id))
                
            if mode == "bank":
                bal = acc[1]
                new = int(bal) + int(sum) - int(dif)
                await cursor.execute("UPDATE economy SET bank = (%s) WHERE userID = (%s)", (new, user.id))

async def updateLeaderbord(bot, userid):
    async with bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT anzahl FROM fq_leaderboard WHERE userID = (%s)", (userid))
            r = await cursor.fetchone()
            if r != None:
                await cursor.execute("UPDATE fq_leaderboard SET anzahl = (%s) WHERE userID = (%s)", (int(r[0]) + 1, userid))
            if r == None:
                await cursor.execute("INSERT INTO fq_leaderboard(userID, anzahl) VALUES(%s, %s)", (userid, 1))

async def check_channel(self, msg):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT channelID FROM fq WHERE guildID = (%s)", (msg.guild.id))
            result = await cursor.fetchone()
            if result is None:
                return False
            else:
                if int(result[0]) == int(msg.channel.id):
                    return True
                else:
                    return False

async def check_word(self, msg: discord.Message):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT lösung FROM fqcurrent WHERE guildID = (%s)", (msg.guild.id))
            result = await cursor.fetchone()
            if result is None:
                return False
            if result[0].lower() == msg.content.lower():
                await cursor.execute("DELETE FROM fqcurrent WHERE guildID = (%s)", (msg.guild.id))
                return True
            else:
                return False
                
async def answer_correct(self, msg):
    try:
        await msg.channel.send(f"{msg.author.mention} hat den gesuchten Begriff erraten. (+10 🍪)")
        await update_acc(self, msg.author, "rucksack", 10, 0)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                result = None
                file = False
                while file == False:
                    await cursor.execute("SELECT filename, lösung FROM fq_flaggen ORDER BY RAND() LIMIT 1")
                    result = await cursor.fetchone()
                    file = await getFile(result[0])
                embed = discord.Embed(color=await getcolour(self, msg.author), title="Flaggenquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                embed.set_image(url=f"attachment://Flagge.png")
                embed.set_footer(text=f"Das letzte Quiz wurde gelöst von {msg.author}.", icon_url=msg.author.avatar)
                m2 = await msg.channel.send(embed=embed, file=file, view=buttons(self.bot))
                await cursor.execute("INSERT INTO fqcurrent(guildID, lösung, msgID) VALUES(%s, %s, %s)", (msg.guild.id, result[1], m2.id))
                await updateLeaderbord(self.bot, msg.author.id)
    except:
        pass


async def answer_incorrect(self, msg):
    try:
        await msg.add_reaction("<:v_kreuz:1119580775411621908>")
    except: 
        pass
      
async def getFile(filename):
    try:
        file_path = f"flaggenquiz/{filename}"
        with open(file_path, "rb") as file:
            image_data = file.read()
        return discord.File(BytesIO(image_data), filename="Flagge.png")
    except Exception as e:
        return None

    
class flaggenquiz(commands.Cog):
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
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_guild=True)
    async def flaggenquiz(self, interaction: discord.Interaction, modus: typing.Literal["Anschalten", "Ausschalten"], kanal: typing.Union[discord.TextChannel, discord.ForumChannel, discord.Thread]):
        """Verwalte das Flaggenquiz deines Servers."""
        await interaction.response.defer()

        # Check Server-Anforderungen
        server = interaction.guild
        server_age = (datetime.datetime.now(datetime.timezone.utc) - server.created_at).days
        user_age = (datetime.datetime.now(datetime.timezone.utc) - interaction.user.created_at).days
        owner_age = (datetime.datetime.now(datetime.timezone.utc) - interaction.guild.owner.created_at).days

        if server_age < 10:
            return await interaction.followup.send("Der Server muss mindestens 10 Tage alt sein, um das Emoji-Quiz zu verwenden.", ephemeral=True)
        non_bot_members = sum(not member.bot for member in server.members)
        if non_bot_members < 10:
            return await interaction.followup.send("Es müssen mindestens 10 Servermitglieder ohne Bots vorhanden sein, um das Emoji-Quiz zu verwenden.", ephemeral=True)
        if owner_age < 30:
            return await interaction.followup.send("Der Account vom Serverowner muss mindestens 30 Tage alt sein, um das Emoji-Quiz zu verwenden.", ephemeral=True)
        if user_age < 30:
            return await interaction.followup.send("Dein Account muss mindestens 30 Tage alt sein, um das Emoji-Quiz zu verwenden.", ephemeral=True)

        if modus == "Anschalten":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelID FROM fq WHERE guildID = (%s)", (server.id))
                    result = await cursor.fetchone()
                    if result is None:
                        await cursor.execute("INSERT INTO fq(guildID, channelID) VALUES(%s, %s)", (server.id, kanal.id))
                        result = None
                        file = False
                        while file == False:
                            await cursor.execute("SELECT filename, lösung FROM fq_flaggen ORDER BY RAND() LIMIT 1")
                            result = await cursor.fetchone()
                            file = await getFile(result[0])
                        embed = discord.Embed(color=discord.Colour.orange(), title="Flaggenquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                        embed.set_image(url=f"attachment://Flagge.png")
                        m2 = await kanal.send(embed=embed, file=file, view=buttons(self.bot))
                        await cursor.execute("INSERT INTO fqcurrent(guildID, lösung, msgID) VALUES(%s, %s, %s)", (interaction.guild.id, result[1], m2.id))
                        return await interaction.followup.send(f"**<:v_haken:1119579684057907251> Das Flaggenquiz wurde gestartet in {kanal.mention}.**", ephemeral=True)
                    if result is not None:
                        await cursor.execute("UPDATE fq SET channelID = (%s) WHERE guildID = (%s)", (kanal.id, server.id))
                        result = None
                        file = False
                        while file == False:
                            await cursor.execute("SELECT filename, lösung FROM fq_flaggen ORDER BY RAND() LIMIT 1")
                            result = await cursor.fetchone()
                            file = await getFile(result[0])
                        embed = discord.Embed(color=discord.Colour.orange(), title="Flaggenquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                        embed.set_image(url=f"attachment://Flagge.png")
                        m2 = await kanal.send(embed=embed, file=file, view=buttons(self.bot))
                        await cursor.execute("INSERT INTO fqcurrent(guildID, lösung, msgID) VALUES(%s, %s, %s)", (interaction.guild.id, result[1], m2.id))
                        return await interaction.followup.send(f"**<:v_haken:1119579684057907251> Das Flaggenquiz wurde neu gestartet in {kanal.mention}.**", ephemeral=True)
        
        if modus == "Ausschalten":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelID FROM fq WHERE guildID = (%s)", (server.id))
                    result = await cursor.fetchone()
                    if result is None:
                        return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Das Flaggenquiz ist nicht in diesem Server aktiviert.**", ephemeral=True)
                    await cursor.execute("DELETE FROM fq WHERE guildID = (%s)", (server.id))
                    return await interaction.followup.send(f"**<:v_haken:1119579684057907251> Das Flaggenquiz wurde in diesem Server ausgeschaltet.**", ephemeral=True)

async def setup(bot):
    await bot.add_cog(flaggenquiz(bot))