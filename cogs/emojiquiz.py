import asyncio
import random
import typing
import discord
from discord.ext import commands
from discord import app_commands
from info import random_color

class buttons(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Nächstes Wort', style=discord.ButtonStyle.grey, custom_id="jqvefkghwkcvh", emoji="⏩")
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        acc = await open_acc(self, interaction.user)
        rucksack = int(acc[0])
        if 20 > int(rucksack):
            return await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> Du hast nicht **20 🍪** in deinem Rucksack. Es fehlen dir **{20 - rucksack} 🍪**. Entweder überweise dir die Cookies von deiner Bank in dein Rucksack oder gehe zuerst arbeiten oder betteln. Alle Commands siehst du mit `/help`.", ephemeral=True)

        await update_acc(self, interaction.user, "rucksack", 0, 20)
        
        await interaction.response.defer(thinking=False, ephemeral=True)
        m = await interaction.channel.send(f"{interaction.user.mention} hat den Begriff übersprungen. (-20 🍪)")
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT emojis, lösung, tipp FROM eqdb")
                result = await cursor.fetchall()
                a = random.randint(1, int(len(result)))
                b = 0
                for quiz in result:
                    if a == b:
                        embed = discord.Embed(color=random_color(), title="Emojiquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                        embed.add_field(name="❓ Gesuchter Begriff", value=quiz[0])
                        embed.add_field(name="❗️ Tipp", value=quiz[2])
                        embed.set_footer(text=f"Das letzte Quiz wurde übersprungen von {interaction.user}.", icon_url=interaction.user.avatar)
                        await asyncio.sleep(2)
                        await interaction.channel.purge(limit=99)
                        m2 = await interaction.channel.send(embed=embed, view=buttons(self.bot))
                        await cursor.execute("DELETE FROM eqcurrent WHERE guildID = (%s)", (interaction.guild.id))
                        await cursor.execute("INSERT INTO eqcurrent(guildID, lösung, msgID) VALUES(%s, %s, %s)", (interaction.guild.id, quiz[1], m2.id))
                        b += 100000
                    else:
                        b += 1
    
    @discord.ui.button(label='Anfangsbuchstabe', style=discord.ButtonStyle.grey, custom_id="dvekzlfdigqwjvliz", emoji="💡")
    async def letter(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT lösung FROM eqcurrent WHERE guildID = (%s)", (interaction.guild.id))
                result = await cursor.fetchone()
                await interaction.response.send_message(f"💡 Der erste Buchstabe des gesuchten Wortes ist __**{result[0][0]}**__. Mehr Tipps gebe ich aber nicht.", ephemeral=True)

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
            await cursor.execute("SELECT channelID FROM eq WHERE guildID = (%s)", (msg.guild.id))
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
            await cursor.execute("SELECT lösung FROM eqcurrent WHERE guildID = (%s)", (msg.guild.id))
            result = await cursor.fetchone()
            if result is None:
                return False
            if result[0].lower() == msg.content.lower():
                await cursor.execute("DELETE FROM eqcurrent WHERE guildID = (%s)", (msg.guild.id))
                return True
            elif result[0].lower() != msg.content.lower():
                return False
                
async def answer_correct(self, msg):
    await msg.channel.send(f"{msg.author.mention} hat den gesuchten Begriff erraten. (+10 🍪)")
    await update_acc(self, msg.author, "rucksack", 10, 0)
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT emojis, lösung, tipp FROM eqdb")
            result = await cursor.fetchall()
            a = random.randint(1, int(len(result)))
            b = 0
            for quiz in result:
                if a == b:
                    embed = discord.Embed(color=random_color(), title="Emojiquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                    embed.add_field(name="❓ Gesuchter Begriff", value=quiz[0])
                    embed.add_field(name="❗️ Tipp", value=quiz[2])
                    embed.set_footer(text=f"Das letzte Quiz wurde gelöst von {msg.author}.", icon_url=msg.author.avatar)
                    await asyncio.sleep(2)
                    await msg.channel.purge(limit=99)
                    m2 = await msg.channel.send(embed=embed, view=buttons(self.bot))
                    await cursor.execute("INSERT INTO eqcurrent(guildID, lösung, msgID) VALUES(%s, %s, %s)", (msg.guild.id, quiz[1], m2.id))
                    await cursor.execute("SELECT anzahl FROM eq_leaderboard WHERE userID = (%s)", (msg.author.id))
                    r = await cursor.fetchone()
                    if r != None:
                        await cursor.execute("UPDATE eq_leaderboard SET anzahl = (%s) WHERE userID = (%s)", (int(r[0]) + 1, msg.author.id))
                    if r == None:
                        await cursor.execute("INSERT INTO eq_leaderboard(userID, anzahl) VALUES(%s, %s)", (msg.author.id, 1))
                    b += 100000
                else:
                    b += 1

async def answer_incorrect(self, msg):
    await msg.add_reaction("<:v_kreuz:1049388811353858069>")
            
class Emojiquiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=buttons(self.bot))
        
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
            tf2 = await check_word(self, msg)
            if tf2 == True:
                await answer_correct(self, msg)
            else:
                await answer_incorrect(self, msg)
    
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def emojiquiz(self, interaction: discord.Interaction, modus: typing.Literal["Anschalten", "Ausschalten"], kanal: discord.TextChannel):
        """Verwalte das Enojiquiz deines Servers."""
        if modus == "Anschalten":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelID FROM eq WHERE guildID = (%s)", (interaction.guild.id))
                    result = await cursor.fetchone()
                    if result is None:
                        await cursor.execute("INSERT INTO eq(guildID, channelID) VALUES(%s, %s)", (interaction.guild.id, kanal.id))
                        await cursor.execute("SELECT emojis, lösung, tipp FROM eqdb")
                        result2 = await cursor.fetchall()
                        a = random.randint(1, int(len(result2)))
                        b = 0
                        for quiz in result2:
                            if a == b:
                                embed = discord.Embed(color=random_color(), title="Emojiquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                                embed.add_field(name="❓ Gesuchter Begriff", value=quiz[0])
                                embed.add_field(name="❗️ Tipp", value=quiz[2])
                                m2 = await kanal.send(embed=embed, view=buttons(self.bot))
                                await cursor.execute("INSERT INTO eqcurrent(guildID, lösung, msgID) VALUES(%s, %s, %s)", (interaction.guild.id, quiz[1], m2.id))
                                b += 100000
                                return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Das Emojiquiz wurde gestartet in {kanal.mention}.**", ephemeral=True)
                            else:
                                b += 1
                    if result is not None:
                        await cursor.execute("UPDATE eq SET channelID = (%s) WHERE guildID = (%s)", (kanal.id, interaction.guild.id))
                        await cursor.execute("SELECT emojis, lösung, tipp FROM eqdb")
                        result2 = await cursor.fetchall()
                        a = random.randint(1, int(len(result2)))
                        b = 0
                        for quiz in result2:
                            if a == b:
                                embed = discord.Embed(color=random_color(), title="Emojiquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                                embed.add_field(name="❓ Gesuchter Begriff", value=quiz[0])
                                embed.add_field(name="❗️ Tipp", value=quiz[2])
                                m2 = await kanal.send(embed=embed, view=buttons(self.bot))
                                await cursor.execute("INSERT INTO eqcurrent(guildID, lösung, msgID) VALUES(%s, %s, %s)", (interaction.guild.id, quiz[1], m2.id))
                                b += 100000
                                return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Das Emojiquiz wurde neu gestartet in {kanal.mention}.**", ephemeral=True)
                            else:
                                b += 1
        if modus == "Ausschalten":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelID FROM eq WHERE guildID = (%s)", (interaction.guild.id))
                    result = await cursor.fetchone()
                    if result is None:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Emojiquiz ist nicht in diesem Server aktiviert.**", ephemeral=True)
                    await cursor.execute("DELETE FROM eq WHERE guildID = (%s)", (interaction.guild.id))
                    return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Das Emojiquiz wurde in diesem Server ausgeschalten.**", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Emojiquiz(bot))