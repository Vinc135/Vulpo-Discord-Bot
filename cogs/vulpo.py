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
from utils.utils import discord_timestamp, getcolour
from utils.MongoDB import getMongoDataBase

class Dropdown(discord.ui.Select):
    def __init__(self, user, farbe, bot):
        selectOptions = [
            #discord.SelectOption(label="Premium", emoji="<:v_ticket:1119584819597279242>"),
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
        self.bot = bot
        self.user = user
        self.farbe = farbe
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        if self.values[0] == "Premium":
            anzeige = """
> <:v_info:1119579853092552715> Spezielle Befehle und Funkt/helpionen, nur für Premium Nutzer.

__<:v_user:1119585450923929672> User Befehle__
</premium embedfarbe:1091635833217486939> Ändere die Farbe aller Embeds, die dir gesendet werden von Vulpo.
</premium rangkarte:1091635833217486939> Ändere das Bild deiner Rangkarte.

__<:v_ticket:1119584819597279242> Premium erhalten__
Es sind noch sehr viel mehr Funktionen in Premium enthalten. Du kannst alle Vorteile unter https://vulpo-bot.de/premium sehen.
Premium ist heiß begehrt. Du kannst es bekommen, indem du ein Abonnement wirst: https://vulpo-bot.de/premium."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            
            return await interaction.edit_original_response(embed=embed)
        if self.values[0] == "Stats":
            anzeige = """
> <:v_info:1119579853092552715> Vulpos Stats System basiert auf Tracking von Mitgliedern, wie aktiv sie in Text- und Sprachkanälen sind.

__<:v_user:1119585450923929672> User Befehle__
</stats user:1002985831713226833> Schau dir die Stats eines Users an.
</stats server:1002985831713226833> Schau dir die Stats des Servers an.

__<:v_einstellungen:1119578559086874636> Team Befehle__
</stats reset:1002985831713226833> Setze alle Stats auf 0 zurück."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.edit_original_response(embed=embed)
        if self.values[0] == "Auto Moderation":
            anzeige = """
> <:v_info:1119579853092552715> Dieses System ermöglicht dir automatische Handlungen gegen Nutzer, die eine bestimmte Warnanzahl erreicht haben. Warns können manuell und automatisch, über z.B.: Blacklist, verteilt werden.

__<:v_user:1119585450923929672> User Befehle__
Keine User Befehle.

__<:v_einstellungen:1119578559086874636> Team Befehle__
</warn:967681545190117423> Warne einen User.
</unwarn:967681545190117424> Entferne eine Warnung eines Users.
</listwarns:967681545190117425> Zeigt wie viele Warnungen ein User hat.

</modlog:967681544917495871> Richte einen Moderationlog ein.
</messagelog:967681544917495870> Richte einen MessageLog ein.

</automod addaction:970000987706232882> Füge eine Aktion für die Automatische Moderation hinzu.
</automod removeaction:970000987706232882> Entferne eine Aktion von der Automatischen Moderation.
</automod liste:970000987706232882> Lass dir alle Automod-Aktionen anzeigen.
</automod caps:970000987706232882> Füge einen Caps Filter hinzu.
</automod spam:970000987706232882> Füge einen Spam Filter hinzu.

</blacklist show:967681544917495877> Zeigt alle Wörter auf der Blacklist an.
</blacklist add:967681544917495877> Füge ein Wort der Blacklist hinzu.
</blacklist remove:967681544917495877> Entferne ein Wort von der Blacklist."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.edit_original_response(embed=embed)
        if self.values[0] == "Ticketsystem":
            anzeige = """
> <:v_info:1119579853092552715> Dieses Ticketsystem hat nur zwei Befehle. Cool oder? Alle Handlungen im Ticket werden durch Buttons gemanaged: öffnen, claimen, schließen, neu öffnen, löschen.

__<:v_user:1119585450923929672> User Befehle__
Keine User Befehle.

__<:v_einstellungen:1119578559086874636> Team Befehle__
</createpanel:967681545307570177> Erstelle ein Panel, womit User ein Ticket öffnen können.
</ticketlog:967681544917495872> Richte einen Ticketlog ein."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.edit_original_response(embed=embed)
        if self.values[0] == "Nachrichten":
            anzeige = """
> <:v_info:1119579853092552715> Die Kategorie Nachrichten beschreibt Befehle, mit denen du auf bestimmte Nachrichten reagieren kannst. Automatisch und manuell. z.B.: automatische Reaktionen

__<:v_user:1119585450923929672> User Befehle__
Keine User Befehle.

__<:v_einstellungen:1119578559086874636> Team Befehle__
</joinmsg:1223292369223549080> Lege eine Nachricht fest, wenn jemand joint.
</testjoin:1223292369223549079> Überprüfe die Join Nachricht.
</leavemsg:1223292369223549082> Lege eine Leave Nachricht fest.
</testleave:1223292369223549081> Überprüfe die Leave Nachricht.
</autoreact add:972922964829945856> Richte Auto Reaktionen in Channels ein.
</autoreact delete:972922964829945856> Entferne automatische Reaktionen von Kanälen.
</autoreact liste:972922964829945856> Lass dir alle automatischen Reaktionen anzeigen.
</embed:972456398166294538> Mache eine eine eingebettete Nachricht.
</tag add:970388955684016258> Erstelle einen Tag.
</tag delete:970388955684016258> Entferne einen Tag.
</tag liste:970388955684016258> Lass dir alle Tags anzeigen.
</reportlog:1027577595816050708> Lege einen Kanal fest für gemeldete Nachrichten von Usern.

Außerdem:
Jeder Nutzer kann die Custom Befehle des Tags System nutzen. Wenn erstmal ein Tag erstellt wurde kann jeder User ihn mit `!tag tagname` ausführen.

❓ Du suchst nach Stats? Sieh dir die Kategorie Stats an! ;)"""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.edit_original_response(embed=embed)
        if self.values[0] == "Information":
            anzeige = """
> <:v_info:1119579853092552715> Hier stehen Befehle, die hauptsächlich Informationen ausgeben oder nützlich sind.

__<:v_user:1119585450923929672> User Befehle__
</about:967681545307570178> Infos über Vulpo.
</help:972109932033892352> Alle wichtigen Links und Befehle.
</invite:967681545307570179> Link, um Vulpo einzuladen.
</support:967681545307570180> Zeigt einen Link für den Support-Server.
</vote:1011653776832213022> Zeigt an, wann du wieder für Vulpo voten kannst.
</info server:967681545013960767> Infos zum Server.
</servericon:967681545013960768> Zeigt das Server Profilbild.
</info member:967681545013960767> Infos zu einem Member.
</info rolle:967681545013960767> Infos zu einer Rolle.
</info kanal:967681545013960767> Infos zu einem Channel.
</permissions:967681545013960770> Listet alle Berechtigungen von jemandem auf.
</ping:967681545307570181>  Zeigt den Ping.
</umfrage:967681545013960766> Erstelle eine Umfrage.
</random:996395516910895125> Erhalte eine random Zahl von deinen ausgewählten Zahlen.
</translate:996795931099943044> Übersetze einen Text in mehrere Sprachen.
</bestenliste:1000783908071284846> Erhalte Bestenlisten verschiedenster Funktionen.
</invites:967681545013960764> Zeigt die Einladungen eines Users.

__<:v_einstellungen:1119578559086874636> Team Befehle__
Keine Team Befehle."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.edit_original_response(embed=embed)
        if self.values[0] == "Settings & Setup":
            anzeige = """
> <:v_info:1119579853092552715> Diese Kategorie bietet dir Einstellungen für deinen Server wie Joinrollen und Tags. Außerdem findest du dort nützliche Befehle für dich selbst.

__<:v_user:1119585450923929672> User Befehle__
</erinnerung erstellen:1002275443786911865> Erstelle dir eine Erinnerung für eine bestimmte Uhrzeit.
</erinnerung löschen:1002275443786911865> Entfernt eine Erinnerung.
</erinnerung anzeigen:1002275443786911865> Bekomme eine Liste von deinen Erinnerungen.
</afk:1010289696351465492> Setze dich AFK.
</starboard:1052926756853661827> - Lege einen Kanal fest für Nachrichten mit 5 Sternen von Usern.

__<:v_einstellungen:1119578559086874636> Team Befehle__
</joinrole:967681544917495868> Lege eine Joinrolle fest.
</botrole:967681544917495869> Lege eine Botrolle fest.
</voicesetup:967681545307570183> Erstelle einen "Join to Create" Kanal.
</reactionrole:967681545307570176> Erstelle Reaktionsrollen."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.edit_original_response(embed=embed)
        if self.values[0] == "Basic Moderation":
            anzeige = """
> <:v_info:1119579853092552715> Dies sind Befehle, die eigentlich jeder Bot hat. Einfache Moderation per Slash Befehle.

__<:v_user:1119585450923929672> User Befehle__
Keine User Befehle.

__<:v_einstellungen:1119578559086874636> Team Befehle__
</kick:967681545190117416> Kicke einen User.
</ban:967681545190117417> Banne einen User.
</unban:967681545190117419> Entbanne einen User.
</banlist:967681545190117420> Zeigt dir eine Liste, die Gebannt wurden.
</clear channel:967681545190117422> Lösche Nachrichten in einem Channel.
</clear between:967681545190117422> Lösche alle Nachrichten zwischen zwei Nachrichten eines Kanals.

❓ Du suchst nach Verwarnungs Befehlen? Guck mal in der Kategorie Auto Moderation nach! ;)"""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.edit_original_response(embed=embed)
        if self.values[0] == "Levelsystem":
            anzeige = """
> <:v_info:1119579853092552715> Das Levelsystem vonn Vulpo ist umfassend. Coole Rangnachrichten und viele Einstellungsmöglichkeiten für Moderatoren.

__<:v_user:1119585450923929672> User Befehle__
</rang:1223292369718349885> Zeigt dir welches Level du bist.

__<:v_einstellungen:1119578559086874636> Team Befehle__
</levelsystem status:1223292369223549083> Zeigt, ob das Levelystem aktiviert/deaktiviert ist.
</levelsystem role add:1223292369223549083> Setzte eine neue Levelrolle.
</levelsystem role delete:1223292369223549083> Entferne eine Levelrolle.
</levelsystem role list:1223292369223549083> Liste von allen Levelrollen in diesem Server.
</levelsystem levelupmessage:1223292369223549083> Richte eine Levelup Nachricht ein.
</levelsystem levelupkanal:1223292369223549083> Richte ein, in welchem Kanal die Levelup Nachricht geschickt werden soll.
</levelsystem block channel:1223292369223549083> Entferne einen Kanal vom Levelsystem
</levelsystem block rolle:1223292369223549083> Entferne eine Rolle vom Levelsystem
</setlevel:1223292369718349886> Setze einen User zu einem bestimmten Level.
</xpboost:1223292369718349887> Starte einen XP Boost auf deinem Server."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.edit_original_response(embed=embed)
        if self.values[0] == "Giveaway":
            anzeige = """
> <:v_info:1119579853092552715> Hinter dem Giveaway System steckt mehr als du denkst. Nicht nur Starten und blacklist, bypassrollen und verwalten. Die Gewinnspiele enden sogar nicht bei Bot Neustart, sondern laufen normal bis zum Ende weiter.
> Man kann ebenso Anforderungen einstellen. Hinter denen steckt noch die ganze Magie. Das Stats System ist mit verknüpft bei Nachrichten. Außerdem ist das Levelsystem mit vernetzt bei Levelanforderungen. Buttons gibt es auch.

__<:v_user:1119585450923929672> User Befehle__
Keine User Befehle.

__<:v_einstellungen:1119578559086874636> Team Befehle__
</gewinnspiel starten:1000350325804388382> Starte ein neues Gewinnspiel.
</gewinnspiel verwalten:1000350325804388382> Verwalte Gewinnspiele. 
</gewinnspiel bypassrolle:1000350325804388382> Bearbeite Rollen, die die Bedingungen umgehen. 
</gewinnspiel blockieren:1000350325804388382> Setze Member und Rollen auf die Blacklist."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.edit_original_response(embed=embed)
        if self.values[0] == "Fun":
            anzeige = """
> <:v_info:1119579853092552715> Schon lange nicht mehr gelacht xD? Dann wird es mal Zeit. Denn mit diesen Befehlen wirst du zu 99% lachen!

__<:v_user:1119585450923929672> User Befehle__
</ask:967681544762294293> Frage eine berühmte Person eine Frage
</avatar:967681545013960765> Zeigt das Profilbild eines Users an
</animal:1124745277471993957> Schicke ein zufälliges Bild eines bestimmten Tieres.
</emojiurl:1223304030202237058> Bekomme das URL eines filename
</games:967681544762294296> Zeigt alle Spiele an, die grade gespielt werden
</iq:967681544762294292> Zeigt das IQ von einem User an.
</lostrate:967681544674230292> Zeigt wie lost ein User ist.
</los:967681544762294295> Ziehe ein Ticket und reibe es auf, indem du auf die schwarzen Blöcke tippst.
</love:967681544762294294> Finde heraus wie verliebt zwei User sind
</meme:977874383261564972> Bekomme ein zufälliges Meme.
</password:967681544762294297> Generiert ein zufälliges Passwort für dich.
</pix:977874382804369472> Verpixelt ein Profilbild eines Users.
</tictactoe start:972881753570152538> Spiele mit jemanden tictactoe.
</tictactoe stats:972881753570152538> Spiele tictacoe mit jemanden und sieh dir deine Tik Tak Toe Stats an.
</wanted:1103348883293216911> Erstellt ein "Gesucht" Plakat mit dem Profilbild eines Users.
</wetter:967681545013960769> Zeigt das Wetter eines bestimmten Orts.
</stealemoji:967681545013960772> Stiehlt ein emoji von einem Server.

__<:v_einstellungen:1119578559086874636> Team Befehle__
Keine Team Befehle."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.edit_original_response(embed=embed)
        if self.values[0] == "Minispiele":
            anzeige = """
> <:v_info:1119579853092552715> Du langweilst dich? Dann probier mal diese Spiele aus. Sie werden dir die Langeweile vertreiben!

__<:v_user:1119585450923929672> User Befehle__
</speedgame profil:1052926756853661828> Zeigt deine Bestzeit
</speedgame start:1052926756853661828> Teste deine Schnelligkeit und steige im Rang auf

__<:v_einstellungen:1119578559086874636> Team Befehle__
</emojiquiz:1223304030202237058> Verwalte das Emojiquiz deines Servers.
</counting set:967681545307570184> Richte den Zählkanal ein.
</counting zahl:967681545307570184> Stelle die aktuelle Zahl des Counting Kanals ein.
</counting disable:967681545307570184> Deaktiviere das Minispiel.
</guessthenumber:999645444684644352> Verwalte das Minispiel 'Guess the number' auf deinem Server."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.edit_original_response(embed=embed)
        if self.values[0] == "Economy":
            anzeige = """
> <:v_info:1119579853092552715> Das globale Wirtschaftssystem von Vulpo bietet viel Spaß und Strategie. Messe dich mit anderen und steige in der Berufsleiter nach oben auf!

__<:v_user:1119585450923929672> User Befehle__
</cookies anzeigen:1040642429860184126> Öffne das Profil eines Users.
</cookies abheben:1040642429860184126> Hebe Geld von der Bank ab.
</cookies einzahlen:1040642429860184126> Überweise Geld auf die Bank.

</daily:1040642429860184128> Hole tägliche Cookies ab.
</work:1040642429860184129> Gehe Arbeiten.
</beg:1040642429860184127> Bettle für Münzen.
</send:1040642429860184130> Gebe einem User Cookies.
</rob:1040642429860184131> Raube einen User aus.
</rps:1040642429860184133> Spiele Schere, Stein, Papier um Cookies.
</slot:1040642429860184132> Spiele Casino.

**Job System**
</job apply:1040642429860184134> Bewerbe dich für einen Job.
</job quit:1040642429860184134> Verlasse deinen Job.
</job list:1040642429860184134> Zeigt dir eine Liste aller Jobs.


**Shop System**
</shop anzeigen:1040642429860184135> Zeigt dir alle Items im Shop.
</shop item kaufen:1040642429860184135> Kaufe ein Item aus dem Shop.
</shop item verkaufen:1040642429860184135> Verkaufe ein Item aus deinem Rucksack. Du bekommst zufällige Prozente des Kaufpreises wieder. Prozente im Bereich von 65% bis 115%
</shop item meine:1040642429860184135> Zeigt alle deine gekauften Items vom Shop.

__<:v_einstellungen:1119578559086874636> Team Befehle__
**Shop System**
</shop item hinzufügen:1040642429860184135> Füge ein Item dem Shop hinzu.
</shop item entfernen:1040642429860184135> Entferne ein Item aus dem Shop."""
            embed = discord.Embed(colour=self.farbe, description=anzeige)
            
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
            return await interaction.edit_original_response(embed=embed)

class DropdownView(discord.ui.View):
    def __init__(self, user, farbe, bot):
        super().__init__(timeout=None)
        self.add_item(Dropdown(user, farbe, bot))
        
        website = discord.ui.Button(label='Zur Website', style=discord.ButtonStyle.url, url='https://vulpo-bot.de/')
        
        self.add_item(website)

class vulpo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.t1 = math.floor(datetime.now().timestamp())
        self.t2 = datetime.fromtimestamp(int(self.t1))
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(DropdownView(None, None, self.bot))

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def help(self, interaction: discord.Interaction):
        """Wichtige Links wie invite, support, vote und viele andere Infos."""
        await interaction.response.defer(ephemeral=True)
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
<:v_info:1119579853092552715> Erhalte Support hier: https://vulpo-bot.de/ticketsystem
<:v_info:1119579853092552715> Benachrichtigungen von Youtube: `/benachrichtigung youtube`

**Links**
[Einladen](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands) **|** [Support](https://discord.gg/49jD3VXksp) **|** [Voten](https://top.gg/bot/925799559576322078/vote)
""", color=farbe)
        
        embed.set_author(name="Vulpo", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549")
        embed.set_thumbnail(url=interaction.guild.icon)
        await interaction.followup.send(embed=embed, view=DropdownView(interaction.user, farbe, self.bot), ephemeral=True)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def vote(self, interaction: discord.Interaction):
        """Zeigt an, wann du wieder für Vulpo voten kannst."""
                
        result = await getMongoDataBase()["vote"].find_one({"userid": interaction.user.id})
        
        if result == None:
            embed = discord.Embed(title="Du kannst voten", url="https://top.gg/bot/925799559576322078/vote", description="""
<:v_info:1119579853092552715> Der Vote-Cooldown von 12 Stunden ist abgelaufen. Es wäre sehr schön, wenn du wieder für mich votest.

<:herz:941398727501955113> Als Belohnung für einen weiteren Vote bekommst du **300 🍪 im Economy System** und eine besondere **Rolle in [Vulpos Wald](https://discord.gg/49jD3VXksp)**""", colour=await getcolour(self, interaction.user))
            embed.set_footer(text="Danke für deine Unterstützung", icon_url="https://media.discordapp.net/attachments/965302660871884840/965315155816767548/Vulpo_neu.png?width=1572&height=1572")
            return await interaction.followup.send(embed=embed)
        t1 = int(result["timestamp"])
        t2 = datetime.fromtimestamp(int(t1))
        embed = discord.Embed(title="Du kannst noch nicht voten", url="https://top.gg/bot/925799559576322078/vote", description=f"""
<:v_info:1119579853092552715> Der Vote-Cooldown von 12 Stunden ist noch nicht abgelaufen. Du kannst wieder {discord_timestamp(t2, "R")} voten.

<:herz:941398727501955113> Als Belohnung für einen weiteren Vote bekommst du **300 🍪 im Economy System** und eine besondere **Rolle in [Vulpos Wald](https://discord.gg/49jD3VXksp)**""", colour=await getcolour(self, interaction.user))
        embed.set_footer(text="Danke für deine Unterstützung", icon_url="https://media.discordapp.net/attachments/965302660871884840/965315155816767548/Vulpo_neu.png?width=1572&height=1572")
        await interaction.followup.send(embed=embed)
        
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def about(self, interaction: discord.Interaction):
        """Zeigt Infos über mich."""
        
        await interaction.response.defer()
        
        bot = self.bot.user
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
        
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def invite(self, interaction: discord.Interaction):
        """Zeigt einen Link um mich einzuladen."""
        
        await interaction.response.defer()
        
        embed = discord.Embed(colour=await getcolour(self, interaction.user), title=f"Vulpo auf anderen Servern verwenden", description=f"Du kannst Vulpo mit [diesem Link](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands) zu deinem Server hinzufügen.", url="https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands")
        
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def support(self, interaction: discord.Interaction):
        """Zeigt einen Link für den Support-Server."""
        
        await interaction.response.defer()
        
        embed = discord.Embed(colour=await getcolour(self, interaction.user), title=f"Bekomme Hilfe", description=f"Wenn du Hilfe benötigst, kannst du meinem Supportserver über [diesen Link](https://discord.gg/49jD3VXksp) beitreten.\nFalls du ein Ticket eröffnen möchtest kannst du das [auf dieser Webseite](https://vulpo-bot.de/ticketsystem) tun.")
        
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def ping(self, interaction: discord.Interaction):
        """Zeigt den Ping von den verschiedensten Funktionen."""
        
        await interaction.response.defer()
        
        #db
        t_1 = time.perf_counter()
        
        await getMongoDataBase()["levelsystem"].find_one({"client_id": 925729625580113951})

        t_2 = time.perf_counter()
        time_delta1 = round((t_2 - t_1) * 1000)

        bot = round(self.bot.latency * 1000)
        embed = discord.Embed(title="Internetgeschwindigkeit", description=f"```Bot: {bot} ms\nDatenbank: {time_delta1} ms```", color=await getcolour(self, interaction.user))
        
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        
        t_3 = time.perf_counter()
        await interaction.followup.send(embed=embed)

        #Answer
        t_4 = time.perf_counter()
        time_delta2 = round((t_4 - t_3) * 1000)
        embed = discord.Embed(title="Internetgeschwindigkeit", description=f"```Bot: {bot} ms\nDatenbank: {time_delta1} ms\nDiscord-Api: {time_delta2} ms```", color=await getcolour(self, interaction.user))
        
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.edit_original_response(embed=embed)

async def setup(bot):
    await bot.add_cog(vulpo(bot))