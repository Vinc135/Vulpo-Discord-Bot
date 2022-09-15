import asyncio
import random
import typing
import discord
from discord.ext import commands
from discord import app_commands
from info import random_color

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


async def check_channel(self, msg):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT channelID FROM gtn WHERE guildID = (%s)", (msg.guild.id))
            result = await cursor.fetchone()
            if result is None:
                return False
            else:
                if int(result[0]) == int(msg.channel.id):
                    return True
                else:
                    return False

async def check_number(self, msg: discord.Message):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT zahl FROM gtncurrent WHERE guildID = (%s)", (msg.guild.id))
            result = await cursor.fetchone()
            if result is None:
                return False
            if int(result[0]) == int(msg.content):
                await cursor.execute("DELETE FROM gtncurrent WHERE guildID = (%s)", (msg.guild.id))
                return True
            elif int(result[0]) != int(msg.content):
                return False
                
async def answer_correct(self, msg):
    await msg.channel.send(f"{msg.author.mention} hat die gesuchte Zahl erraten. (+10 🍪)")
    await update_acc(self, msg.author, "rucksack", 10, 0)
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            a = random.randint(20, 100)
            b = random.randint(1, a)
            embed = discord.Embed(color=random_color(), title="Guess the number", description=f"Ich habe mir eine Zahl zwischen **1** und **{a}** ausgedacht. Kannst du sie erraten?")
            embed.set_footer(text=f"Die letzte Zahl wurde erraten von {msg.author}.", icon_url=msg.author.avatar)
            await asyncio.sleep(2)
            m2 = await msg.channel.send(embed=embed)
            await cursor.execute("INSERT INTO gtncurrent(guildID, zahl, msgID) VALUES(%s, %s, %s)", (msg.guild.id, b, m2.id))

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
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def guessthenumber(self, interaction: discord.Interaction, modus: typing.Literal["Anschalten", "Ausschalten"], kanal: discord.TextChannel):
        """Verwalte das Minispiel 'Guess the number' auf deinem Server."""
        a = random.randint(20, 100)
        b = random.randint(1, a)
        if modus == "Anschalten":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelID FROM gtn WHERE guildID = (%s)", (interaction.guild.id))
                    result = await cursor.fetchone()
                    if result is None:
                        await cursor.execute("INSERT INTO gtn(guildID, channelID) VALUES(%s, %s)", (interaction.guild.id, kanal.id))
                        embed = discord.Embed(color=random_color(), title="Guess the number", description=f"Ich habe mir eine Zahl zwischen **1** und **{a}** ausgedacht. Kannst du sie erraten?")
                        m2 = await interaction.channel.send(embed=embed)
                        await cursor.execute("INSERT INTO gtncurrent(guildID, zahl, msgID) VALUES(%s, %s, %s)", (interaction.guild.id, b, m2.id))
                        return await interaction.response.send_message(f"**✅ Guess the number wurde gestartet in {kanal.mention}.**", ephemeral=True)
                    if result is not None:
                        await cursor.execute("UPDATE gtn SET channelID = (%s) WHERE guildID = (%s)", (kanal.id, interaction.guild.id))
                        embed = discord.Embed(color=random_color(), title="Guess the number", description=f"Ich habe mir eine Zahl zwischen **1** und **{a}** ausgedacht. Kannst du sie erraten?")
                        m2 = await interaction.channel.send(embed=embed)
                        await cursor.execute("INSERT INTO gtncurrent(guildID, zahl, msgID) VALUES(%s, %s, %s)", (interaction.guild.id, b, m2.id))
                        return await interaction.response.send_message(f"**✅ Guess the number wurde neu gestartet in {kanal.mention}.**", ephemeral=True)
                    
        if modus == "Ausschalten":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelID FROM eq WHERE guildID = (%s)", (interaction.guild.id))
                    result = await cursor.fetchone()
                    if result is None:
                        return await interaction.response.send_message("**❌ Guess the number ist nicht in diesem Server aktiviert.**", ephemeral=True)
                    await cursor.execute("DELETE FROM eq WHERE guildID = (%s)", (interaction.guild.id))
                    return await interaction.response.send_message(f"**✅ Guess the number wurde in diesem Server ausgeschalten.**", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Guessthenumber(bot))