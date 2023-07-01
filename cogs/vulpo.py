import asyncio
import math
import typing
import discord
from discord.ext import commands
from datetime import datetime
import time
import sys
import psutil
from discord import app_commands
from info import discord_timestamp
from info import getcolour

class Dropdown(discord.ui.Select):
    def __init__(self, user, farbe):
        selectOptions = [
            discord.SelectOption(label="Premium", emoji="<:v_ticket:1119584819597279242>"),
            discord.SelectOption(label="Information", emoji="<:v_info:1119579853092552715>"),
            discord.SelectOption(label="Settings & Setup", emoji="<:v_einstellungen:1119578559086874636>"),
            discord.SelectOption(label="Basic Moderation", emoji="<:v_mod:1119581819122241621>"),
            discord.SelectOption(label="Levelsystem", emoji="<:v_levelup:1119581140240576612>"),
            discord.SelectOption(label="Giveaway", emoji="<:v_geschenk:1119579279274025060>"),
            discord.SelectOption(label="Stats", emoji="<:v_stats:1119583678083895346>"),
            discord.SelectOption(label="Ticketsystem", emoji="<:v_ticket:1119584819597279242>"),
            discord.SelectOption(label="Nachrichten", emoji="<:v_chat:1119577968457568327>"),
            discord.SelectOption(label="Auto Moderation", emoji="<:v_schutz:1119582601104076943>"),
            discord.SelectOption(label="Fun", emoji="<:v_smiley:1119583113153089626>"),
            discord.SelectOption(label="Economy", emoji="<:v_cookie:1119578273580593232>"),
            discord.SelectOption(label="Minispiele", emoji="<:v_spiel:1119583527919435796>")
        ]
        super().__init__(placeholder="Wähle eine Seite", min_values=1, max_values=1, options=selectOptions, custom_id="Dropdown-Help")
        self.user = user
        self.farbe = farbe
    async def callback(self, interaction: discord.Interaction):
        if self.user.id != interaction.user.id:
            return await interaction.response.defer(thinking=False, ephemeral=True)
        
        if self.values[0] == "Premium":
            anzeige = """
> <:v_info:1119579853092552715> Spezielle Befehle und Funtkionen, nur für Premium Nutzer.

__<:v_user:1119585450923929672> User Befehle__
`/premium embedfarbe` Ändere die Farbe aller Embeds, die dir gesendet werden von Vulpo.
`/premium rangkarte` Ändere das Bild deiner Rangkarte.

__<:v_ticket:1119584819597279242> Premium erhalten__
Premium ist heiß begehrt. Du kannst es bekommen, indem du ein Abonnement wirst: https://vulpo-bot.de/premium."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Stats":
            anzeige = """
> <:v_info:1119579853092552715> Vulpos Stats System basiert auf Tracking von Mitgliedern, wie aktiv sie in Text- und Sprachkanälen sind.

__<:v_user:1119585450923929672> User Befehle__
`/stats anzeigen` Zeigt Stats für Member und Kanäle.
`/stats top` Lass dir die besten Stats dieses Servers anzeigen.
`/stats lookback` Zeigt Stats für Member und Kanäle von einem bestimmten Zeitraum.

__<:v_einstellungen:1119578559086874636> Team Befehle__
`/stats blacklist` Setze Kanäle auf die Blacklist für Nachrichten.
`/stats reset` Setze alle Stats auf 0 zurück.
`/statschannel` Richte einen Stats-Kanal ein."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Auto Moderation":
            anzeige = """
> <:v_info:1119579853092552715> Dieses System ermöglicht dir automatische Handlungen gegen Nutzer, die eine bestimmte Warnanzahl erreicht haben. Warns können manuell und automatisch, über z.B.: Blacklist, verteilt werden.

__<:v_user:1119585450923929672> User Befehle__
Keine User Befehle.

__<:v_einstellungen:1119578559086874636> Team Befehle__
`/warn` Warne einen User.
`/unwarn` Entferne eine Warnung eines Users.
`/listwarn` Zeigt wie viele Warnungen ein User hat.

`/modlog` Richte einen Moderationlog ein.
`/messagelog` Richte einen MessageLog ein.

`/automod addaction` Füge hinzu Automod-Aktionen hinzu.
`/automod removeaction` Entferne Automod-Aktionen.
`/automod liste` Lass dir alle Automod-Aktionen anzeigen.
`/automod caps` Füge einen Caps Filter hinzu.
`/automod spam` Füge einen Spam Filter hinzu.

`/blacklist show` Zeigt alle Wörter auf der Blacklist an.
`/blacklist add` Füge ein Wort der Blacklist hinzu.
`/blacklist remove` Entferne ein Wort von der Blacklist."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Ticketsystem":
            anzeige = """
> <:v_info:1119579853092552715> Dieses Ticketsystem hat nur zwei Befehle. Cool oder? Alle Handlungen im Ticket werden durch Buttons gemanaged: öffnen, claimen, schließen, neu öffnen, löschen.

__<:v_user:1119585450923929672> User Befehle__
Keine User Befehle.

__<:v_einstellungen:1119578559086874636> Team Befehle__
`/createpanel` Erstelle ein Panel, womit User ein Ticket öffnen können.
`/ticketlog` Richte einen Ticketlog ein."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Nachrichten":
            anzeige = """
> <:v_info:1119579853092552715> Die Kategorie Nachrichten beschreibt Befehle, mit denen du auf bestimmte Nachrichten reagieren kannst. Automatisch und manuell. z.B.: automatische Reaktionen

__<:v_user:1119585450923929672> User Befehle__
Keine User Befehle.

__<:v_einstellungen:1119578559086874636> Team Befehle__
`/joinmsg` Lege eine Nachricht fest, wenn jemand joint.
`/testjoin` Überprüfe die Join Nachricht.
`/leavemsg` Lege eine Leave Nachricht fest.
`/testleave` Überprüfe die Leave Nachricht.
`/autoreact add` Richte Auto Reaktionen in Channels ein.
`/autoreact delete` Entferne automatische Reaktionen von Kanälen.
`/autoreact liste` Lass dir alle automatischen Reaktionen anzeigen.
`/embed` Mache eine eine eingebettete Nachricht.
`/tag add` Erstelle einen Tag.
`/tag delete` Entferne einen Tag.
`/tag liste` Lass dir alle Tags anzeigen.
`/reportlog` Lege einen Kanal fest für gemeldete Nachrichten von Usern.

Außerdem:
Jeder Nutzer kann die Custom Befehle des Tags System nutzen. Wenn erstmal ein Tag erstellt wurde kann jeder User ihn mit `!tag tagname` ausführen.

❓ Du suchst nach Stats? Sieh dir die Kategorie Stats an! ;)"""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Information":
            anzeige = """
> <:v_info:1119579853092552715> Hier stehen Befehle, die hauptsächlich Informationen ausgeben oder nützlich sind.

__<:v_user:1119585450923929672> User Befehle__
`/about` Infos über Vulpo.
`/help` Alle wichtigen Links und Befehle.
`/invite` Link, um Vulpo einzuladen.
`/support` Zeigt einen Link für den Support-Server.
`/vote` Zeigt an, wann du wieder für Vulpo voten kannst.
`/info server` Infos zum Server.
`/servericon` Zeigt das Server Profilbild.
`/info member` Infos zu einem Member.
`/info role` Infos zu einer Rolle.
`/info channel` Infos zu einem Channel.
`/permissions` Listet alle Berechtigungen von jemandem auf.
`/ping`  Zeigt den Ping.
`/umfrage` Erstelle eine Umfrage.
`/mostvoted` Bekomme eine Liste von den 10 Usern, die am öftesten gevotet haben.
`/random` Erhalte eine random Zahl von deinen ausgewählten Zahlen.
`/translate` Übersetze einen Text in mehrere Sprachen.
`/bestenliste` Erhalte Bestenlisten verschiedenster Funktionen.
`/invites` Zeigt die Einladungen eines Users.

__<:v_einstellungen:1119578559086874636> Team Befehle__
Keine Team Befehle."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Settings & Setup":
            anzeige = """
> <:v_info:1119579853092552715> Diese Kategorie bietet dir Einstellungen für deinen Server wie Joinrollen und Tags. Außerdem findest du dort nützliche Befehle für dich selbst.

__<:v_user:1119585450923929672> User Befehle__
`/erinnerung erstellen` Erstelle dir eine Erinnerung für eine bestimmte Uhrzeit.
`/erinnerung löschen` Entfernt eine Erinnerung.
`/erinnerung anzeigen` Bekomme eine Liste von deinen Erinnerungen.
`/afk` Setze dich AFK.
`/starboard` - Lege einen Kanal fest für Nachrichten mit 5 Sternen von Usern.

__<:v_einstellungen:1119578559086874636> Team Befehle__
`/joinrole` Lege eine Joinrolle fest.
`/botrole` Lege eine Botrolle fest.
`/voicesetup` Erstelle einen "Join to Create" Kanal.
`/reactionrole` Erstelle Reaktionsrollen."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Basic Moderation":
            anzeige = """
> <:v_info:1119579853092552715> Dies sind Befehle, die eigentlich jeder Bot hat. Einfache Moderation per Slash Befehle.

__<:v_user:1119585450923929672> User Befehle__
Keine User Befehle.

__<:v_einstellungen:1119578559086874636> Team Befehle__
`/kick` Kicke einen User.
`/ban` Banne einen User.
`/unban` Entbanne einen User.
`/banlist` Zeigt dir eine Liste, die Gebannt wurden.
`/clear channel` Lösche Nachrichten in einem Channel.
`/clear between` Lösche alle Nachrichten zwischen zwei Nachrichten eines Kanals.

❓ Du suchst nach Verwarnungs Befehlen? Guck mal in der Kategorie Auto Moderation nach! ;)"""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Levelsystem":
            anzeige = """
> <:v_info:1119579853092552715> Das Levelsystem vonn Vulpo ist umfassend. Coole Rangnachrichten und viele Einstellungsmöglichkeiten für Moderatoren.

__<:v_user:1119585450923929672> User Befehle__
`/rank` Zeigt dir welches Level du bist.

__<:v_einstellungen:1119578559086874636> Team Befehle__
`/levelsystem status` Zeigt, ob das Levelystem aktiviert/deaktiviert ist.
`/levelsystem role add/delete/list` Richte Rollen ein die beim Erreichen eines bestimmten Levels automatisch gegeben werden soll.
`/levelystem levelupmessage` Richte eine Levelup Nachricht ein.
`/levelsystem Levelupkanal` Richte ein, in welchem Kanal die Levelup Nachricht geschickt werden soll.
`/levelsystem block channel/rolle` Richte Channels/Rollen ein, die keine Level sammeln können.
`/setlevel` Setze einen User zu einem bestimmten Level.
`/xpboost` Starte einen XP Boost auf deinem Server."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Giveaway":
            anzeige = """
> <:v_info:1119579853092552715> Hinter dem Giveaway System steckt mehr als du denkst. Nicht nur Starten und blacklist, bypassrollen und verwalten. Die Gewinnspiele enden sogar nicht bei Bot Neustart, sondern laufen normal bis zum Ende weiter.
> Man kann ebenso Anforderungen einstellen. Hinter denen steckt noch die ganze Magie. Das Stats System ist mit verknüpft bei Nachrichten. Außerdem ist das Levelsystem mit vernetzt bei Levelanforderungen. Buttons gibt es auch.

__<:v_user:1119585450923929672> User Befehle__
Keine User Befehle.

__<:v_einstellungen:1119578559086874636> Team Befehle__
`/gewinnspiel starten` Starte ein neues Gewinnspiel.
`/gewinnspiel verwalten` Verwalte Gewinnspiele. 
`/gewinnspiel bypassrolle` Bearbeite Rollen, die die Bedingungen umgehen. 
`/gewinnspiel blacklist` Setze Member und Rollen auf die Blacklist."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Fun":
            anzeige = """
> <:v_info:1119579853092552715> Schon lange nicht mehr gelacht xD? Dann wird es mal Zeit. Denn mit diesen Befehlen wirst du zu 99% lachen!

__<:v_user:1119585450923929672> User Befehle__
`/ask` Frage eine berühmte Person eine Frage
`/avatar` Zeigt das Profilbild eines Users an
`/cat` Schicke ein zufälliges Bild einer Katze.
`/color` Bekomme eine zufällige Farbe
`/emojiurl` Bekomme das URL eines Emojis
`/games` Zeigt alle Spiele an, die grade gespielt werden
`/regenbogen` Sendet dein Profilbild mit einem Regenbogen Filter.
`/iq` Zeigt das IQ von einem User an.
`/lostrate` Zeigt wie lost ein User ist.
`/los` Ziehe ein Rubbellos.
`/love` Finde heraus wie verliebt zwei User sind
`/meme` Bekomme ein zufälliges Meme.
`/password` Generiert ein zufälliges Passwort für dich.
`/pix` Verpixelt ein Profilbild eines Users.
`/tictactoe start/stats` Spiele tictacoe mit jemanden und sieh dir deine Tik Tak Toe Stats an.
`/triggered` Zeigt, dass du getriggered bist.
`/wanted` Erstellt ein "Gesucht" Plakat mit dem Profilbild eines Users.
`/wasted` Sendet ein Profilbild mit Effekten.
`/wetter` Zeigt das Wetter eines bestimmten Orts.
`/stealemoji` Stiehlt ein emoji von einem Server.

__<:v_einstellungen:1119578559086874636> Team Befehle__
Keine Team Befehle."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Minispiele":
            anzeige = """
> <:v_info:1119579853092552715> Du langweilst dich? Dann probier mal diese Spiele aus. Sie werden dir die Langeweile vertreiben!

__<:v_user:1119585450923929672> User Befehle__
`/speedgame` Teste deine Schnelligkeit und steige Ränge auf.

__<:v_einstellungen:1119578559086874636> Team Befehle__
`/emojiquiz` Verwalte das Emojiquiz deines Servers.
`/counting set` Richte den Zählkanal ein.
`/counting zahl` Stelle die aktuelle Zahl des Counting Kanals ein.
`/counting disable` Deaktiviere das Minispiel.
`/guessthenumber` Verwalte das Minispiel 'Guess the number' auf deinem Server."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Economy":
            anzeige = """
> <:v_info:1119579853092552715> Das globale Wirtschaftssystem von Vulpo bietet viel Spaß und Strategie. Messe dich mit anderen und steige in der Berufsleiter nach oben auf!

__<:v_user:1119585450923929672> User Befehle__
`/cookies anzeigen` Öffne das Profil eines Users.
`/cookies abheben` Hebe Geld von der Bank ab.
`/cookies einzahlen` Überweise Geld auf die Bank.

`/daily` Hole tägliche Cookies ab.
`/work` Gehe Arbeiten.
`/beg` gehe betteln.
`/send` Gebe einem User Cookies.
`/rob` Raube einen User aus.
`/rps` Spiele Schere, Stein, Papier um Cookies.
`/slot` Spiele Casino.

**Job System**
`/job apply` Bewerbe dich für einen Job.
`/job quit` Verlasse deinen Job.
`/job list` Zeigt dir eine Liste aller Jobs.


**Shop System**
`/shop anzeigen` Zeigt dir alle Items im Shop.
`/shop item kaufen` Kaufe ein Item aus dem Shop.
`/shop item verkaufen` Verkaufe ein Item aus deinem Rucksack. Du bekommst zufällige Prozente des Kaufpreises wieder. Prozente im Bereich von 65% bis 115%
`/shop item meine` Zeigt alle deine gekauften Items vom Shop.

__<:v_einstellungen:1119578559086874636> Team Befehle__
**Shop System**
`/shop item hinzufügen` Füge ein Item dem Shop hinzu.
`/shop item entfernen` Entferne ein Item aus dem Shop."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.response.edit_message(embed=embed)

class DropdownView(discord.ui.View):
    def __init__(self, user, farbe):
        super().__init__(timeout=None)
        self.add_item(Dropdown(user, farbe))

class vulpo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.t1 = math.floor(datetime.now().timestamp())
        self.t2 = datetime.fromtimestamp(int(self.t1))
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(DropdownView(None, None))

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def help(self, interaction: discord.Interaction):
        """Wichtige Links wie invite, support, vote und viele andere Infos."""
        farbe = await getcolour(self, interaction.user)
        embed = discord.Embed(title="Help Menü", description=f"""
<:v_info:1119579853092552715> Danke dass du mich benutzt. Hier findest du alle Befehle von mir und wichtige Links.
Für mehr Hilfe, joine bitte unserem [Support-Server ➚](https://discord.gg/49jD3VXksp).

**Alle Kategorien**
> <:v_info:1119579853092552715> Information
> <:v_einstellungen:1119578559086874636> Settings & Setup
> <:v_mod:1119581819122241621> Basic Moderation
> <:v_levelup:1119581140240576612> Levelsystem
> <:v_geschenk:1119579279274025060> Giveaway
> <:v_stats:1119583678083895346> Stats
> <:v_ticket:1119584819597279242> Ticketsystem
> <:v_chat:1119577968457568327> Nachrichten
> <:v_schutz:1119582601104076943> Auto Moderation
> <:v_smiley:1119583113153089626> Fun
> <:v_cookie:1119578273580593232> Economy
> <:v_spiel:1119583527919435796> Minispiele

**Letzte Updates**
<:v_info:1119579853092552715> Starboard für coole Nachrichten -> `/starboard`
<:v_info:1119579853092552715> Tempchannels nun mit **Interface verfügbar** -> `/voicesetup`
<:v_info:1119579853092552715> Reportlog - melde Nutzer per Rechtsklick ans Team -> `/reportlog`
<:v_info:1119579853092552715> Statschannel - fertige live Stats Kanäle an -> `/statschannel`

**Links**
[Einladen](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands) **|** [Support](https://discord.gg/49jD3VXksp) **|** [Voten](https://top.gg/bot/925799559576322078/vote)
""", color=farbe)
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        embed.set_author(name="Vulpo", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
        embed.set_thumbnail(url=interaction.guild.icon)
        await interaction.response.send_message(embed=embed, view=DropdownView(interaction.user, farbe))

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def vote(self, interaction: discord.Interaction):
        """Zeigt an, wann du wieder für Vulpo voten kannst."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT endtime FROM vote WHERE userid = (%s)", (interaction.user.id))
                result = await cursor.fetchone()
                if result == None:
                    embed = discord.Embed(title="Du kannst voten", url="https://top.gg/bot/925799559576322078/vote", description="""
<:v_info:1119579853092552715> Der Vote-Cooldown von 12 Stunden ist abgelaufen. Es wäre sehr schön, wenn du wieder für mich votest.

<:herz:941398727501955113> Als Belohnung für einen weiteren Vote bekommst du **300 🍪 im Economy System** und eine besondere **Rolle in [Vulpos Wald](https://discord.gg/49jD3VXksp)**""", colour=await getcolour(self, interaction.user))
                    embed.set_footer(text="Danke für deine Unterstützung", icon_url="https://media.discordapp.net/attachments/965302660871884840/965315155816767548/Vulpo_neu.png?width=1572&height=1572")
                    return await interaction.response.send_message(embed=embed)
                t1 = int(result[0])
                t2 = datetime.fromtimestamp(int(t1))
                embed = discord.Embed(title="Du kannst noch nicht voten", url="https://top.gg/bot/925799559576322078/vote", description=f"""
<:v_info:1119579853092552715> Der Vote-Cooldown von 12 Stunden ist noch nicht abgelaufen. Du kannst wieder {discord_timestamp(t2, "R")} voten.

<:herz:941398727501955113> Als Belohnung für einen weiteren Vote bekommst du **300 🍪 im Economy System** und eine besondere **Rolle in [Vulpos Wald](https://discord.gg/49jD3VXksp)**""", colour=await getcolour(self, interaction.user))
                embed.set_footer(text="Danke für deine Unterstützung", icon_url="https://media.discordapp.net/attachments/965302660871884840/965315155816767548/Vulpo_neu.png?width=1572&height=1572")
                await interaction.response.send_message(embed=embed)
        
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def about(self, interaction: discord.Interaction):
        """Zeigt Infos über mich."""
        bot = interaction.guild.get_member(925799559576322078)
        erstellt1 = math.floor(bot.created_at.timestamp())
        erstellt2 = datetime.fromtimestamp(int(erstellt1))
        
        verifiziert = datetime.fromtimestamp(1648256400)

        #alle user
        all_users = 0
        for guild in self.bot.guilds:
            for member in guild.members:
                all_users += 1

        #teammember
        guild = self.bot.get_guild(925729625580113951)
        role = guild.get_role(947881106332582018)
        teammember = ""
        for member in role.members:
            if str(teammember) == "":
                teammember += f"{member}"
            else:
                teammember += f", {member}"

        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Infos über Vulpo", description=f"""
<:v_statusonline:1037071233902182491> Vulpo wurde {discord_timestamp(erstellt2, 'R')} erstellt
<:v_verifiedbot:1037069972226179182> Vulpo wurde {discord_timestamp(verifiziert, 'R')} verifiziert
<:v_info:1119579853092552715> Vulpo ist {discord_timestamp(self.t2, 'R')} online gegangen.

<:v_verifiedbotdeveloper:1037070049539788851> Entwickler: {self.bot.get_user(824378909985341451)}
<:v_mod:1119581819122241621> Team: {teammember}

<:v_info:1119579853092552715> Server: {len(self.bot.guilds)}
<:v_user:1119585450923929672> User: {all_users}
❗ Commands: {len(self.bot.tree.get_commands())}

<:v_python:1037073367175544932> Python Version: {str(sys.version)[0]}{str(sys.version)[1]}{str(sys.version)[2]}{str(sys.version)[3]}{str(sys.version)[4]}{str(sys.version)[5]}
<:v_discordpy:1037073431969140798> Library: discord.py: {discord.__version__}
🎛 CPU: {psutil.cpu_percent()}%
""")
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def invite(self, interaction: discord.Interaction):
        """Zeigt einen Link um mich einzuladen."""
        embed = discord.Embed(colour=await getcolour(self, interaction.user), title=f"Vulpo auf anderen Servern verwenden", description=f"Du kannst Vulpo mit [diesem Link](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands) zu deinem Server hinzufügen.", url="https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands")
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def support(self, interaction: discord.Interaction):
        """Zeigt einen Link für den Support-Server."""
        embed = discord.Embed(colour=await getcolour(self, interaction.user), title=f"Bekomme Hilfe", description=f"Wenn du Hilfe benötigst, kannst du meinem Supportserver über [diesen Link](https://discord.gg/49jD3VXksp) beitreten.", url="https://discord.gg/49jD3VXksp")
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def ping(self, interaction: discord.Interaction):
        """Zeigt den Ping von den verschiedensten Funktionen."""
        #db
        t_1 = time.perf_counter()
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT user_xp FROM levelsystem WHERE client_id = 925729625580113951")
                r = await cursor.fetchall()

        t_2 = time.perf_counter()
        time_delta1 = round((t_2 - t_1) * 1000)

        bot = round(self.bot.latency * 1000)
        t_3 = time.perf_counter()
        embed = discord.Embed(title="Internetgeschwindigkeit", description=f"```Bot: {bot} ms\nDatenbank: {time_delta1} ms```", color=await getcolour(self, interaction.user))
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

        #Answer
        t_4 = time.perf_counter()
        time_delta2 = round((t_4 - t_3) * 1000)
        embed = discord.Embed(title="Internetgeschwindigkeit", description=f"```Bot: {bot} ms\nDatenbank: {time_delta1} ms\nDiscord-Api: {time_delta2} ms```", color=await getcolour(self, interaction.user))
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.edit_original_response(embed=embed)

async def setup(bot):
    await bot.add_cog(vulpo(bot))