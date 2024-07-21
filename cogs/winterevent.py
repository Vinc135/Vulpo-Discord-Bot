import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import getcolour, haspremium_forserver
from datetime import date

async def change_points(bot, userID, punkte, p_n, tag):
    async with bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT punkte FROM adventskalender WHERE userID = (%s)", (userID))
            result = await cursor.fetchone()
            if result == None:
                punkte_vorher = 0
            else:
                punkte_vorher = int(result[0])
            punkte_neu = 0
            if p_n == "+":
                punkte_neu += (punkte_vorher + punkte)
                if result == None:
                    return await cursor.execute("INSERT INTO adventskalender(userID, punkte, tag) VALUES(%s, %s, %s)", (userID, punkte_neu, tag))
                await cursor.execute("UPDATE adventskalender SET punkte = (%s) WHERE userID = (%s)", (punkte_neu, userID))
                await cursor.execute("UPDATE adventskalender SET tag = (%s) WHERE userID = (%s)", (tag, userID))

            if p_n == "-":
                punkte_neu += (punkte_vorher - punkte)
                if result == None:
                    return await cursor.execute("INSERT INTO adventskalender(userID, punkte, tag) VALUES(%s, %s, %s)", (userID, punkte_neu, 0))
                await cursor.execute("UPDATE adventskalender SET punkte = (%s) WHERE userID = (%s)", (punkte_neu, userID))

aufgaben = {
    1: {
        "Aufgabe": 'Vervollständige dieses Weihnachtslied: "O Tannenbaum, o Tannenbaum, wie ____ sind deine Blätter!"',
        "Lösung": 'grün',
        "Belohnung": 10
    },
    2: {
        "Aufgabe": 'Finde das versteckte Weihnachtswort: "R_N__ER"',
        "Lösung": 'RENTIER',
        "Belohnung": 10
    },
    3: {
        "Aufgabe": 'Löse fünf Emojiquizze. (`/emojiquiz`)',
        "Lösung": 'emojiquiz',
        "Belohnung": 10
    },
    4: {
        "Aufgabe": 'Vervollständige diesen Satz: "In der Weihnachtsbäckerei, gibt es ______ __________…"',
        "Lösung": 'manche Leckereien',
        "Belohnung": 15
    },
    5: {
        "Aufgabe": 'Was kommt vor dem Weihnachtsfest, ist oft weiß und hat viele Kanten?',
        "Lösung": 'Schneeflocke',
        "Belohnung": 15
    },
    6: {
        "Aufgabe": 'Welcher Heilige bringt kleine Geschenke in die Schuhe der Kinder?',
        "Lösung": 'St. Nikolaus',
        "Belohnung": 10
    },
    7: {
        "Aufgabe": 'Welche Pflanze wird oft als "Königin der Blumen" bezeichnet und ist ein traditioneller Weihnachtsschmuck?',
        "Lösung": 'Christrose',
        "Belohnung": 10
    },
    8: {
        "Aufgabe": 'Entschlüssle das folgende Weihnachtsrätsel: "Was ist weiß, flauschig und lebt am Nordpol?"',
        "Lösung": 'Weihnachtsschaf',
        "Belohnung": 10
    },
    9: {
        "Aufgabe": 'Welches traditionelle Weihnachtsgetränk enthält Eier, Zucker, Milch und Gewürze?',
        "Lösung": 'Eierpunsch',
        "Belohnung": 15
    },
    10: {
        "Aufgabe": 'Welcher Tag wird oft mit Kerzen in einem speziellen Leuchter namens "Lucia-Kranz" gefeiert?',
        "Lösung": 'Lucia-Tag (Luciafest)',
        "Belohnung": 15
    },
    11: {
        "Aufgabe": 'Entschlüssle das folgende Weihnachtsrätsel: "Was fliegt durch die Luft und hat eine rote Nase?"',
        "Lösung": 'Rentier',
        "Belohnung": 10
    },
    12: {
        "Aufgabe": 'Vervollständige diesen Satz: "Ihr Kinderlein, kommet, o kommet doch ___..."',
        "Lösung": 'all',
        "Belohnung": 10
    },
    13: {
        "Aufgabe": 'Welches Getränk wird oft mit Zimtstangen, Kardamom, Nelken und Milch zubereitet?',
        "Lösung": 'Chai Latte',
        "Belohnung": 10
    },
    14: {
        "Aufgabe": 'Was ist der Name des geizigen Hauptcharakters in Charles Dickens\' Weihnachtsgeschichte?',
        "Lösung": 'Ebenezer Scrooge',
        "Belohnung": 10
    },
    15: {
        "Aufgabe": 'Vervollständige dieses Weihnachtslied: "Kling, Glöckchen, ___, ..."',
        "Lösung": 'klingelingeling',
        "Belohnung": 10
    },
    16: {
        "Aufgabe": 'In welchem Land wird das Weihnachtsfest mit dem Begriff "Pasko" gefeiert?',
        "Lösung": 'Philippinen',
        "Belohnung": 15
    },
    17: {
        "Aufgabe": 'Was ist das traditionelle Gebäck, das man häufig in Form von Sternen, Glocken und Tannenbäumen findet?',
        "Lösung": 'Lebkuchen',
        "Belohnung": 15
    },
    18: {
        "Aufgabe": 'Entschlüssle das folgende Weihnachtsrätsel: "Was hat vier Beine, ein Geweih und fliegt durch die Luft?"',
        "Lösung": 'Rentierschlitten',
        "Belohnung": 10
    },
    19: {
        "Aufgabe": 'Welches weihnachtliche Instrument wird oft mit Engeln in Verbindung gebracht?',
        "Lösung": 'Harfe',
        "Belohnung": 10
    },
    20: {
        "Aufgabe": 'Was ist der höchste Berg in Deutschland, der oft im Winter mit Schnee bedeckt ist?',
        "Lösung": 'Zugspitze',
        "Belohnung": 10
    },
    21: {
        "Aufgabe": 'Welche mythischen Kreaturen bewachen den Nordpol und helfen dem Weihnachtsmann?',
        "Lösung": 'Weihnachtselfen',
        "Belohnung": 10
    },
    22: {
        "Aufgabe": 'Welcher Monat folgt auf Dezember?',
        "Lösung": 'Januar',
        "Belohnung": 10
    },
    23: {
        "Aufgabe": 'Entschlüssle das folgende Weihnachtsrätsel: "Was hat Flügel, kann aber nicht fliegen?"',
        "Lösung": 'Engel',
        "Belohnung": 10
    },
    24: {
        "Aufgabe": 'Entschlüssle dieses Rätsel.',
        "Lösung": 'mehrere',
        "Belohnung": 5
    }
}

class Modal(discord.ui.Modal, title="Antwort"):
    def __init__(self, bot, index):
        super().__init__(custom_id="lczguzegcuizegfuzge")
        self.bot = bot
        self.index = index
        self.add_item(discord.ui.TextInput(label="Deine Antwort", style=discord.TextStyle.short, required=True))

    async def on_submit(self, interaction: discord.Interaction):
        for index, aufgabe_info in aufgaben.items():
            if index == self.index:
                antwort = str(self.children[0].value)
                lösung = str(aufgabe_info["Lösung"])
                belohnung = int(aufgabe_info["Belohnung"])
                aktuelles_datum = date.today()
                aktueller_tag = aktuelles_datum.day

                if antwort.lower() == lösung.lower():
                    await change_points(self.bot, interaction.user.id, aufgabe_info["Belohnung"], "+", aktueller_tag)
                    await interaction.response.send_message(f"**✅ Richtig. Du hast {belohnung} Punkte erhalten.**", ephemeral=True)

                else:
                    await change_points(self.bot, interaction.user.id, 2, "-", aktueller_tag)
                    await interaction.response.send_message(f"**❌ Falsch. Für jeden falschen Versuch verlierst du 2 Punkte. Du kannst es so oft probieren, wie du willst.**", ephemeral=True)

class answer(discord.ui.View):
    def __init__(self, bot=None, index=None):
        super().__init__(timeout=None)
        self.bot = bot
        self.index = index

    @discord.ui.button(label='Antwort abgeben', style=discord.ButtonStyle.grey, custom_id="efdfiwrzfouzgw4izf", emoji="<:v_31:1264264994774585445>")
    async def antwort_prüfen(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT tag FROM adventskalender WHERE userID = (%s)", (interaction.user.id))
                result = await cursor.fetchone()
                if result != None:
                    if int(result[0]) == int(self.index):
                        return await interaction.response.send_message("**❌ Schau morgen wieder vorbei. Du hast das Türchen für heute schon geöffnet.**", ephemeral=True)
                    
        await interaction.response.send_modal(Modal(self.bot, self.index))
        
class winterevent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=answer(self.bot, None))
    
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def adventskalender(self, interaction: discord.Interaction):
        """Öffne das heutige Türchen des Adventskalenders."""
        if interaction.user.id != 824378909985341451:
            return await interaction.response.send_message("Gedulde dich noch. Diese Funktion ist noch nicht verfügbar.", ephemeral=True)
        aktuelles_datum = date.today()
        aktueller_tag = aktuelles_datum.day

        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT tag FROM adventskalender WHERE userID = (%s)", (interaction.user.id))
                result = await cursor.fetchone()
                if result != None:
                    if int(result[0]) == int(aktueller_tag):
                        return await interaction.response.send_message("**❌ Schau morgen wieder vorbei. Du hast das Türchen für heute schon geöffnet.**", ephemeral=True)
                    
        for index, aufgabe_info in aufgaben.items():
            if index == aktueller_tag:
                embed = discord.Embed(title=f"<:v_181:1264268817790664756> Heutiges Türchen: {aktueller_tag}", description=f"__Löse folgende Aufgabe und erhalte Punkte:__\n{aufgabe_info['Aufgabe']}", colour=await getcolour(self, interaction.user))
                await interaction.response.send_message(embed=embed, view=answer(self.bot, index), ephemeral=True)
        

async def setup(bot):
    await bot.add_cog(winterevent(bot))