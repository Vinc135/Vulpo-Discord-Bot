import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime
import mysql.connector
from info import get_syntax
##########
jobs = [{"name": "Küchenhilfe", "req": 0, "desc": "\nVerdiene zwischen 20 und 30 Münzen pro Stunde.\nDu musst mindestens **0** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [20, 30]},
        {"name": "Kassierer", "req": 5, "desc": "\nVerdiene zwischen 30 und 40 Münzen pro Stunde.\nDu musst mindestens **5** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [30, 40]},
        {"name": "Dönermann", "req": 10, "desc": "\nVerdiene zwischen 40 und 50 Münzen pro Stunde.\nDu musst mindestens **10** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [40, 50]},
        {"name": "Elektroniker", "req": 15, "desc": "\nVerdiene zwischen 50 und 60 Münzen pro Stunde.\nDu musst mindestens **15** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [50, 60]},
        {"name": "Pfleger", "req": 20, "desc": "\nVerdiene zwischen 60 und 70 Münzen pro Stunde.\nDu musst mindestens **20** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [60, 70]},
        {"name": "Bäcker", "req": 25, "desc": "\nVerdiene zwischen 70 und 80 Münzen pro Stunde.\nDu musst mindestens **25** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [70, 80]},
        {"name": "Bauarbeiter", "req": 30, "desc": "\nVerdiene zwischen 80 und 90 Münzen pro Stunde.\nDu musst mindestens **30** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [80, 90]},
        {"name": "Gärtner", "req": 35, "desc": "\nVerdiene zwischen 90 und 100 Münzen pro Stunde.\nDu musst mindestens **35** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [90, 100]},
        {"name": "Lehrer", "req": 40, "desc": "\nVerdiene zwischen 100 und 110 Münzen pro Stunde.\nDu musst mindestens **40** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [100, 110]},
        {"name": "Koch", "req": 45, "desc": "\nVerdiene zwischen 110 und 120 Münzen pro Stunde.\nDu musst mindestens **45** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [110, 120]},
        {"name": "Sanitäter", "req": 50, "desc": "\nVerdiene zwischen 120 und 130 Münzen pro Stunde.\nDu musst mindestens **50** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [120, 130]},
        {"name": "TV-Moderator", "req": 60, "desc": "\nVerdiene zwischen 130 und 140 Münzen pro Stunde.\nDu musst mindestens **60** Stunden gearbeitet haben, um diesen Job freizuschalten.",
         "amt": [130, 140]},
        {"name": "Schauspieler", "req": 70, "desc": "\nVerdiene zwischen 140 und 150 Münzen pro Stunde.\nDu musst mindestens **70** Stunden gearbeitet haben, um diesen Job freizuschalten.",
         "amt": [140, 150]},
        {"name": "Engineur", "req": 80, "desc": "\nVerdiene zwischen 140 und 150 Münzen pro Stunde.\nDu musst mindestens **80** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [150, 160]},
        {"name": "Streamer", "req": 90, "desc": "\nVerdiene zwischen 160 und 170 Münzen pro Stunde.\nDu musst mindestens **90** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [160, 170]},
        {"name": "Atlet", "req": 100, "desc": "\nVerdiene zwischen 170 und 180 Münzen pro Stunde.\nDu musst mindestens **100** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [170, 180]},
        {"name": "Polizist", "req": 120, "desc": "\nVerdiene zwischen 180 und 190 Münzen pro Stunde.\nDu musst mindestens **120** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [180, 190]},
        {"name": "Programmierer", "req": 140, "desc": "\nVerdiene zwischen 190 und 200 Münzen pro Stunde.\nDu musst mindestens **140** Stunden gearbeitet haben, um diesen Job freizuschalten.",
         "amt": [190, 200]},
        {"name": "Chirurg", "req": 160, "desc": "\nVerdiene zwischen 170 und 180 Münzen pro Stunde.\nDu musst mindestens **160** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [220, 240]},
        {"name": "Chefarzt", "req": 180, "desc": "\nVerdiene zwischen 240 und 250 Münzen pro Stunde.\nDu musst mindestens **180** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [240, 250]},
        {"name": "Anwalt", "req": 200, "desc": "\nVerdiene zwischen 250 und 260 Münzen pro Stunde.\nDu musst mindestens **200** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [250, 260]},
        {"name": "CEO", "req": 250, "desc": "\nVerdiene zwischen 260 und 270 Münzen pro Stunde.\nDu musst mindestens **250** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [260, 270]},
        {"name": "Richter", "req": 300, "desc": "\nVerdiene zwischen 270 und 280 Münzen pro Stunde.\nDu musst mindestens **300** Stunden gearbeitet haben, um diesen Job freizuschalten.", "amt": [270, 300]}]
##########
async def job_list(ctx, page):
    page = page - 1
    amt = 5
    index = page * amt
    joblist = ""
    for job in jobs[index: index + 5]:
        if await has_job_req(ctx, jobs.index(job)):
            emoji = '🔓'
        else:
            emoji = '🔒'
        joblist = joblist + f'**{emoji} {job["name"]}** {job["desc"]}\n'
    return joblist

async def has_job_req(ctx, job):
    acc = await open_acc(ctx.author)

    if int(acc[3]) >= jobs[job]["req"]:
        return True
    else:
        return False

async def open_acc(user):
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute(f"SELECT rucksack, bank, job, stunden FROM economy WHERE userID = {user.id}")
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO economy(rucksack, bank, job, stunden, userID) VALUES(%s, %s, %s, %s, %s)",("0", "0", "Kein Job", "0", user.id))
        mydb.commit()
        mydb.close()
        liste = ["0","0","Kein Job","0",user.id]
        return liste
    else:
        mydb.close()
        return result

async def update_acc(user, mode, sum, dif):
    acc = await open_acc(user)
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    if mode == "rucksack":
        bal = acc[0]
        new = int(bal) + int(sum) - int(dif)
        cursor.execute("UPDATE economy SET rucksack = (%s) WHERE userID = (%s)", (new, user.id))
    if mode == "bank":
        bal = acc[1]
        new = int(bal) + int(sum) - int(dif)
        cursor.execute("UPDATE economy SET bank = (%s) WHERE userID = (%s)", (new, user.id))

    mydb.commit()
    mydb.close()

async def get_job(user):
    acc = await open_acc(user)
    job = acc[2]
    return job

async def set_job(user, job):
    await open_acc(user)
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute("UPDATE economy SET job = (%s) WHERE userID = (%s)", (job, user.id))
    mydb.commit()
    mydb.close()

async def quit_job(user, job):
    await open_acc(user)
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute("UPDATE economy SET job = (%s) WHERE userID = (%s)", ("Kein Job", user.id))
    mydb.commit()
    mydb.close()

async def work(user):
    await open_acc(user)
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute(f"SELECT stunden FROM economy WHERE userID = {user.id}")
    result = cursor.fetchone()
    cursor.execute("UPDATE economy SET stunden = (%s) WHERE userID = (%s)", (int(result[0]) + 1, user.id))
    mydb.commit()
    mydb.close()


#SHOP
#cursor.execute("CREATE TABLE IF NOT EXISTS economy_shop(guildID TEXT, titel TEXT, beschreibung TEXT, preis TEXT)")
async def addshopitem(guild, titel, beschreibung, preis):
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute("INSERT INTO economy_shop(guildID, titel, beschreibung, preis) VALUES(%s, %s, %s, %s)", (guild.id, titel, beschreibung, preis))
    mydb.commit()
    mydb.close()

async def getshopitem(guild, titel):
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT titel, beschreibung, preis FROM economy_shop WHERE guildID = (%s) AND titel = (%s)", (guild.id, titel))
    result = cursor.fetchone()
    if result is None:
        mydb.close()
        return False
    if result is not None:
        mydb.close()
        return True

async def removeshopitem(guild, titel):
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute("DELETE FROM economy_shop WHERE guildID = (%s) AND titel = (%s)", (guild.id, titel))
    mydb.commit()
    mydb.close()

async def listshopitems(guild):
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute(f"SELECT * FROM economy_shop WHERE guildID = {guild.id}")
    result = cursor.fetchall()
    if result is None:
        mydb.close()
        return False
    else:
        mydb.close()
        return result
#ITEMS
#cursor.execute("CREATE TABLE IF NOT EXISTS economy_items(userID TEXT, titel TEXT, beschreibung TEXT, preis TEXT)")
async def buyitem(user, guild, titel):
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT titel, beschreibung, preis FROM economy_shop WHERE guildID = (%s) AND titel = (%s)", (guild.id, titel))
    item = cursor.fetchone()
    if item is None:
        return False
    if item is not None:
        cursor.execute("INSERT INTO economy_items(userID, titel, beschreibung, preis) VALUES(%s, %s, %s, %s)", (user.id, titel, item[1], item[2]))
    mydb.commit()
    mydb.close()

async def sellitem(user, titel):
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute("DELETE FROM economy_items WHERE userID = (%s) AND titel = (%s)", (user.id, titel))
    mydb.commit()
    mydb.close()

async def checkbalance(user, preis):
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute(f"SELECT rucksack FROM economy WHERE userID = {user.id}")
    result = cursor.fetchone()
    rucksack = int(result[0])
    if int(rucksack) >= int(preis):
        return True
    if int(rucksack) < int(preis):
        return False

    mydb.commit()
    mydb.close()

async def getuseritems(user):
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute(f"SELECT * FROM economy_items WHERE userID = {user.id}")
    result = cursor.fetchall()
    if result is None:
        mydb.close()
        return False
    else:
        mydb.close()
        return result

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['bal'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def balance(self, ctx, u: discord.User = None):
        """Öffnet einen Account."""
        if u is None:
            u = ctx.author
        acc = await open_acc(u)
        if acc is False:
            em = discord.Embed(title=f"{u.name}'s Konto", color=u.color)
            em.add_field(name='Job', value=f"Kein Job, :stopwatch: 0h")
            em.add_field(name="Brieftasche", value=f"0 🍪", inline=False)
            em.add_field(name='Bank', value=f"0 🍪", inline=False)
            em.add_field(name='Total', value=f"0 🍪")
            em.set_footer(text="Teste den work Command",
                        icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            em.set_footer(text="Interesse an Items? Guck dir mal den Command 'shop' an!")
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title=f"{u.name}'s Konto", color=discord.Color.orange())
            em.add_field(name='Job', value=f"{acc[2]}, :stopwatch: {acc[3]}h")
            em.add_field(name="Brieftasche", value=f"{acc[0]} 🍪", inline=False)
            em.add_field(name='Bank', value=f"{acc[1]} 🍪", inline=False)
            em.add_field(name='Total', value=f"{int(acc[0]) + int(acc[1])} 🍪")
            em.set_footer(text="Teste den work Command",
                        icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            em.set_footer(text="Interesse an Items? Guck dir mal den Command 'shop' an!")
            await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def beg(self, ctx):
        """Bettle für Münzen."""
        x = random.randint(0, 1000)

        if int(x) <= 400:
            earnings = random.randint(30, 50)
            em = discord.Embed(title=f"Bettel command", description=f"Ein alter Mann hat dir **{earnings}** 🍪 gegeben.", color=discord.Color.gold())
            em.set_footer(text="Du kannst mit dem Command work schneller Geld verdienen.",
                          icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await update_acc(ctx.author, "rucksack", earnings, 0)
            await ctx.send(embed=em)
            return
        if int(x) <= 900:
            earnings = random.randint(1, 30)
            em = discord.Embed(title=f"Bettel command",
                               description=f"Jemand gab dir **{earnings}** 🍪.",
                               color=discord.Color.gold())
            em.set_footer(text="Du kannst mit dem Command work schneller Geld verdienen.",
                          icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await update_acc(ctx.author, "rucksack", earnings, 0)
            await ctx.send(embed=em)
            return
        if int(x) <= 999:
            em = discord.Embed(title=f"Bettel command",
                               description=f"Du hast nichts bekommen",
                               color=discord.Color.red())
            em.set_footer(text="Du kannst mit dem Command work schneller Geld verdienen.",
                          icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=em)
            return
        if int(x) == 1000:
            earnings = random.randint(1000, 10000)
            em = discord.Embed(title=f"Bettel command",
                               description=f"Du hast so viel Glück!!!\nDie Chance, dies zu bekommen, ist 1 zu 1000\nDu hast {earnings} 🍪",
                               color=discord.Color.red())
            em.set_footer(text="Du kannst mit dem Command work schneller Geld verdienen.",
                          icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await update_acc(ctx.author, "rucksack", earnings, 0)
            await ctx.send(embed=em)
            return

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        """Gehe zur Arbeit mit deinem aktuellen Job."""
        if await get_job(ctx.author) != "Kein Job":
            beruf = await get_job(ctx.author)
            for job in jobs:
                if job["name"] == str(beruf):
                    earnings = int(random.randint(job["amt"][0], job["amt"][1]))
            await work(ctx.author)
            text = [f"Du hast als **{beruf}** gearbeitet und hast dafür **{earnings}** 🍪 bekommen!", f"Ein erfolgreicher Arbeitstag als **{beruf}** hat dir **{earnings}** 🍪 gebracht!"]
            endtext = random.choice(text)

            em = discord.Embed(title="Work command", description=f"{endtext}", color=discord.Color.gold())
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await update_acc(ctx.author, "bank", earnings, 0)
            await ctx.send(embed=em)
        else:
            error_embed = discord.Embed(description=f"Du musst dich zuerst für einen Job bewerben!\nNutze **{ctx.prefix}job apply <job>** um dich für eine Job zu bewerben.", color=discord.Colour.red())
            await ctx.send(embed=error_embed)
            ctx.command.reset_cooldown(ctx)

    @commands.command(aliases=['wd', "with"], usage="<anzahl>")
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def withdraw(self, ctx, amount=None):
        """Hebe Geld von deiner Bank ab."""
        if amount == None:
            await get_syntax(ctx)
            ctx.command.reset_cooldown(ctx)
            return
        acc = await open_acc(ctx.author)
        bank = int(acc[1])
        if int(amount) > int(bank):
            embed = discord.Embed(colour=discord.Colour.red(),
                                    description=f"Du hast nicht so viel Geld auf deiner Bank.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return
        if int(amount) < 0:
            embed = discord.Embed(colour=discord.Colour.red(),
                                    description=f"Die Anzahl zum Abheben muss positiv sein.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return

        await update_acc(ctx.author, "bank", 0, amount)
        await update_acc(ctx.author, "rucksack", amount, 0)

        embed = discord.Embed(colour=discord.Colour.green(), title="Erfolgreich",
                                description=f"Du hast **{amount}** 🍪 von deiner Bank abgehoben.",
                                timestamp=datetime.utcnow())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=['dp', "dep"], usage="<anzahl/all>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    async def deposit(self, ctx, amount=None):
        """Überweise Geld auf deine Bank."""
        if amount == None:
            await get_syntax(ctx)
            ctx.command.reset_cooldown(ctx)
            return
        acc = await open_acc(ctx.author)
        bank = int(acc[0])
        if int(amount) > int(bank):
            embed = discord.Embed(colour=discord.Colour.red(),
                                    description=f"Du hast nicht so viel Geld in deinem Rucksack.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return
        if int(amount) < 0:
            embed = discord.Embed(colour=discord.Colour.red(),
                                    description=f"Die Anzahl zum Abheben muss positiv sein.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return

        await update_acc(ctx.author, "rucksack", 0, amount)
        await update_acc(ctx.author, "bank", amount, 0)

        embed = discord.Embed(colour=discord.Colour.green(), title="Erfolgreich",
                                description=f"Du hast **{amount}** 🍪 auf deine Bank überwiesen.",
                                timestamp=datetime.utcnow())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=['give'], usage="<member/ID> <anzahl/all>")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def send(self, ctx, user: discord.User, amount=None):
        """Sende Geld zu einem anderen User."""
        if amount == None:
            await get_syntax(ctx)
            ctx.command.reset_cooldown(ctx)
            return
        if user == None:
            await get_syntax(ctx)
            ctx.command.reset_cooldown(ctx)
            return
        if user == ctx.author:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description="Du kannst dir selber kein Geld senden.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return
        acc = await open_acc(ctx.author)
        rucksack1 = acc[0]
        amount = int(amount)
        if amount > int(rucksack1):
            embed = discord.Embed(colour=discord.Colour.red(),
                                    description=f"Du hast nicht so viel Geld in deinem Rucksack.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            await self.bot.get_command("send").reset_cooldown(ctx)
            return
        if amount < 0:
            embed = discord.Embed(colour=discord.Colour.red(),
                                    description=f"Die Anzahl muss eine positive Zahl sein.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            await self.bot.get_command("send").reset_cooldown(ctx)
            return

        await update_acc(ctx.author, "rucksack", 0, amount)
        await update_acc(user, "rucksack", amount, 0)
        embed = discord.Embed(colour=discord.Colour.green(), title="Erfolgreich",
                                description=f"Du hast {user} **{amount}** 🍪 gegeben.")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=['rb'], usage="<member/ID>")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.guild_only()
    async def rob(self, ctx, member: discord.User = None):
        """Raube einen User aus."""
        if member == None:
            await get_syntax(ctx)
            ctx.command.reset_cooldown(ctx)
            return

        if member == ctx.author:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f"Du kannst dich selber nicht ausrauben.")
            embed.set_footer(text="Versuche jemand anderen auszurauben.",
                             icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return

        if member is not None:
            acc = await open_acc(member)
            rucksack = int(acc[0])
            if rucksack < 50:
                embed = discord.Embed(colour=discord.Colour.red(),
                                      description=f"**{member.name}** hat nicht viel Geld. Versuche jemand anderen auszurauben.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            if rucksack > 50:
                x = random.randint(1, 100)
                if x < 25:
                    strafe = random.randint(50, rucksack)
                    embed = discord.Embed(colour=discord.Colour.red(), title="Guter Versuch!",
                                          description=f"Du wurdest beim Ausrauben von {member.name} erwischt! Du musst **{strafe}** 🍪 als Strafe zahlen.")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await update_acc(ctx.author, "rucksack", 0, strafe)
                    await ctx.send(embed=embed)
                    return

                if x > 25:
                    earnings = random.randint(50, rucksack)
                    embed = discord.Embed(colour=discord.Colour.green(), title="Glück gehabt!",
                                          description=f"Du hast {member.name} erfolgreich ausgeraubt und **{earnings}** 🍪 bekommen.")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await update_acc(ctx.author, "rucksack", earnings, 0)
                    await update_acc(member, "rucksack", 0, earnings)
                    await ctx.send(embed=embed)
                    return

    @commands.command(usage="<anzahl>", aliases=['slots'])
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def slot(self, ctx, amount=None):
        """Teste dein Glück."""
        # überprüfen ob er geld hat
        acc = await open_acc(ctx.author)
        bal = int(acc[0])

        if amount == None:
            await get_syntax(ctx)
            ctx.command.reset_cooldown(ctx)
            return
        # results
        choices = ["🍇", "🍋", "🍒", "🍓", "🍊"]
        e1 = random.choice(choices)
        e2 = random.choice(choices)
        e3 = random.choice(choices)

        # embed1
        embed1 = discord.Embed(colour=discord.Colour.blurple(),
                               description="🎰 Slots")
        embed1.add_field(name=f"Slots:",
                         value=f"[<a:spin:942112865391882361> <a:spin:942112865391882361> <a:spin:942112865391882361>]",
                         inline=False)
        embed1.add_field(name="💰 Bet", value=f"{amount} 🍪", inline=False)
        embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar)

        # embed2
        embed2 = discord.Embed(colour=discord.Colour.blurple(),
                               description="🎰 Slots")
        embed2.add_field(name=f"Slots", value=f"[{e1} <a:spin:942112865391882361> <a:spin:942112865391882361>]",
                         inline=False)
        embed2.add_field(name="💰 Bet", value=f"{amount} 🍪", inline=False)
        embed2.set_author(name=ctx.author, icon_url=ctx.author.avatar)

        # embed3
        embed3 = discord.Embed(colour=discord.Colour.blurple(),
                               description="🎰 Slots")
        embed3.add_field(name=f"Slots", value=f"[{e1} {e2} <a:spin:942112865391882361>]", inline=False)
        embed3.add_field(name="💰 Bet", value=f"{amount} 🍪", inline=False)
        embed3.set_author(name=ctx.author, icon_url=ctx.author.avatar)

        try:
            if int(amount) < 0:
                embed = discord.Embed(colour=discord.Colour.red(),
                                      description=f"Die Anzahl muss eine positive Zahl sein.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return

            if int(amount) > int(bal):
                embed = discord.Embed(colour=discord.Colour.red(),
                                      description=f"Du hast nicht so viel Geld in deinem Rucksack.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
        except:
            pass
        # ergebnisse überprüfen
        # embedchanges
        amount = int(amount)
        message = await ctx.send(embed=embed1)
        await asyncio.sleep(1.5)
        await message.edit(embed=embed2)
        await asyncio.sleep(1.5)
        await message.edit(embed=embed3)
        if e1 == e2 == e3:
            await asyncio.sleep(1.5)
            embed4 = discord.Embed(colour=discord.Colour.gold(),
                                    description="🎰 Slots")
            embed4.add_field(name=f"Slots", value=f"[{e1} {e2} {e3}]", inline=False)
            embed4.add_field(name="🏆 Gewinn", value=f"Du gewinnst {amount * 6} 🍪",
                                inline=False)
            embed4.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await update_acc(ctx.author, "rucksack", 3 * amount, 0)
            await message.edit(embed=embed4)
            return
        if e1 == e3 != e2:
            await asyncio.sleep(1.5)
            embed4 = discord.Embed(colour=discord.Colour.green(),
                                    description="🎰 Slots")
            embed4.add_field(name=f"Slots", value=f"[{e1} {e2} {e3}]", inline=False)
            embed4.add_field(name="💰 Unentschieden", value=f"Du behältst {amount} 🍪",
                                inline=False)
            embed4.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await message.edit(embed=embed4)
            return
        if e1 == e2 != e3:
            await asyncio.sleep(1.5)
            embed4 = discord.Embed(colour=discord.Colour.green(),
                                    description="🎰 Slots")
            embed4.add_field(name=f"Slots", value=f"[{e1} {e2} {e3}]", inline=False)
            embed4.add_field(name="💰 Unentschieden", value=f"Du behältst {amount} 🍪",
                                inline=False)
            embed4.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await message.edit(embed=embed4)
            return
        if e2 == e1 != e3:
            await asyncio.sleep(1.5)
            embed4 = discord.Embed(colour=discord.Colour.green(),
                                    description="🎰 Slots")
            embed4.add_field(name=f"Slots", value=f"[{e1} {e2} {e3}]", inline=False)
            embed4.add_field(name="💰 Unentschieden", value=f"Du behältst {amount} 🍪",
                                inline=False)
            embed4.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await message.edit(embed=embed4)
            return
        if e2 == e3 != e1:
            await asyncio.sleep(1.5)
            embed4 = discord.Embed(colour=discord.Colour.green(),
                                    description="🎰 Slots")
            embed4.add_field(name=f"Slots", value=f"[{e1} {e2} {e3}]", inline=False)
            embed4.add_field(name="💰 Unentschieden", value=f"Du behältst {amount} 🍪",
                                inline=False)
            embed4.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await message.edit(embed=embed4)
            return
        if e3 == e1 != e2:
            await asyncio.sleep(1.5)
            embed4 = discord.Embed(colour=discord.Colour.green(),
                                    description="🎰 Slots")
            embed4.add_field(name=f"Slots", value=f"[{e1} {e2} {e3}]", inline=False)
            embed4.add_field(name="💰 Unentschieden", value=f"Du behältst {amount} 🍪",
                                inline=False)
            embed4.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await message.edit(embed=embed4)
            return
        if e3 == e2 != e1:
            await asyncio.sleep(1.5)
            embed4 = discord.Embed(colour=discord.Colour.green(),
                                    description="🎰 Slots")
            embed4.add_field(name=f"Slots", value=f"[{e1} {e2} {e3}]", inline=False)
            embed4.add_field(name="💰 Unentschieden", value=f"Du behältst {amount} 🍪",
                                inline=False)
            embed4.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await message.edit(embed=embed4)
            return
        else:
            await asyncio.sleep(1.5)
            embed4 = discord.Embed(colour=discord.Colour.red(),
                                    description="🎰 Slots")
            embed4.add_field(name=f"Slots", value=f"[{e1} {e2} {e3}]", inline=False)
            embed4.add_field(name="💰 Verloren", value=f"Du verlierst {amount} 🍪",
                                inline=False)
            embed4.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await update_acc(ctx.author, "rucksack", 0, amount)
            await message.edit(embed=embed4)
            return

    @commands.command(usage="<amount>")
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.guild_only()
    async def rps(self, ctx, amount=None):
        """Game, Schere Stein Papier. Deine Reaktion ist deine Entscheidung."""
        # überprüfen ob er geld hat
        acc = await open_acc(ctx.author)
        bal = int(acc[0])

        if amount == None:
            await get_syntax(ctx)
            return
        else:
            try:
                int(amount)
            except:
                await get_syntax(ctx)
                return 
            if int(amount) < 0:
                embed = discord.Embed(colour=discord.Colour.red(),
                                      description=f"Die Anzahl muss eine positivie Zahl sein.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

            if int(amount) > bal:
                embed = discord.Embed(colour=discord.Colour.red(),
                                      description=f"Du hast nicht so viel Geld.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return
            else:
                amount = int(amount)
                embed = discord.Embed(
                    color=discord.Color.blue(),
                    description=f"✊ Schere, Stein oder Papier?\nWette: {amount} 🍪",
                    timestamp=datetime.utcnow()
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                msg = await ctx.send(embed=embed)

                emojis = ["✌️", "✊", "✋"]
                for emoji in emojis:
                    await msg.add_reaction(emoji)

                choice = random.choice(emojis)

                def check(reaction, user):
                    return str(reaction.emoji) in emojis and user == ctx.message.author

                def same(choice, reaction):
                    e = discord.Embed(
                        title="Unentschieden!",
                        description=f"Deine Entscheidung: {reaction}\nMeine Entscheidung: {choice}"
                    )
                    e.add_field(name="💰 Du behältst", value=f"Du behältst {amount} 🍪")
                    return e

                def win(choice, reaction):
                    e = discord.Embed(
                        color=discord.Color.gold(),
                        title="Gewinn! 🏆",
                        description=f"Deine Entscheidung: {reaction}\nMeine Entscheidung: {choice}"
                    )
                    e.add_field(name="💰 Gewinn",
                                value=f"Du gewinnst {amount * 2} 🍪")
                    return e

                def loose(choice, reaction):
                    e = discord.Embed(
                        color=discord.Color.red(),
                        title="Verloren",
                        description=f"Deine Entscheidung: {reaction}\nMeine Entscheidung: {choice}"
                    )
                    e.add_field(name="💰 Du verlierst Geld", value=f"Du verlierst {amount} 🍪")
                    return e

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=10)

                    if str(reaction.emoji) == choice:
                        x = same(choice, str(reaction.emoji))
                        await msg.clear_reactions()
                        await msg.edit(embed=x)

                    else:
                        if choice == "✌️":
                            if str(reaction.emoji) == "✋":
                                x = loose(choice, str(reaction.emoji))
                                await update_acc(ctx.author, "rucksack", 0, amount)
                                await msg.edit(embed=x)
                            if str(reaction.emoji) == "✊":
                                x = win(choice, str(reaction.emoji))
                                await update_acc(ctx.author, "rucksack", 2 * amount, 0)
                                await msg.edit(embed=x)

                        if choice == "✊":
                            if str(reaction.emoji) == "✌️":
                                x = loose(choice, str(reaction.emoji))
                                await update_acc(ctx.author, "rucksack", 0, amount)
                                await msg.edit(embed=x)
                            if str(reaction.emoji) == "✋":
                                x = win(choice, str(reaction.emoji))
                                await update_acc(ctx.author, "rucksack", 2 * amount, 0)
                                await msg.edit(embed=x)

                        if choice == "✋":
                            if str(reaction.emoji) == "✊":
                                x = loose(choice, str(reaction.emoji))
                                await update_acc(ctx.author, "rucksack", 0, amount)
                                await msg.edit(embed=x)
                            if str(reaction.emoji) == "✌️":
                                x = win(choice, str(reaction.emoji))
                                await update_acc(ctx.author, "rucksack", 2 * amount, 0)
                                await msg.edit(embed=x)

                        await msg.clear_reactions()


                except asyncio.TimeoutError:
                    try:
                        await msg.clear_reactions()
                        x = discord.Embed(
                            title="Alleine spielen ist dumm",
                            description=f"Du hast nichts ausgewählt.\nDu behältst {amount} 🍪"
                        )
                    except:
                        pass

    @commands.command(usage="<amount>", aliases=["cf"])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def coinflip(self, ctx, amount=None):
        """Wirf eine Münze."""
        if amount == None:
            await get_syntax(ctx)
            return
        else:
            acc = await open_acc(ctx.author)
            bal = int(acc[0])

            if int(amount) < 0:
                embed = discord.Embed(colour=discord.Colour.red(),
                                      description=f"Die Anzahl muss eine positivie Zahl sein.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

            if int(amount) > int(bal):
                embed = discord.Embed(colour=discord.Colour.red(),
                                      description=f"Du hast nicht so viel Geld.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return
            else:
                amount = int(amount)
                embed1 = discord.Embed(colour=discord.Colour.red(),
                                       description=f"Die Münze fliegt ...")
                embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                embed1.add_field(name="💰 Wette", value=f"{amount} 🍪", inline=False)

                choices = ["**Kopf**", "**Zahl**"]
                e1 = random.choice(choices)
                e2 = random.choice(choices)

                message = await ctx.send(embed=embed1)
                await asyncio.sleep(5)

                if e1 == e2:
                    embed2 = discord.Embed(colour=discord.Colour.gold(),
                                           description=f"Deine Entscheidung: {e1}\nMeine Entscheidung: {e2}")
                    embed2.add_field(name="🏆 Gewinn",
                                     value=f"Du gewinnst {amount} 🍪", inline=False)
                    embed2.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await update_acc(ctx.author, "rucksack", amount, 0)
                    await message.edit(embed=embed2)
                else:
                    embed3 = discord.Embed(colour=discord.Colour.red(),
                                           description=f"Deine Entscheidung: {e1}\nMeine Entscheidung: {e2}")
                    embed3.add_field(name="💰 Verloren",
                                     value=f"Du verlierst {amount} 🍪",
                                     inline=False)
                    embed3.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await update_acc(ctx.author, "rucksack", 0, amount)
                    await message.edit(embed=embed3)
                    
    @commands.command(aliases=["rich"], usage="")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def richest(self, ctx):
        """Bekomme eine Liste von den 10 reichsten Usern basierend vom Geld der Bank."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT bank, rucksack, userID FROM economy ORDER BY bank DESC, rucksack DESC")
        leaderboard = cursor.fetchall()
        embed = discord.Embed(title="Die reichsten User", color=discord.Color.green())
        for i, pos in enumerate(leaderboard, start=1):
            bank, rucksack, userID = pos
            total = bank + rucksack
            name = self.bot.get_user(int(userID))
            embed.add_field(name=f"{i}. {name}", value=f"Total: {total} 🍪", inline=False)
            if i >= 10:
                await ctx.send(embed=embed)
                break
        await asyncio.sleep(1.5)
        if not i >= 10:
            await ctx.send(embed=embed)
        mydb.close()

    @commands.group(usage="<apply <job>, quit, list>")
    @commands.guild_only()
    async def job(self, ctx):
        """Bekomme eine Liste von allen Job Commands."""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='Job Commands', description=f'**{ctx.prefix}job apply <job>** - Bewirb dich für einen Job.\n'
                                                            f'**{ctx.prefix}job quit** - Quitte deinen aktuellen Job.\n'
                                                            f'**{ctx.prefix}job list** - Zeigt dir alle Jobs.',
                                  colour=discord.Color.green())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

    @job.command(usage="<job>")
    @commands.guild_only()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def apply(self, ctx, *, arg=None):
        """Bewirb dich für einen Job."""
        acc = await open_acc(ctx.author)
        job = acc[2]
        user_hours = acc[3]
        a = 0
        if arg != None:
            if await get_job(ctx.author) == "Kein Job":
                for job in jobs:
                    a += 1
                    if job["name"] == arg:
                        if int(user_hours) >= job["req"]:
                            await set_job(ctx.author, arg)
                            success_embed = discord.Embed(description=f'Herzlichen Glückwunsch! Deine Bewerbung als **{arg}** wurde angenommen.',
                                                            colour=discord.Colour.green())
                            success_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                            await ctx.send(embed=success_embed)
                            return
                        else:
                            not_enough_hours_error_embed = discord.Embed(description=f'Um sich als {arg} zu bewerben, musst du mindestens **{job["req"]}** Stunden gearbeitet haben.',
                                                                            color=discord.Colour.red())
                            not_enough_hours_error_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                            await ctx.send(embed=not_enough_hours_error_embed)
                            ctx.command.reset_cooldown(ctx)
                            return
                await asyncio.sleep(2)
                if a >= 23:
                    not_a_job_error_embed = discord.Embed(description=f"Der Job **{arg}** existiert nicht!\n"
                                                                    f"Schau dir eine Liste von Jobs mit **{ctx.prefix}job list** an.",
                                                        colour=discord.Colour.red())
                    not_a_job_error_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await ctx.send(embed=not_a_job_error_embed)
                    ctx.command.reset_cooldown(ctx)
                    return
            else:
                active_job = await get_job(ctx.author)
                active_job_error_embed = discord.Embed(description=f'Du bist derzeit noch als **{active_job}** angestellt!\n'
                                                                   f'Beende deinen Job als **{active_job}** mit **{ctx.prefix}job quit**',
                                                       colour=discord.Colour.red())
                active_job_error_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=active_job_error_embed)
                ctx.command.reset_cooldown(ctx)
                return
        else:
            await get_syntax(ctx)
            ctx.command.reset_cooldown(ctx)
            return

    @job.command(usage="")
    @commands.guild_only()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def quit(self, ctx):
        """Beende deinen aktuellen Job."""
        job = await get_job(ctx.author)
        if job != "Kein Job":
            success_embed = discord.Embed(description=f'Du hast deinen Job als **{job}** gekündigt.',
                                          colour=discord.Colour.green())
            success_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await set_job(ctx.author, "Kein Job")
            await ctx.send(embed=success_embed)
            return
        else:
            error_embed = discord.Embed(description=f"Du hast keinen Job, also kannst du nicht kündigen.\nBewerbe dich für einen Job mit **{ctx.prefix}job apply <job>**", color=discord.Colour.red())
            error_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=error_embed)
            ctx.command.reset_cooldown(ctx)

    @job.command(usage="")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def list(self, ctx):
        """Erhalte eine Liste aller Jobs."""
        msg = await ctx.send(embed=discord.Embed(title=':dividers: Jobliste',
                                                 description=f"Hier siehst du alle verfügbaren Jobs.\nSie können sich mit **{ctx.prefix}job bewerben <job>**.\n\n" + await job_list(ctx, 1), colour=discord.Colour.green()).set_footer(text='Seite 1 von 5'))
        def check(reaction, user):
            return reaction.message.id == msg.id and user == ctx.author

        Seite = 1
        while True:
            await msg.add_reaction('◀')
            await msg.add_reaction('▶')
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=30, check=check)
                if reaction.emoji == '◀':
                    Seite -= 1
                    if Seite < 1:
                        Seite = 5
                    embed = discord.Embed(title=':dividers: Jobliste',
                                          description=f'Hier siehst du alle verfügbaren Jobs.\nDu kannst dich für einen Job bewerben mit **{ctx.prefix}job apply <job>**\n\n' + await job_list(
                                              ctx, Seite), colour=discord.Colour.green())
                    embed.set_footer(text='Seite ' + str(Seite) + ' von 5')
                    await msg.remove_reaction('◀', ctx.author)
                    await msg.edit(embed=embed)
                if reaction.emoji == '▶':
                    Seite += 1
                    if Seite > 5:
                        Seite = 1
                    embed = discord.Embed(title=':dividers: Jobliste',description=f'Hier siehst du alle verfügbaren Jobs.\nDu kannst dich für einen Job bewerben mit **{ctx.prefix}job bewerben <job>**\n\n' + await job_list(ctx, Seite), colour=discord.Colour.green())
                    embed.set_footer(text='Seite ' + str(Seite) + ' von 5')
                    await msg.remove_reaction('▶', ctx.author)
                    await msg.edit(embed=embed)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break

    @commands.group(usage="additem <item>, removeitem <item>, list")
    @commands.guild_only()
    async def shop(self, ctx):
        """Bekomme eine Liste von allen Shop Commands."""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='Shop Commands', description=f'**{ctx.prefix}shop additem <item>** - Füge ein Item dem Shop hinzu.\n'
                                                            f'**{ctx.prefix}shop removeitem <item>** - Entferne ein Item aus dem Shop.\n'
                                                            f'**{ctx.prefix}shop list** - Zeigt dir alle Items im Shop.',
                                  colour=discord.Color.green())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

    @shop.command(usage="<item> <preis> <beschreibung>", aliases=["aitem"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def additem(self, ctx, titel=None, preis: int=None, *, beschreibung=None):
        """Füge ein Item dem Shop hinzu."""
        if titel == None or preis == None or beschreibung == None:
            await get_syntax(ctx)
            return
        item = await getshopitem(ctx.guild, titel)
        if item is False:
            await addshopitem(ctx.guild, titel, beschreibung, preis)
            embed = discord.Embed(color=discord.Color.green(), title="Item hinzugefügt", description=f"Das Item {titel} wurde zum Shop dieses Servers hinzugefügt.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        if item is True:
            embed = discord.Embed(color=discord.Color.red(), title="Item bereits vorhanden", description=f"Das Item {titel} gibt es bereits im Shop dieses Servers. Bitte wähle einen anderen Namen für das Item.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        
    @additem.error
    async def additem_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(colour=discord.Colour.red(), title="❌ Falscher Syntax",
                                description=f"Dein Betrag muss eine Zahl sein.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return


    @shop.command(usage="<item>", aliases=["ritem"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def removeitem(self, ctx, titel=None):
        """Entferne ein Item aus dem Shop."""
        if titel == None:
            await get_syntax(ctx)
        item = await getshopitem(ctx.guild, titel)
        if item is True:
            await removeshopitem(ctx.guild, titel)
            embed = discord.Embed(color=discord.Color.green(), title="Item gelöscht", description=f"Das Item {titel} wurde aus dem Shop dieses Servers gelöscht.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        if item is False:
            embed = discord.Embed(color=discord.Color.red(), title="Item nicht vorhanden", description=f"Das Item {titel} gibt es nicht im Shop dieses Servers. Bitte gib den korrekten Namen für das Item an.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

    @shop.command()
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def show(self, ctx):
        """Zeigt dir alle Items im Shop."""
        items = await listshopitems(ctx.guild)
        if items == False:
            embed = discord.Embed(color=discord.Color.red(), title="Keine Items vorhanden", description=f"Es gibt keine Items in dem Shop dieses Servers.\nFüge Items hinzu mit dem Command `{ctx.prefix}shop additem <item>`")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        else:
            a = 0
            embed = discord.Embed(color=discord.Color.orange(), title="Alle Items dieses Servers", description=f"Dieser Server hat ein paar Items im Shop.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            for item in items:
                a += 1
                #guildID, titel, beschreibung, preis
                embed.add_field(name=item[1], value=f"{item[2]}\n**Preis:** {item[3]}")
            if a == 0:
                embed = discord.Embed(color=discord.Color.red(), title="Keine Items vorhanden", description=f"Es gibt keine Items in dem Shop dieses Servers.\nFüge Items hinzu mit dem Command `{ctx.prefix}shop additem <item>`")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return
            await ctx.send(embed=embed)

    @commands.command(usage="<item>")
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.guild_only()
    async def buyitem(self, ctx, item=None):
        """Kaufe ein Item aus dem Shop."""
        if item == None:
            await get_syntax(ctx)
        i = await getshopitem(ctx.guild, item)
        if i == False:
            embed = discord.Embed(color=discord.Color.red(), title="Item nicht vorhanden", description=f"Das Item {item} gibt es nicht im Shop dieses Servers. Bitte gib den korrekten Namen für das Item an.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        if i == True:
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            cursor = mydb.cursor(buffered=True)
            cursor.execute("SELECT preis FROM economy_shop WHERE guildID = (%s) AND titel = (%s)", (ctx.guild.id, item))
            result = cursor.fetchone()
            if result is None:
                embed = discord.Embed(color=discord.Color.red(), title="Item nicht vorhanden", description=f"Das Item {item} gibt es nicht im Shop dieses Servers. Bitte gib den korrekten Namen für das Item an.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return
            else:
                canbuy = await checkbalance(ctx.author, result[0])
                if canbuy == True:
                    await buyitem(ctx.author, ctx.guild, item)
                    await update_acc(ctx.author, "rucksack", 0, result[0])
                    embed = discord.Embed(color=discord.Color.green(), title="Item gekauft", description=f"Das Item {item} wurde von dir gekauft. Ich habe es für dich in deinen Rucksack getan!")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await ctx.send(embed=embed)
                    return
                if canbuy == False:
                    embed = discord.Embed(color=discord.Color.red(), title="Item nicht gekauft", description=f"Das Item {item} wurde von dir nicht gekauft. Du hast zu wenig Geld in deinem Rucksack!")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await ctx.send(embed=embed)
                    return
        mydb.close()

    @commands.command()
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.guild_only()
    async def myitems(self, ctx):
        """Zeigt alle deine gekauften Items vom Shop."""
        items = await getuseritems(ctx.author)
        if items == False:
            embed = discord.Embed(color=discord.Color.red(), title="Keine Items vorhanden", description=f"Es gibt keine Items in deinem Rucksack.\nKaufe Items mit dem Command `{ctx.prefix}buyitem <item>`")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        else:
            a = 0
            embed = discord.Embed(color=discord.Color.orange(), title="Alle Items in deinem Rucksack", description=f"In deinem Rucksack sind ein paar Items.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            for item in items:
                a += 1
                embed.add_field(name=item[1], value=f"{item[2]}\n**Hat gekostet:** {item[3]}")
            if a == 0:
                embed = discord.Embed(color=discord.Color.red(), title="Keine Items vorhanden", description=f"Es gibt keine Items in deinem Rucksack.\nKaufe Items mit dem Command `{ctx.prefix}buyitem <item>`")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return
            await ctx.send(embed=embed)
    
    @commands.command(usage="<item>")
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.guild_only()
    async def sellitem(self, ctx, item=None):
        """Verkaufe ein Item aus deinem Rucksack. Du bekommst zufällige Prozente des Kaufpreises wieder. Prozente im Bereich von 65% bis 115%"""
        if item == None:
            await get_syntax(ctx)
            return
        items = await getuseritems(ctx.author)
        if items == False:
            embed = discord.Embed(color=discord.Color.red(), title="Keine Items vorhanden", description=f"Es gibt keine Items in deinem Rucksack.\nKaufe Items mit dem Command `{ctx.prefix}buyitem <item>`")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        else:
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            cursor = mydb.cursor(buffered=True)
            cursor.execute("SELECT preis FROM economy_shop WHERE guildID = (%s) AND titel = (%s)", (ctx.guild.id, item))
            preis = cursor.fetchone()
            Prozente = random.uniform(0.65, 1.15)
            verkaufspreis = round(Prozente * int(preis[0]))
            await sellitem(ctx.author, item)
            await update_acc(ctx.author, "rucksack", verkaufspreis, 0)
            embed = discord.Embed(color=discord.Color.green(), title="Item verkauft", description=f"Das Item {item} wurde für {verkaufspreis} 🍪 verkauft. Du hast es nun nicht mehr im Rucksack.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(economy(bot))