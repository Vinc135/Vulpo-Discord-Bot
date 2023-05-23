import typing
import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime, timedelta
from discord import app_commands
from info import getcolour

class joblist(discord.ui.View):
    def __init__(self, interaction=None, bot=None, s=None):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.bot = bot
        self.s = s

    @discord.ui.button(label='Zurück', style=discord.ButtonStyle.red, custom_id="grth676zetwerf43e", emoji="⬅️")
    async def zurück(self, interaction: discord.Interaction, button: discord.ui.Button):
        page = int(str(interaction.message.embeds[0].footer.text)[6])
        new_page = page - 1
        if new_page <= 0:
            new_page = 11
        embed = discord.Embed(title=':dividers: Jobliste', description=f"Hier siehst du alle verfügbaren Jobs.\nDu kannst dich für einen Job bewerben mit `/job apply <job>`\n\n" + await job_list(self.s, interaction, new_page),
                            colour=await getcolour(self, interaction.user)).set_footer(text=f'Seite {new_page} von 11')
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        await interaction.response.edit_message(embed=embed, content="")
    
    @discord.ui.button(label='Weiter', style=discord.ButtonStyle.green, custom_id="fewgwrgwrtgtg", emoji="➡️")
    async def vor(self, interaction: discord.Interaction, button: discord.ui.Button):
        page = int(str(interaction.message.embeds[0].footer.text)[6])
        new_page = page + 1
        if new_page > 11:
            new_page = 1
        embed = discord.Embed(title=':dividers: Jobliste', description=f"Hier siehst du alle verfügbaren Jobs.\nDu kannst dich für einen Job bewerben mit `/job apply <job>`\n\n" + await job_list(self.s, interaction, new_page),
                            colour=await getcolour(self, interaction.user)).set_footer(text=f'Seite {new_page} von 11')
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        await interaction.response.edit_message(embed=embed, content="")

##########
jobs = [{"name": "Küchenhilfe", "req": 0, "amt": [20, 30]},
        {"name": "Kassierer", "req": 5, "amt": [30, 40]},
        {"name": "Dönermann", "req": 10, "amt": [40, 50]},
        {"name": "Elektroniker", "req": 15, "amt": [50, 60]},
        {"name": "Pfleger", "req": 20, "amt": [60, 70]},
        {"name": "Bäcker", "req": 25,  "amt": [70, 80]},
        {"name": "Bauarbeiter", "req": 30, "amt": [80, 90]},
        {"name": "Gärtner", "req": 35, "amt": [90, 100]},
        {"name": "Lehrer", "req": 40, "amt": [100, 120]},
        {"name": "Koch", "req": 45, "amt": [120, 140]},
        {"name": "Sanitäter", "req": 50, "amt": [140, 160]},
        {"name": "TV-Moderator", "req": 60, "amt": [160, 180]},
        {"name": "Schauspieler", "req": 70, "amt": [180, 200]},
        {"name": "Engineur", "req": 80, "amt": [200, 220]},
        {"name": "Streamer", "req": 90, "amt": [220, 240]},
        {"name": "Atlet", "req": 100, "amt": [240, 260]},
        {"name": "Polizist", "req": 120, "amt": [260, 280]},
        {"name": "Programmierer", "req": 140, "amt": [280, 300]},
        {"name": "Chirurg", "req": 160, "amt": [300, 320]},
        {"name": "Arzthelfer", "req": 180, "amt": [320, 340]},
        {"name": "Chefarzt", "req": 200, "amt": [340, 360]},
        {"name": "Anwalt", "req": 220, "amt": [360, 380]},
        {"name": "CEO", "req": 240, "amt": [380, 400]},
        {"name": "Richter", "req": 260, "amt": [400, 420]},
        {"name": "Marketing Manager", "req": 280, "amt": [420, 440]},
        {"name": "Analyst", "req": 300, "amt": [440, 460]},
        {"name": "Wirtschaftsingenieur", "req": 320, "amt": [460, 480]},
        {"name": "Mediaplaner", "req": 340, "amt": [480, 500]},
        {"name": "Pressesprecher", "req": 360, "amt": [500, 520]},
        {"name": "Qualitätsmanager", "req": 380, "amt": [520, 540]},
        {"name": "Informatiker", "req": 400, "amt": [540, 560]},
        {"name": "Fachinformatiker", "req": 420, "amt": [560, 580]},
        {"name": "Referent", "req": 440, "amt": [580, 600]},
        {"name": "Consultant", "req": 460, "amt": [600, 620]},
        {"name": "Bauleiter", "req": 480, "amt": [620, 640]},
        {"name": "Tiefbau-Ingenieur", "req": 500, "amt": [640, 660]},
        {"name": "Mediaplaner", "req": 550, "amt": [660, 680]},
        {"name": "App Developer", "req": 600, "amt": [680, 700]},
        {"name": "Volljurist", "req": 650, "amt": [700, 720]},
        {"name": "Harvard Professor", "req": 700, "amt": [720, 740]},
        {"name": "Pilot", "req": 750, "amt": [740, 760]},
        {"name": "Corporate Finance Manager", "req": 800, "amt": [760, 780]},
        {"name": "Trader", "req": 850, "amt": [780, 800]},
        {"name": "Marktkettenführer", "req": 900, "amt": [800, 820]},
        {"name": "Lufthansa Chef", "req": 950, "amt": [820, 840]},
        {"name": "Wirtschaftsprüfer", "req": 1000, "amt": [840, 860]},
        {"name": "Fußballer", "req": 1050, "amt": [860, 880]},
        {"name": "Fußball Trainer", "req": 1100, "amt": [880, 900]},
        {"name": "Nasa", "req": 1150, "amt": [900, 920]},
        {"name": "Präsident", "req": 1200, "amt": [920, 940]},
        {"name": "Chef Anwaltskanzlei", "req": 1250, "amt": [940, 960]},
        {"name": "Medical Advisor", "req": 1300, "amt": [960, 980]},
        {"name": "Astronaut", "req": 1350, "amt": [980, 1000]}]

##########

async def job_autocomplete(interaction: discord.Interaction, current: str,) -> typing.List[app_commands.Choice[str]]:
    try:
        matching_jobs = [
            app_commands.Choice(name=job["name"], value=job["name"])
            for job in jobs if current.lower() in job["name"].lower()
        ]
        return matching_jobs[:25]
    except:
        pass
        
def same(userchoice, botchoice, betrag):
    e = discord.Embed(
        title="Unentschieden!",
        description=f"Deine Entscheidung: {userchoice}\nMeine Entscheidung: {botchoice}"
    )
    e.add_field(name="💰 Nichts", value=f"Du behältst {betrag} 🍪")
    e.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
    return e

def win(userchoice, botchoice, betrag):
    e = discord.Embed(
        color=discord.Color.gold(),
        title="Gewinn! 🏆",
        description=f"Deine Entscheidung: {userchoice}\nMeine Entscheidung: {botchoice}"
    )
    e.add_field(name="💰 Gewinn", value=f"Du gewinnst {betrag * 2} 🍪")
    e.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
    return e

def loose(userchoice, botchoice, betrag):
    e = discord.Embed(
        color=discord.Color.red(),
        title="Verloren",
        description=f"Deine Entscheidung: {userchoice}\nMeine Entscheidung: {botchoice}"
    )
    e.add_field(name="💰 Verlust", value=f"Du verlierst {betrag} 🍪")
    e.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
    return e
        
class rps(discord.ui.View):
    def __init__(self, botchoice=None, betrag=None, user=None, bot=None, interaction=None):
        super().__init__(timeout=None)
        self.botchoice = botchoice
        self.betrag = betrag
        self.user = user
        self.bot = bot
        self.interaction = interaction

    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="ljhgdfiugegrfwiuegrfiu", emoji="✌️")
    async def schere(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"""
        Userchoice: ✌️
        Botchoice: {self.botchoice}""")
        await interaction.response.defer(thinking=False, ephemeral=True)
        botchoice = self.botchoice
        userchoice = button.emoji
        betrag = self.betrag
        interaction = self.interaction
        if interaction.user.id != self.user.id:
            return await interaction.response.defer(thinking=False, ephemeral=True)
        if str(userchoice) == str(botchoice):
            x = same(userchoice, botchoice, self.betrag)
            return await interaction.edit_original_response(embed=x, view=None)
        if str(botchoice) == "✌️":
            if str(userchoice) == "✋":
                x = loose(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 0, betrag)
                await interaction.edit_original_response(embed=x, view=None)
            if str(userchoice) == "✊":
                x = win(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 2 * betrag, 0)
                await interaction.edit_original_response(embed=x, view=None)

        if str(botchoice) == "✊":
            if str(userchoice) == "✌️":
                x = loose(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 0, betrag)
                await interaction.edit_original_response(embed=x, view=None)
            if str(userchoice) == "✋":
                x = win(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 2 * betrag, 0)
                await interaction.edit_original_response(embed=x, view=None)

        if str(botchoice) == "✋":
            if str(userchoice) == "✊":
                x = loose(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 0, betrag)
                await interaction.edit_original_response(embed=x, view=None)
            if str(userchoice) == "✌️":
                x = win(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 2 * betrag, 0)
                await interaction.edit_original_response(embed=x, view=None)

    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="flwehrbfvwejrhgfvweurhfk", emoji="✊")
    async def stein(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"""
        Userchoice: ✊
        Botchoice: {self.botchoice}""")
        await interaction.response.defer(thinking=False, ephemeral=True)
        botchoice = self.botchoice
        userchoice = button.emoji
        betrag = self.betrag
        interaction = self.interaction
        if interaction.user.id != self.user.id:
            return await interaction.response.defer(thinking=False, ephemeral=True)
        if str(userchoice) == str(botchoice):
            x = same(userchoice, botchoice, self.betrag)
            return await interaction.edit_original_response(embed=x, view=None)
        if botchoice == "✌️":
            if userchoice == "✋":
                x = loose(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 0, betrag)
                await interaction.edit_original_response(embed=x, view=None)
            if userchoice== "✊":
                x = win(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 2 * betrag, 0)
                await interaction.edit_original_response(embed=x, view=None)

        if botchoice == "✊":
            if userchoice == "✌️":
                x = loose(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 0, betrag)
                await interaction.edit_original_response(embed=x, view=None)
            if userchoice == "✋":
                x = win(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 2 * betrag, 0)
                await interaction.edit_original_response(embed=x, view=None)

        if botchoice == "✋":
            if userchoice == "✊":
                x = loose(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 0, betrag)
                await interaction.edit_original_response(embed=x, view=None)
            if userchoice == "✌️":
                x = win(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 2 * betrag, 0)
                await interaction.edit_original_response(embed=x, view=None)

    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="ebwkfuzgqewriufgiwuezrgfiu", emoji="✋")
    async def papier(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"""
        Userchoice: ✋
        Botchoice: {self.botchoice}""")
        await interaction.response.defer(thinking=False, ephemeral=True)
        botchoice = self.botchoice
        userchoice = button.emoji
        betrag = self.betrag
        interaction = self.interaction
        if interaction.user.id != self.user.id:
            return await interaction.response.defer(thinking=False, ephemeral=True)
        if str(userchoice) == str(botchoice):
            x = same(userchoice, botchoice, self.betrag)
            return await interaction.edit_original_response(embed=x, view=None)
        if botchoice == "✌️":
            if userchoice == "✋":
                x = loose(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 0, betrag)
                await interaction.edit_original_response(embed=x, view=None)
            if userchoice== "✊":
                x = win(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 2 * betrag, 0)
                await interaction.edit_original_response(embed=x, view=None)

        if botchoice == "✊":
            if userchoice == "✌️":
                x = loose(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 0, betrag)
                await interaction.edit_original_response(embed=x, view=None)
            if userchoice == "✋":
                x = win(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 2 * betrag, 0)
                await interaction.edit_original_response(embed=x, view=None)

        if botchoice == "✋":
            if userchoice == "✊":
                x = loose(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 0, betrag)
                await interaction.edit_original_response(embed=x, view=None)
            if userchoice == "✌️":
                x = win(userchoice, botchoice, betrag)
                await update_account(self, interaction.user, "rucksack", 2 * betrag, 0)
                await interaction.edit_original_response(embed=x, view=None)

#####
async def job_list(self, interaction, page):
    page = page - 1
    amt = 5
    index = page * amt
    joblist = ""
    for job in jobs[index: index + 7]:
        if await has_job_req(self, interaction, jobs.index(job)):
            emoji = '🔓'
        else:
            emoji = '🔒'
        joblist = joblist + f'**{emoji} {job["name"]}** Verdiene zwischen {job["amt"][0]} und {job["amt"][1]} pro Arbeitsstunde.\nDu brauchst {job["req"]} Arbeitsstunden.\n'
    return joblist

async def has_job_req(self, interaction, job):
    acc = await open_acc(self, interaction.user)
    if int(acc[3]) >= jobs[job]["req"]:
        return True
    else:
        return False

async def open_acc(self, user):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT rucksack, bank, job, stunden FROM economy WHERE userID = (%s)", (user.id))
            result = await cursor.fetchone()
            if result is None:
                await cursor.execute("INSERT INTO economy(rucksack, bank, job, stunden, userID) VALUES(%s, %s, %s, %s, %s)",("0", "0", "Kein Job", "0", user.id))
                
                liste = ["0","0","Kein Job","0",user.id]
                return liste
            else:
                return result

async def update_account(self, user, mode, sum, dif):
    acc = await open_acc(self, user)
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            print(user)
            print(user.id)
            if mode == "rucksack":
                bal = acc[0]
                new = int(bal) + int(sum) - int(dif)
                print(new)
                await cursor.execute(f"UPDATE economy SET rucksack = {new} WHERE userID = {user.id}")
                
            if mode == "bank":
                bal = acc[1]
                new = int(bal) + int(sum) - int(dif)
                await cursor.execute(f"UPDATE economy SET bank = {new} WHERE userID = {user.id}")
            

async def get_job(self, user):
    acc = await open_acc(self, user)
    job = acc[2]
    return job

async def set_job(self, user, job):
    await open_acc(self, user)
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE economy SET job = (%s) WHERE userID = (%s)", (job, user.id))
        

async def work(self, user):
    await open_acc(self, user)
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT stunden FROM economy WHERE userID = (%s)", (user.id))
            result = await cursor.fetchone()
            await cursor.execute("UPDATE economy SET stunden = (%s) WHERE userID = (%s)", (int(result[0]) + 1, user.id))

#SHOP
async def addshopitem(self, guild, titel, beschreibung, preis, rolle):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            if rolle:
                return await cursor.execute("INSERT INTO economy_shop(guildID, titel, beschreibung, preis, roleID) VALUES(%s, %s, %s, %s, %s)", (guild.id, titel, beschreibung, preis, rolle.id))
            await cursor.execute("INSERT INTO economy_shop(guildID, titel, beschreibung, preis) VALUES(%s, %s, %s, %s)", (guild.id, titel, beschreibung, preis))


async def getshopitem(self, guild, titel):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT titel, beschreibung, preis, roleID FROM economy_shop WHERE guildID = (%s) AND titel = (%s)", (guild.id, titel))
            result = await cursor.fetchone()
            if result is None:
                return False
            if result is not None:
                return True

async def removeshopitem(self, guild, titel):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM economy_shop WHERE guildID = (%s) AND titel = (%s)", (guild.id, titel))

async def listshopitems(self, guild):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM economy_shop WHERE guildID = (%s)", (guild.id))
            result = await cursor.fetchall()
            if result == ():
                return False
            else:
                return result
            
#ITEMS
async def buyitem(self, user, guild, titel):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT titel, beschreibung, preis, roleID FROM economy_shop WHERE guildID = (%s) AND titel = (%s)", (guild.id, titel))
            item = await cursor.fetchone()
            if item is None:
                return False
            if item is not None:
                if item[3] == None:
                    await cursor.execute("INSERT INTO economy_items(userID, titel, beschreibung, preis, guildID) VALUES(%s, %s, %s, %s, %s)", (user.id, titel, item[1], item[2], guild.id))
                else:
                    rolle = guild.get_role(int(item[3]))
                    await user.add_roles(rolle)
                    await cursor.execute("INSERT INTO economy_items(userID, titel, beschreibung, preis, guildID, roleID) VALUES(%s, %s, %s, %s, %s, %s)", (user.id, titel, item[1], item[2], guild.id, item[3]))

async def sellitem(self, user, titel):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT titel, beschreibung, preis, roleID FROM economy_shop WHERE guildID = (%s) AND titel = (%s)", (user.guild.id, titel))
            item = await cursor.fetchone()
            if item is None:
                return False
            if item is not None:
                if item[3] == None:
                    await cursor.execute("DELETE FROM economy_items WHERE userID = (%s) AND titel = (%s) AND guildID = (%s)", (user.id, titel, user.guild.id))
                else:
                    rolle = user.guild.get_role(int(item[3]))
                    await user.remove_roles(rolle)
                    await cursor.execute("DELETE FROM economy_items WHERE userID = (%s) AND titel = (%s) AND guildID = (%s)", (user.id, titel, user.guild.id))

async def checkbalance(self, user, preis):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT rucksack FROM economy WHERE userID = (%s)", (user.id))
            result = await cursor.fetchone()
            rucksack = int(result[0])
            if int(rucksack) >= int(preis):
                return True
            if int(rucksack) < int(preis):
                return False

async def getuseritems(self, user):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM economy_items WHERE userID = (%s) AND guildID = (%s)", (user.id, user.guild.id))
            result = await cursor.fetchall()
            if result == ():
                return False
            else:        
                return result 

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    cookies = app_commands.Group(name='cookies', description='Befehle vom Economy System für das Verwalten seines Accounts.', guild_only=True)
        
    @cookies.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def anzeigen(self, interaction: discord.Interaction):
        """Verwalte dein Geld."""            
        acc = await open_acc(self, interaction.user)
        em = discord.Embed(title=f"Dein supertolles Konto", color=await getcolour(self, interaction.user), description="> Dein Rucksack hat viel Platz. Dort findest du deine Items und deine Cookies.")
        em.add_field(name="Rucksack", value=f"{acc[0]} 🍪")
        em.add_field(name="Bank", value=f"{acc[1]} 🍪")
        em.add_field(name='Beruf', value=f"{acc[2]}, :stopwatch: {acc[3]} Stunden")
        items = await getuseritems(self, interaction.user)
        if items != False:
            string = ""
            wert = 0
            for item in items:
                wert += int(item[3])
                if string == "":
                    string += f"{item[1]}({item[3]}🍪)"
                else:
                    string += f", {item[1]}({item[3]}🍪)"
            string += f"\n\n**Items Wert: {wert}.** Mit Glück bekommst du mehr Geld beim Verkauf als du ausgegeben hast."
            em.add_field(name="Items", value=string)
        
        em.set_thumbnail(url=interaction.user.avatar)
        em.set_footer(text="Interesse an einem täglich steigenden Cookie Bonus? Befehl: /daily", icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
        await interaction.response.send_message(embed=em)

    @cookies.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def abheben(self, interaction: discord.Interaction, betrag: int):
        """Bekomme Geld von der Bank."""
        acc = await open_acc(self, interaction.user)
        rucksack = int(acc[0])
        bank = int(acc[1])
        if betrag > int(bank):
            await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> Du hast nicht **{betrag} 🍪** auf deiner Bank. Es fehlen dir **{betrag - bank} 🍪**.", ephemeral=True)
            return
        if betrag < 0:
            await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> Der Betrag muss eine positive Zahl sein. Beispiel: `/balance withdraw {bank}`", ephemeral=True)
            return

        await update_account(self, interaction.user, "bank", 0, betrag)
        await update_account(self, interaction.user, "rucksack", betrag, 0)

        await interaction.response.send_message(f"<:v_haken:1048677657040134195> Ich habe **{betrag} 🍪** von deiner Bank abgehoben. Du hast nun **{rucksack + betrag} 🍪** in deinem Rucksack und **{bank - betrag} 🍪** auf deiner Bank.")
    
    @cookies.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def einzahlen(self, interaction: discord.Interaction, betrag: int):
        """Überweise Geld auf deine Bank."""
        acc = await open_acc(self, interaction.user)
        rucksack = int(acc[0])
        bank = int(acc[1])
        if betrag > int(rucksack):
            await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> Du hast nicht **{betrag} 🍪** auf deiner Bank. Es fehlen dir **{betrag - rucksack} 🍪**.", ephemeral=True)
            return
        if betrag < 0:
            await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> Der Betrag muss eine positive Zahl sein. Beispiel: `/balance withdraw {rucksack}`", ephemeral=True)
            return

        await update_account(self, interaction.user, "rucksack", 0, betrag)
        await update_account(self, interaction.user, "bank", betrag, 0)

        await interaction.response.send_message(f"<:v_haken:1048677657040134195> Ich habe **{betrag} 🍪** auf deine Bank überwiesen. Du hast nun **{rucksack - betrag} 🍪** in deinem Rucksack und **{bank + betrag} 🍪** auf deiner Bank.")

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    async def beg(self, interaction: discord.Interaction):
        """Bettle für Münzen."""
        x = random.randint(0, 1000)
        if int(x) <= 400:
            earnings = random.randint(30, 50)
            em = discord.Embed(title=f"Bettel command", description=f"Ein alter Mann hat dir **{earnings}** 🍪 gegeben.", color=await getcolour(self, interaction.user))
            em.set_footer(text="Du kannst mit dem Command work schneller Geld verdienen.",
                          icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            em.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            await update_account(self, interaction.user, "rucksack", earnings, 0)
            await interaction.response.send_message(embed=em)
            return
        if int(x) <= 900:
            earnings = random.randint(1, 30)
            em = discord.Embed(title=f"Bettel command",
                               description=f"Jemand gab dir **{earnings}** 🍪.",
                               color=await getcolour(self, interaction.user))
            em.set_footer(text="Du kannst mit dem Command work schneller Geld verdienen.",
                          icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            em.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            await update_account(self, interaction.user, "rucksack", earnings, 0)
            await interaction.response.send_message(embed=em)
            return
        if int(x) <= 999:
            em = discord.Embed(title=f"Bettel command",
                               description=f"Du hast nichts bekommen",
                               color=await getcolour(self, interaction.user))
            em.set_footer(text="Du kannst mit dem Command work schneller Geld verdienen.",
                          icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            em.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed=em)
            return
        if int(x) == 1000:
            earnings = random.randint(1000, 10000)
            em = discord.Embed(title=f"Bettel command",
                               description=f"Du hast so viel Glück!!!\nDie Chance, dies zu bekommen, ist 1 zu 1000\nDu hast {earnings} 🍪 erhalten.",
                               color=await getcolour(self, interaction.user))
            em.set_footer(text="Du kannst mit dem Command work schneller Geld verdienen.",
                          icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            em.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            await update_account(self, interaction.user, "rucksack", earnings, 0)
            await interaction.response.send_message(embed=em)
            return

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 86400 , key=lambda i: (i.user.id))
    async def daily(self, interaction: discord.Interaction):
        """Sammle deinen täglichen Cookie-Bonus ein."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT streak, timestamp FROM economy_streak WHERE userID = (%s)", (interaction.user.id))
                result = await cursor.fetchone()
                now = datetime.now()
                if result is not None:
                    streak = result[0]
                    last_claim_stamp = result[1]
                    last_claim = datetime.fromtimestamp(float(last_claim_stamp))
                    delta = now - last_claim
                    if delta > timedelta(hours=48):
                        await cursor.execute("UPDATE economy_streak SET streak = (%s) WHERE userID = (%s)", (1, interaction.user.id))
                        await cursor.execute("UPDATE economy_streak SET timestamp = (%s) WHERE userID = (%s)", (str(now.timestamp()), interaction.user.id))
                        earnings = 50
                        await update_account(self, interaction.user, "rucksack", earnings, 0)
                        embed = discord.Embed(title="Täglicher Bonus", description=f"Du hast deinen täglichen Bonus eingefordert und dafür **{earnings} 🍪** bekommen. Leider warst du zu spät und dein Daily Streak von **{streak}🔥** wurde auf **1** zurückgesetzt.", color=await getcolour(self, interaction.user))
                        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                        await interaction.response.send_message(embed=embed)
                        return
                    else:
                        await cursor.execute("UPDATE economy_streak SET streak = (%s) WHERE userID = (%s)", (int(streak) + 1, interaction.user.id))
                        await cursor.execute("UPDATE economy_streak SET timestamp = (%s) WHERE userID = (%s)", (str(now.timestamp()), interaction.user.id))
                        earnings = 50 + ((streak + 1) * 5)
                        await update_account(self, interaction.user, "rucksack", earnings, 0)
                        embed = discord.Embed(title="Täglicher Bonus", description=f"Du hast deinen täglichen Bonus eingefordert und dafür **{earnings} 🍪** bekommen. Du kamst rechtzeitig und hast deinen Streak erhöht.", color=await getcolour(self, interaction.user))
                        embed.set_footer(text=f"Er liegt nun bei {streak + 1}🔥", icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                        await interaction.response.send_message(embed=embed)
                        return
                if result is None:
                    await cursor.execute("INSERT INTO economy_streak(streak, timestamp, userID) VALUES(%s,%s,%s)", (1, str(now.timestamp()), interaction.user.id))
                    earnings = 50
                    await update_account(self, interaction.user, "rucksack", earnings, 0)
                    embed = discord.Embed(title="Täglicher Bonus", description=f"Du hast deinen täglichen Bonus eingefordert und dafür **{earnings} 🍪** bekommen. Oh, du bist neu 🔎! Wenn du innerhalb von 48 Stunden diesen Befehl erneut ausführst, bekommst du immer mehr Cookies.", color=await getcolour(self, interaction.user))
                    embed.set_footer(text=f"Er liegt nun bei 1🔥", icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                    await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    async def work(self, interaction: discord.Interaction):
        """Gehe zur Arbeit mit deinem aktuellen Job."""
        try:
            if await get_job(self, interaction.user) != "Kein Job":
                beruf = await get_job(self, interaction.user)
                for job in jobs:
                    if job["name"] == str(beruf):
                        earnings = int(random.randint(job["amt"][0], job["amt"][1]))
                        await work(self, interaction.user)
                        text = [f"Du hast als **{beruf}** gearbeitet und hast dafür **{earnings} 🍪** bekommen!", f"Eine erfolgreiche Arbeitsstunde als **{beruf}** hat dir **{earnings} 🍪** gebracht!", f"Nach einer harten Arbeitsstunde als **{beruf}** hat dich dein Chef mit **{earnings} 🍪** bezahlt!"]
                        endtext = random.choice(text)
                        await update_account(self, interaction.user, "bank", earnings, 0)
                        embed = discord.Embed(title="Du hast gearbeitet", description=endtext, color=await getcolour(self, interaction.user))
                        acc = await open_acc(self, interaction.user)
                        embed.set_footer(text=f"Deine Arbeitsstunden: {acc[3]}", icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                        await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> Du musst dich zuerst für einen Job bewerben!\nAlle Jobs siehst du mit dem Befehl `/job list`\nNutze `/job apply <job>` um dich für einen Job zu bewerben.", ephemeral=True)
        except:
            pass
        
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def send(self, interaction: discord.Interaction, user: discord.User, betrag: int):
        """Sende Geld zu einem anderen User."""
        if user == interaction.user:
            await interaction.response.send_message("<:v_kreuz:1049388811353858069> Du kannst dir kein Geld selber senden.", ephemeral=True)
            return
        acc = await open_acc(self, interaction.user)
        rucksack = int(acc[0])
        if betrag > int(rucksack):
            await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> Du hast nicht so viel Geld in deinem Rucksack. Dir fehlen **{betrag - rucksack} 🍪**.", ephemeral=True)
            return
        if betrag < 0:
            await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> Der Betrag muss eine positive Zahl sein. Beispiel: `/send @Vinc {betrag}`", ephemeral=True)
            return

        await update_account(self, interaction.user, "rucksack", 0, betrag)
        await update_account(self, user, "rucksack", betrag, 0)
        await interaction.response.send_message(f"<:v_haken:1048677657040134195> {user.mention} hat **{betrag} 🍪** von dir erhalten. Du hast nun **{rucksack - betrag} 🍪** in deinem Rucksack.")

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3500, key=lambda i: (i.user.id))
    async def rob(self, interaction: discord.Interaction, user: discord.User):
        """Raube einen User aus."""
        if user == interaction.user:
            await interaction.response.send_message("<:v_kreuz:1049388811353858069> Du kannst dir kein Geld selber senden.", ephemeral=True)
            return
        acc = await open_acc(self, user)
        rucksack = int(acc[0])
        if rucksack < 50:
            await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> {user} hat nicht viel Geld. Versuche jemand anderen auszurauben.", ephemeral=True)
            return
        if rucksack > 50:
            x = random.randint(1, 100)
            if x < 25:
                strafe = random.randint(50, rucksack)
                embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Guter Versuch!",
                                        description=f"Du wurdest beim Ausrauben von {user} erwischt! Du musst **{strafe} 🍪** als Strafe zahlen.")
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                await update_account(self, interaction.user, "rucksack", 0, strafe)
                await interaction.response.send_message(embed=embed)
                return

            if x > 25:
                earnings = random.randint(50, rucksack)
                embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Glück gehabt!",
                                        description=f"Du hast {user} erfolgreich ausgeraubt und **{earnings} 🍪** bekommen.")
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                await update_account(self, interaction.user, "rucksack", earnings, 0)
                await update_account(self, user, "rucksack", 0, earnings)
                await interaction.response.send_message(embed=embed)
                return

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def slot(self, interaction: discord.Interaction, betrag: int):
        """Teste dein Glück."""
        # überprüfen ob er geld hat
        acc = await open_acc(self, interaction.user)
        rucksack = int(acc[0])

        if betrag < 0:
            await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> Der Betrag muss eine positive Zahl sein. Beispiel: `/send @Vinc {betrag}`", ephemeral=True)
            return
        if betrag > rucksack:
            await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> Du hast nicht so viel Geld in deinem Rucksack. Dir fehlen **{betrag - rucksack} 🍪**.", ephemeral=True)
            return
        # results
        choices = ["🍇", "🍋", "🍒", "🍓", "🍊"]
        e1 = random.choice(choices)
        e2 = random.choice(choices)
        e3 = random.choice(choices)

        # embed1
        embed1 = discord.Embed(colour=await getcolour(self, interaction.user),
                               description="🎰 Slots")
        embed1.add_field(name=f"Slots:",
                         value=f"[<a:slot:1037066744105291918> <a:slot:1037066744105291918> <a:slot:1037066744105291918>]",
                         inline=False)
        embed1.add_field(name="💰 Einsatz", value=f"{betrag} 🍪", inline=False)
        embed1.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed1.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")

        # embed2
        embed2 = discord.Embed(colour=await getcolour(self, interaction.user),
                               description="🎰 Slots")
        embed2.add_field(name=f"Slots", value=f"[{e1} <a:slot:1037066744105291918> <a:slot:1037066744105291918>]",
                         inline=False)
        embed2.add_field(name="💰 Einsatz", value=f"{betrag} 🍪", inline=False)
        embed2.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed2.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")

        # embed3
        embed3 = discord.Embed(colour=await getcolour(self, interaction.user),
                               description="🎰 Slots")
        embed3.add_field(name=f"Slots", value=f"[{e1} {e2} <a:slot:1037066744105291918>]", inline=False)
        embed3.add_field(name="💰 Einsatz", value=f"{betrag} 🍪", inline=False)
        embed3.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed3.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        # ergebnisse überprüfen
        # embedchanges
        await interaction.response.send_message(embed=embed1)
        await asyncio.sleep(1.5)
        await interaction.edit_original_response(embed=embed2)
        await asyncio.sleep(1.5)
        await interaction.edit_original_response(embed=embed3)
        if e1 == e2 == e3:
            await asyncio.sleep(1.5)
            embed4 = discord.Embed(colour=await getcolour(self, interaction.user),
                                    description="🎰 Slots")
            embed4.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed4.add_field(name=f"Slots", value=f"[{e1} {e2} {e3}]", inline=False)
            embed4.add_field(name="🏆 Gewinn", value=f"Du gewinnst {betrag * 3} 🍪",
                                inline=False)
            embed4.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            await update_account(self, interaction.user, "rucksack", 3 * betrag, 0)
            await interaction.edit_original_response(embed=embed4)
            return
        if e1 == e3 != e2 or e1 == e2 != e3 or e2 == e1 != e3 or e2 == e3 != e1 or e3 == e1 != e2 or e3 == e2 != e1:
            await asyncio.sleep(1.5)
            embed4 = discord.Embed(colour=await getcolour(self, interaction.user),
                                    description="🎰 Slots")
            embed4.add_field(name=f"Slots", value=f"[{e1} {e2} {e3}]", inline=False)
            embed4.add_field(name="💰 Unentschieden", value=f"Du behältst {betrag} 🍪",
                                inline=False)
            embed4.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            embed4.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.edit_original_response(embed=embed4)
            return
        else:
            await asyncio.sleep(1.5)
            embed4 = discord.Embed(colour=await getcolour(self, interaction.user),
                                    description="🎰 Slots")
            embed4.add_field(name=f"Slots", value=f"[{e1} {e2} {e3}]", inline=False)
            embed4.add_field(name="💰 Verloren", value=f"Du verlierst {betrag} 🍪",
                                inline=False)
            embed4.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            embed4.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await update_account(self, interaction.user, "rucksack", 0, betrag)
            await interaction.edit_original_response(embed=embed4)
            return

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=rps(None, None, None, self.bot, None))
        
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def rps(self, interaction: discord.Interaction, betrag: int):
        """Game, Schere Stein Papier. Deine Reaktion ist deine Entscheidung."""
        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Der Befehl ist zurzeit nicht verfügbar.**", ephemeral=True)
        # überprüfen ob er geld hat
        acc = await open_acc(self, interaction.user)
        rucksack = int(acc[0])
        if betrag < 0:
            await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> Der Betrag muss eine positive Zahl sein.", ephemeral=True)
            return
        if betrag > rucksack:
            await interaction.response.send_message(f"<:v_kreuz:1049388811353858069> Du hast nicht so viel Geld in deinem Rucksack. Dir fehlen **{betrag - rucksack} 🍪**.", ephemeral=True)
            return
        embed = discord.Embed(
            color=await getcolour(self, interaction.user),
            description=f"✊ Schere, Stein oder Papier?\nEinsatz: {betrag} 🍪",
            timestamp=datetime.now()
        )
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        emojis = ["✌️", "✊", "✋"]
        choice = random.choice(emojis)
        await interaction.response.send_message(embed=embed, view=rps(choice, betrag, interaction.user, self.bot, interaction))

    job = app_commands.Group(name='job', description='Bewirb dich für Jobs, kündige diese oder lass sie dir alle anzeigen.', guild_only=True)
    
    @job.command()
    @app_commands.autocomplete(beruf=job_autocomplete)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def apply(self, interaction: discord.Interaction, beruf: str):
        """Bewirb dich für einen Job."""
        acc = await open_acc(self, interaction.user)
        job = acc[2]
        user_hours = acc[3]
        a = 0
        if await get_job(self, interaction.user) == "Kein Job":
            for job in jobs:
                a += 1
                if job["name"] == beruf:
                    if int(user_hours) >= job["req"]:
                        await set_job(self, interaction.user, beruf)
                        success_embed = discord.Embed(description=f'Herzlichen Glückwunsch! Deine Bewerbung als **{beruf}** wurde angenommen.',
                                                        colour=await getcolour(self, interaction.user))
                        await interaction.response.send_message(embed=success_embed)
                        success_embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                        return
                    else:
                        not_enough_hours_error_embed = discord.Embed(description=f'Um sich als {beruf} zu bewerben, musst du mindestens **{job["req"]}** Stunden gearbeitet haben.',
                                                                        color=await getcolour(self, interaction.user))
                        not_enough_hours_error_embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                        await interaction.response.send_message(embed=not_enough_hours_error_embed)
                        return
            if a >= 53:
                not_a_job_error_embed = discord.Embed(description=f"Der Job **{beruf}** existiert nicht. Schau dir alle Jobs mit dem Command `/job list` an.",
                                                    colour=await getcolour(self, interaction.user))
                not_a_job_error_embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                await interaction.response.send_message(embed=not_a_job_error_embed)
                return
        else:
            active_job = await get_job(self, interaction.user)
            active_job_error_embed = discord.Embed(description=f'Du bist derzeit noch als **{active_job}** angestellt!\n'
                                                                f'Beende deinen Job als **{active_job}** mit `/job quit`',
                                                    colour=await getcolour(self, interaction.user))
            active_job_error_embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(embed=active_job_error_embed)
            return

    @job.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def quit(self, interaction: discord.Interaction):
        """Beende deinen aktuellen Job."""
        job = await get_job(self, interaction.user)
        if job != "Kein Job":
            success_embed = discord.Embed(description=f'Du hast deinen Job als **{job}** gekündigt.',
                                          colour=await getcolour(self, interaction.user))
            await set_job(self, interaction.user, "Kein Job")
            success_embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(embed=success_embed)
            return
        else:
            error_embed = discord.Embed(description=f"Du hast keinen Job, also kannst du nicht kündigen.\nBewerbe dich für einen Job mit `/job apply <job>`", color=discord.Colour.red())
            error_embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(embed=error_embed)

    @job.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def list(self, interaction: discord.Interaction):
        """Erhalte eine Liste aller Jobs."""
        await interaction.response.send_message(embed=discord.Embed(title=':dividers: Jobliste',
                                                                    description=f"Hier siehst du alle verfügbaren Jobs.\nDu kannst dich für einen Job bewerben mit `/job apply <job>`\n\n" + await job_list(self, interaction, 1),
                                                                    colour=await getcolour(self, interaction.user)).set_footer(text='Seite 1 von 11'), view=joblist(interaction, self.bot, self))

    shop = app_commands.Group(name='shop', description='Erstelle Items für deinen Server. Nutzer können diese kaufen.', guild_only=True)
    item = app_commands.Group(name='item', description='Erstelle Items für deinen Server. Nutzer können diese kaufen.', parent=shop, guild_only=True)
    
    @item.command()
    @app_commands.checks.has_permissions(administrator=True)
    async def hinzufügen(self, interaction: discord.Interaction, titel: str, kaufpreis: int, beschreibung: str, rolle: discord.Role=None):
        """Füge ein Item dem Shop hinzu."""
        item = await getshopitem(self, interaction.guild, titel)
        if item is False:
            await addshopitem(self, interaction.guild, titel, beschreibung, kaufpreis, rolle)
            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Item hinzugefügt", description=f"Das Item {titel} wurde zum Shop dieses Servers hinzugefügt.")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(embed=embed)
            return
        if item is True:
            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Item bereits vorhanden", description=f"Das Item {titel} gibt es bereits im Shop dieses Servers. Bitte wähle einen anderen Namen für das Item.")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @item.command()
    @app_commands.checks.has_permissions(administrator=True)
    async def entfernen(self, interaction: discord.Interaction, titel: str):
        """Entferne ein Item aus dem Shop."""
        item = await getshopitem(self, interaction.guild, titel)
        if item is True:
            await removeshopitem(self, interaction.guild, titel)
            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Item gelöscht", description=f"Das Item {titel} wurde aus dem Shop dieses Servers gelöscht.")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(embed=embed)
            return
        if item is False:
            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Item nicht vorhanden", description=f"Das Item {titel} gibt es nicht im Shop dieses Servers. Bitte gib den korrekten Namen für das Item an.")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @shop.command()
    async def anzeigen(self, interaction: discord.Interaction):
        """Zeigt dir alle Items im Shop."""
        items = await listshopitems(self, interaction.guild)
        if items == False:
            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Keine Items vorhanden", description=f"Es gibt keine Items in dem Shop dieses Servers.\nFüge Items hinzu mit dem Command `/shop item hinzufügen`")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        else:
            a = 0
            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Alle Items dieses Servers", description=f"Dieser Server hat ein paar Items im Shop.")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            for item in items:
                a += 1
                #guildID, titel, beschreibung, preis, roleID
                if item[4]:
                    rolle = interaction.guild.get_role(int(item[4]))
                    embed.add_field(name=item[1], value=f"{item[2]}\n**Preis:** {item[3]}\n**Rolle:** {rolle.mention}")
                else:
                    embed.add_field(name=item[1], value=f"{item[2]}\n**Preis:** {item[3]}")

            if a == 0:
                embed = discord.Embed(color=await getcolour(self, interaction.user), title="Keine Items vorhanden", description=f"Es gibt keine Items in dem Shop dieses Servers.\nFüge Items hinzu mit dem Command `/shop item hinzufügen`")
                embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            await interaction.response.send_message(embed=embed)

    @item.command()
    async def kaufen(self, interaction: discord.Interaction, item: str):
        """Kaufe ein Item aus dem Shop."""
        i = await getshopitem(self, interaction.guild, item)
        if i == False:
            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Item nicht vorhanden", description=f"Das Item {item} gibt es nicht im Shop dieses Servers. Bitte gib den korrekten Namen für das Item an.")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(embed=embed)
            return
        if i == True:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT preis FROM economy_shop WHERE guildID = (%s) AND titel = (%s)", (interaction.guild.id, item))
                    result = await cursor.fetchone()
                    if result is None:
                        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Item nicht vorhanden", description=f"Das Item {item} gibt es nicht im Shop dieses Servers. Bitte gib den korrekten Namen für das Item an.")
                        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return
                    else:
                        canbuy = await checkbalance(self, interaction.user, result[0])
                        if canbuy == True:
                            await buyitem(self, interaction.user, interaction.guild, item)
                            await update_account(self, interaction.user, "rucksack", 0, result[0])
                            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Item gekauft", description=f"Das Item {item} wurde von dir gekauft. Ich habe es für dich in deinen Rucksack getan!")
                            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                            await interaction.response.send_message(embed=embed)
                            return
                        if canbuy == False:
                            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Item nicht gekauft", description=f"Das Item {item} wurde von dir nicht gekauft. Du hast zu wenig Geld in deinem Rucksack!")
                            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return

    @item.command()
    async def meine(self, interaction: discord.Interaction):
        """Zeigt alle deine gekauften Items vom Shop."""
        items = await getuseritems(self, interaction.user)
        if items == False:
            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Keine Items vorhanden", description=f"Es gibt keine Items in deinem Rucksack.\nKaufe Items mit dem Command `/shop item kaufen`")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        else:
            a = 0
            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Alle Items in deinem Rucksack", description=f"In deinem Rucksack sind ein paar Items.")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            for item in items:
                a += 1
                embed.add_field(name=item[1], value=f"{item[2]}\n**Hat gekostet:** {item[3]}")
            if a == 0:
                embed = discord.Embed(color=await getcolour(self, interaction.user), title="Keine Items vorhanden", description=f"Es gibt keine Items in deinem Rucksack.\nKaufe Items mit dem Command `/shop item meine`")
                embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            await interaction.response.send_message(embed=embed)
    
    @item.command()
    async def verkaufen(self, interaction: discord.Interaction, item: str):
        """Verkaufe ein Item aus deinem Rucksack. Du bekommst zufällige Prozente des Kaufpreises wieder. Prozente im Bereich von 65% bis 115%"""
        items = await getuseritems(self, interaction.user)
        if items == False:
            embed = discord.Embed(color=await getcolour(self, interaction.user), title="Keine Items vorhanden", description=f"Es gibt keine Items in deinem Rucksack.\nKaufe Items mit dem Command `/shop item kaufen`")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        else:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT preis FROM economy_shop WHERE guildID = (%s) AND titel = (%s)", (interaction.guild.id, item))
                    preis = await cursor.fetchone()
                    Prozente = random.uniform(0.65, 1.15)
                    verkaufspreis = round(Prozente * int(preis[0]))
                    await sellitem(self, interaction.user, item)
                    await update_account(self, interaction.user, "rucksack", verkaufspreis, 0)
                    embed = discord.Embed(color=await getcolour(self, interaction.user), title="Item verkauft", description=f"Das Item {item} wurde für {verkaufspreis} 🍪 verkauft. Du hast es nun nicht mehr im Rucksack.")
                    embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                    await interaction.response.send_message(embed=embed)
            
async def setup(bot):
    await bot.add_cog(economy(bot))