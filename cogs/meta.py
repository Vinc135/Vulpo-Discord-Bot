import datetime
import math
import discord
from discord.ext import commands
import typing
import aiohttp
from discord import app_commands
import re
import random
from googletrans import Translator
from utils.utils import discord_timestamp
from utils.utils import getcolour, getLevelSystemEnabled
from utils.MongoDB import getMongoDataBase

# with open("training_data.csv", "rb") as file:
#     response = openai.Dataset.create(
#         file=file,
#         name="my_training_data",
#         description="A dataset of training data for my GPT-3 model",
#     )
class EmbedMaker(discord.ui.Modal, title="Embed-Maker"):
    def __init__(self, farbe: str, titel: str):
        super().__init__(custom_id="133Xhh91RXHXhP9hRXP9XR")
        self.farbe = farbe
        self.titel = titel
    kopfzeile = discord.ui.TextInput(label="Kopfzeile", style=discord.TextStyle.short, required=False, placeholder="Schreib hier rein, was in der Kopfzeile des Embeds stehen soll.")
    beschreibung = discord.ui.TextInput(label="Beschreibung", style=discord.TextStyle.paragraph, required=True, placeholder="Schreib hier rein, was in der Beschreibung des Embeds stehen soll.")
    fußzeile = discord.ui.TextInput(label="Fußzeile", style=discord.TextStyle.short, required=False, placeholder="Schreib hier rein, was in der Beschreibung des Embeds stehen soll.")
    thumbnail = discord.ui.TextInput(label="Thumbnail", style=discord.TextStyle.short, required=False, placeholder="Schreibe den Link des Bildes für das Thumbnail hier rein.")
    image = discord.ui.TextInput(label="Image", style=discord.TextStyle.short, required=False, placeholder="Schreibe den Link des Bildes für das Image hier rein.")

    async def on_submit(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title=self.titel, description=self.beschreibung.value)
            if self.farbe == "Gelb":
                embed.color = discord.Color.gold()
            if self.farbe == "Orange":
                embed.color = discord.Color.orange()
            if self.farbe == "Rot":
                embed.color = discord.Color.red()
            if self.farbe == "Grün":
                embed.color = discord.Color.green()
            if self.farbe == "Blau":
                embed.color = discord.Color.blue()
            if self.kopfzeile.value != None:
                embed.set_author(name=self.kopfzeile.value)
            if self.fußzeile.value != None:
                embed.set_footer(text=self.fußzeile.value)
            if self.thumbnail.value != None:
                embed.set_thumbnail(url=self.thumbnail.value)
            if self.image.value != None:
                embed.set_image(url=self.image.value)
            await interaction.channel.send(embed=embed)
            await interaction.followup.send("**<:v_checkmark:1264271011818242159> Das Embed wurde erfolgreich erstellt und gesendet.**", ephemeral=True)
        except:
            await interaction.followup.send("**<:v_x:1264270921452224562> Etwas mit deinen Angaben stimmt nicht überein. Bitte versuche es erneut.**", ephemeral=True)

class meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "b490a86c0b800ef278846f71592953f4"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def embed(self, interaction: discord.Interaction, titel: str, farbe: typing.Literal["Gelb","Orange","Rot","Grün","Blau"]):
        """Erstelle ein vollständiges Custom-Embed."""
        await interaction.response.send_modal(EmbedMaker(farbe, titel))

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def invites(self, interaction: discord.Interaction, member: discord.Member=None):
        """Finde heraus wieveiele Leute du schon eingeladen hast."""
        if member == None:
            member = interaction.user
        totalInvites = 0
        for invite in await interaction.guild.invites():
            if invite.inviter == member:
                totalInvites += invite.uses
        
        embed=discord.Embed(description=f"Das Mitglied {member.mention} hat insgesamt __**{totalInvites} Mitglied{'er' if totalInvites >= 2 else ''}**__ zum Server eingeladen!", color=await getcolour(self, interaction.user))
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_footer(text="Diese Zahl basiert auf allen Invites, seitdem du auf dem Server bist.", icon_url="https://cdn.discordapp.com/filename/814202875387183145.png")

        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        """Zeigt das Profilbild eines Benutzers an."""
        await interaction.response.defer()
        if member is None:
            member = interaction.user
        embed = discord.Embed(colour=await getcolour(self, interaction.user), description=f"Profilbild und Banner (wenn existent) von {member.mention}")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar or None)
        
        user = await self.bot.fetch_user(member.id)
        if user.banner:
            embed.set_image(url=user.banner)
            embed.set_thumbnail(url=member.avatar or None)
        else:
            embed.set_image(url=member.avatar or None)
        
                
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def umfrage(self, interaction: discord.Interaction, frage: str, antworten: str):
        """Beispiel: /umfrage Testfrage <Antwort Nummer 1> <Hier die zweite Antwort>. Maximale Antworten: 9"""
        await interaction.response.defer()
        a = 0
        desc = ""
        pattern = "<.*?>"
        for match in re.finditer(pattern, antworten):
            answer = match.group(0).replace("<","").replace(">","")
            a += 1
            c = ""
            if a == 1:
                c += "one"
            if a == 2:
                c += "two"
            if a == 3:
                c += "three"
            if a == 4:
                c += "four"
            if a == 5:
                c += "five"
            if a == 6:
                c += "six"
            if a == 7:
                c += "seven"
            if a == 8:
                c += "eight"
            if a == 9:
                c += "nine"
            if a == 10:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Du kannst nur maximal neun Antwortmöglichkeiten geben.**", ephemeral=True)
            desc += f":{c}: - {answer}\n"
        embed = discord.Embed(color=await getcolour(self, interaction.user), title=frage, description=desc)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
        embed.set_footer(text="Entscheide dich nur für eins!")
        message = await interaction.channel.send("**Neue Umfrage!**", embed=embed)
        if a == 1:
            await message.add_reaction("1️⃣")
        if a == 2:
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
        if a == 3:
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
        if a == 4:
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            await message.add_reaction("4️⃣")
        if a == 5:
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            await message.add_reaction("4️⃣")
            await message.add_reaction("5️⃣")
        if a == 6:
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            await message.add_reaction("4️⃣")
            await message.add_reaction("5️⃣")
            await message.add_reaction("6️⃣")
        if a == 7:
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            await message.add_reaction("4️⃣")
            await message.add_reaction("5️⃣")
            await message.add_reaction("6️⃣")
            await message.add_reaction("7️⃣")
        if a == 8:
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            await message.add_reaction("4️⃣")
            await message.add_reaction("5️⃣")
            await message.add_reaction("6️⃣")
            await message.add_reaction("7️⃣")
            await message.add_reaction("8️⃣")
        if a == 9:
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            await message.add_reaction("4️⃣")
            await message.add_reaction("5️⃣")
            await message.add_reaction("6️⃣")
            await message.add_reaction("7️⃣")
            await message.add_reaction("8️⃣")
            await message.add_reaction("9️⃣")

        await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Umfrage wurde geschickt.**", ephemeral=True)

    info = app_commands.Group(name='info', description='Bekomme Infos zu bestimmten Usern, Rollen und Kanälen.', guild_only=True)

    @info.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def kanal(self, interaction: discord.Interaction, textkanal: discord.TextChannel=None, sprachkanal: discord.VoiceChannel=None):
        """Zeigt viele Informationen von einem Kanal an."""
        await interaction.response.defer()
        if textkanal != None and sprachkanal == None:
            channel = textkanal
            t1 = math.floor(channel.created_at.timestamp())
            t2 = datetime.datetime.fromtimestamp(int(t1))
            embed = discord.Embed(colour=await getcolour(self, interaction.user))
            embed.add_field(name=f"🆔 ID", value=f"{channel.id}", inline=False)
            embed.add_field(name="⚙️ Erstellt", value=f"Der Kanal wurde {discord_timestamp(t2, 'R')} erstellt.",
                            inline=False)
            if channel.category:
                embed.add_field(name="🗂 Kategorie",
                                value=f"{channel.category.name if channel.category.name else 'Keine Kategorie'}",
                                inline=False)
            embed.add_field(name="🖌 Beschreibung", value=f"{channel.topic if channel.topic else 'Keine Beschreibung'}",
                            inline=False)
            embed.add_field(name="🔢 Position", value=f"{channel.position}",
                            inline=False)
            embed.set_author(name=f"Kanal info {channel.name}")
            
            await interaction.followup.send(embed=embed)
            return
        if textkanal == None and sprachkanal != None:
            channel = sprachkanal
            t1 = math.floor(channel.created_at.timestamp())
            t2 = datetime.datetime.fromtimestamp(int(t1))
            embed = discord.Embed(colour=await getcolour(self, interaction.user))
            embed.add_field(name=f"🆔 ID", value=f"{channel.id}", inline=False)
            embed.add_field(name="⏱️ Erstellt", value=f"Der Kanal wurde {discord_timestamp(t2, 'R')} erstellt.", inline=False)
            embed.add_field(name="🗂 Kategorie",
                            value=f"{channel.category.name if channel.category.name else 'Keine Kategorie'}",
                            inline=False)
            embed.add_field(name=f"📊 Limit", value=f"{channel.user_limit}", inline=False)
            embed.add_field(name=f"🔊 Bitrate", value=f"{channel.bitrate/1000} kbps", inline=False)
            embed.set_author(name=f"Kanal info {channel.name}")
            
            await interaction.followup.send(embed=embed)
            return
        else:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Eine Kanalangabe ist erforderlich.**", ephemeral=True)
    
    @info.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def member(self, interaction: discord.Interaction, member: discord.Member=None):
        """Zeigt viele Informationen von einem Benutzer an."""
        await interaction.response.defer()
        if member == None:
            member = interaction.user
        t1 = math.floor(member.created_at.timestamp())
        t2 = datetime.datetime.fromtimestamp(int(t1))
        t3 = math.floor(member.joined_at.timestamp())
        t4= datetime.datetime.fromtimestamp(int(t3))
        embed = discord.Embed(colour=await getcolour(self, interaction.user), description=f"Der Account wurde {discord_timestamp(t2, 'R')} erstellt.")
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Beitritt", value=f"Der User ist {discord_timestamp(t4, 'R')} dem Server beigetreten.", inline=True)
        embed.add_field(name="Bot?", value='Ja' if member.bot else 'Nein', inline=False)
        embed.add_field(name="Höchste Rolle", value=member.top_role.mention, inline=True)
        
        if member.public_flags:
            flags = ""
            for flag in member.public_flags:
                if flag[1] == True:
                    if flag[0] == "staff":
                        flags += "<:v_discordstaff:1037069155008000042> "
                    if flag[0] == "partner":
                        flags += "<:v_discordpartner:1037069463532601404> "
                    if flag[0] == "bug_hunter":
                        flags += "<:v_bughunter:1037069367483060244> "
                    if flag[0] == "hypesquad_bravery":
                        flags += "<:v_bravery:1037069608127037500> "
                    if flag[0] == "hypesquad_brilliance":
                        flags += "<:brilliance:1037069659708600435> "
                    if flag[0] == "hypesquad_balance":
                        flags += "<:v_balance:1037069709318819950> "
                    if flag[0] == "early_supporter":
                        flags += "<:v_supporter:1037069787043483678> "
                    if flag[0] == "bug_hunter_level_2":
                        flags += "<:v_bughuntergold:1037069871286059058> "
                    if flag[0] == "verified_bot":
                        flags += "<:v_verifiedbot:1037069972226179182> "
                    if flag[0] == "verified_bot_developer":
                        flags += "<:v_verifiedbotdeveloper:1037070049539788851>"
                    if flag[0] == "discord_certified_moderator":
                        flags += "<:v_168:1264268507193806900>"
            if flags != "":
                embed.add_field(name="🎖 Abzeichen", value=flags, inline=False)

        liste = ""
        m = interaction.guild.get_member(member.id)
        for a in m.activities:
            if a.name not in liste:
                if liste == "":
                    liste += f"{a.name}"
                else:
                    liste += f", {a.name}"
        if liste != "":
            embed.add_field(name="🎮 Aktivitäten", value=liste, inline=False)
        user = await self.bot.fetch_user(member.id)
        if user.banner:
            embed.set_image(url=user.banner)
        embed.set_author(name=f"Userinfo {member}", icon_url=member.avatar)
        await interaction.followup.send(embed=embed)
    
    @info.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def server(self, interaction: discord.Interaction):
        """Zeigt viele Informationen von einem Server an."""
        await interaction.response.defer()
        t1 = math.floor(interaction.guild.created_at.timestamp())
        t2 = datetime.datetime.fromtimestamp(int(t1))
        embed = discord.Embed(colour=await getcolour(self, interaction.user), description=f"Der Server wurde {discord_timestamp(t2, 'R')} erstellt.")
        embed.add_field(name="ID", value=str(interaction.guild.id), inline=True)
        embed.add_field(name="Owner", value=interaction.guild.owner, inline=True)
        if interaction.guild.description:
            embed.add_field(name="Beschreibung", value=interaction.guild.description, inline=False)

        online = 0
        for member in interaction.guild.members:
            if member.status.name == "online":
                online += 1
        embed.add_field(name="Mitglieder", value=f"<:v_statusonline:1037071233902182491> {online} Online **|** <:v_statusoffline:1037071732474921080> {interaction.guild.member_count} Mitglieder", inline=False)
        embed.add_field(name="Kanäle", value=f"<:v_31:1264264994774585445> {len(interaction.guild.text_channels)} Textkanäle **|** <:v_3:1264264503810592778> {len(interaction.guild.voice_channels)} Sprachkanäle", inline=False)
        
        bans = [ban async for ban in interaction.guild.bans()]
        embed.add_field(name="Gebannte User", value=f"<:v_168:1264268507193806900> {len(bans)}", inline=False)
        embed.add_field(name="Boost Status", value=f"<:v_101:1264266606293291130> {interaction.guild.premium_subscription_count if interaction.guild.premium_subscription_count else 'Keine'} Booster (Level {interaction.guild.premium_tier})", inline=False)
        if interaction.guild.features:
            funktionen = ""
            for funktion in interaction.guild.features:
                if funktion == "ANIMATED_BANNER":
                    if funktionen == "":
                        funktionen += "Animiertes Serverbanner"
                    else:
                        funktionen += ", Animiertes Serverbanner"
                if funktion == "ANIMATED_ICON":
                    if funktionen == "":
                        funktionen += "Animiertes Servericon"
                    else:
                        funktionen += ", Animiertes Servericon"
                if funktion == "BANNER":
                    if funktionen == "":
                        funktionen += "Serverbanner"
                    else:
                        funktionen += ", Serverbanner"
                if funktion == "COMMERCE":
                    if funktionen == "":
                        funktionen += "Verkauf"
                    else:
                        funktionen += ", Verkauf"
                if funktion == "COMMUNITY":
                    if funktionen == "":
                        funktionen += "Community Server"
                    else:
                        funktionen += ", Community Server"
                if funktion == "DISCOVERABLE":
                    if funktionen == "":
                        funktionen += "Discord's Discovery Programm"
                    else:
                        funktionen += ", Discord's Discovery Programm"
                if funktion == "MEMBER_VERIFICATION_GATE_ENABLED":
                    if funktionen == "":
                        funktionen += "Verifikationsbildschirm"
                    else:
                        funktionen += ", Verifikationsbildschirm"
                if funktion == "MORE_EMOJI":
                    if funktionen == "":
                        funktionen += "Mehr Emoji Slots"
                    else:
                        funktionen += ", Mehr Emoji Slots"
                if funktion == "MORE_STICKERS":
                    if funktionen == "":
                        funktionen += "Mehr Sticker Slots"
                    else:
                        funktionen += ", Mehr Sticker Slots"
                if funktion == "NEWS":
                    if funktionen == "":
                        funktionen += "News Kanäle"
                    else:
                        funktionen += ", News Kanäle"
                if funktion == "PARTNERED":
                    if funktionen == "":
                        funktionen += "Partner"
                    else:
                        funktionen += ", Partner"
                if funktion == "PREVIEW_ENABLED":
                    if funktionen == "":
                        funktionen += "Vorschau aktiviert"
                    else:
                        funktionen += ", Vorschau aktiviert"
                if funktion == "PRIVATE_THREADS":
                    if funktionen == "":
                        funktionen += "Private Threads"
                    else:
                        funktionen += ", Private Threads"
                if funktion == "ROLE_ICONS":
                    if funktionen == "":
                        funktionen += "Rollen Icons"
                    else:
                        funktionen += ", Rollen Icons"
                if funktion == "VANITY_URL":
                    if funktionen == "":
                        funktionen += "Vanity Url"
                    else:
                        funktionen += ", Vanity Url"
                if funktion == "VERIFIED":
                    if funktionen == "":
                        funktionen += "Verifizierter Server"
                    else:
                        funktionen += ", Verifizierter Server"
                if funktion == "VIP_REGIONS":
                    if funktionen == "":
                        funktionen += "Vip Regionen"
                    else:
                        funktionen += ", Vip Regionen"
                if funktion == "WELCOME_SCREEN_ENABLED":
                    if funktionen == "":
                        funktionen += "Willkommensbildschirm"
                    else:
                        funktionen += ", Willkommensbildschirm"
            embed.add_field(name="🎛 Server Funktionen", value=funktionen, inline=False)
        if interaction.guild.banner:
            embed.set_image(url=interaction.guild.banner)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_author(name=f"Serverinfo {interaction.guild.name}", icon_url=interaction.guild.icon)
        
        await interaction.followup.send(embed=embed)
    
    @info.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def rolle(self, interaction: discord.Interaction, rolle: discord.Role):
        """Sendet eine Rolleninfo."""
        await interaction.response.defer()
        guild = interaction.guild
        t1 = math.floor(rolle.created_at.timestamp())
        t2 = datetime.datetime.fromtimestamp(int(t1))
        embed = discord.Embed(color=await getcolour(self, interaction.user), description=f"ℹ️ Rollen info für {rolle.name}")
        embed.add_field(name=f"🆔 ID", value=f"{rolle.id}", inline=False)
        embed.add_field(name="⏱ Erstellt", value=f"Die Rolle wurde {discord_timestamp(t2, 'R')} erstellt.",inline=False)
        a = rolle.color.value
        embed.add_field(name="🖌 Farbcode (HEX)", value=f'#{a:x}', inline=False)
        embed.add_field(name="👥 Benutzer mit der Rolle",
                        value=f"{len(rolle.members)} von {guild.member_count} Mitgliedern", inline=False)
        embed.set_author(name=f"Rolleninfo {rolle.name}")
        
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def servericon(self, interaction: discord.Interaction):
        """Zeigt das Profilbild vom Server an."""
        await interaction.response.defer()
        guild = interaction.user.guild
        embed = discord.Embed(colour=await getcolour(self, interaction.user), description=f"Serverbild von {guild.name}")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_image(url=guild.icon)
        
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def wetter(self, interaction: discord.Interaction, stadt: str=None):
        """Zeigt das Wetter einer Stadt an."""
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        f"https://api.openweathermap.org/data/2.5/weather?appid=bf254c2299576dc022583728cfaf7971&q=" + stadt.replace(
                            " ", "+")) as r:
                    data = await r.json()
                    icon = data['weather'][0]['icon']
                    embed = discord.Embed(colour=await getcolour(self, interaction.user), title=f"Weather",
                                            description=f"Mal gucken...")
                    embed.add_field(name=f"🗽 Location", value=f"{data['name']}")
                    embed.add_field(name=f"☁️ Wetter", value=f"{data['weather'][0]['main']} - {data['weather'][0]['description']}", inline=False)
                    embed.add_field(name=f"🔥 Temperatur", value=f"{int((float(data['main']['temp']))) - 273}°C")
                    embed.add_field(name=f"👆 Fühlt sich an wie", value=f"{int((float(data['main']['feels_like']))) - 273}°C")
                    embed.add_field(name=f"💧 Luftfeuchtigkeit", value=f"{int((float(data['main']['humidity'])))}%", inline=False)
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{icon}@2x.png")
                    
                    await interaction.followup.send(embed=embed)
        except:
            embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                    description=f"Stadt **{stadt}** nicht gefunden")
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            
            await interaction.followup.send(embed=embed)
            return

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def permissions(self, interaction: discord.Interaction, user: discord.Member=None):
        """Listet alle Berechtigungen von jemandem auf."""
        await interaction.response.defer()
        if user is None:
            permissions = interaction.channel.permissions_for(interaction.user)
            user = interaction.user
        permissions = interaction.channel.permissions_for(user)
        embed = discord.Embed(title=f':customs:  Berechtigungen von {user}', color=await getcolour(self, interaction.user))
        
        embed.add_field(name='Server', value=f"<:v_12:1264264683427336259> {interaction.guild.name}")
        embed.add_field(name='Kanal', value=f"<:v_31:1264264994774585445> {interaction.channel.name}", inline=False)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        
        embed2 = discord.Embed(color=await getcolour(self, interaction.user))
        

        permissionsCount = 0

        for item, valueBool in permissions:
            
            if valueBool == True:
                value = '<:v_checkmark:1264271011818242159>'
            else:
                value = '<:v_x:1264270921452224562>'
            if(permissionsCount < 23):
                embed.add_field(name=item, value=value)
            elif(permissionsCount <= 23*2):
                embed2.add_field(name=item, value=value)

            permissionsCount += 1

        await interaction.followup.send(embeds=[embed, embed2])

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def emojiurl(self, interaction: discord.Interaction, emoji: str):
        """Gibt den Link für ein Emoji."""
        try:
            await interaction.response.defer()
            emoj = discord.PartialEmoji.from_str(emoji)
            if emoj is None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Der Emoji wurde nicht gefunden. Stelle sicher dass dieses Emoji auf einem Server ist, auf dem ich auch in und dass du das Format eingehalten hast:\n`Für normale filename: name:id oder für Animierte: a:name:id`**", ephemeral=True)
            embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                description=f"Hier der Link: {emoj.url}")
            
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            embed.set_image(url=f"{emoj.url}")
            await interaction.followup.send(embed=embed)
        except:
            return await interaction.followup.send(content="**<:v_x:1264270921452224562> Der Emoji wurde nicht gefunden. Stelle sicher dass dieses Emoji auf einem Server ist, auf dem ich auch in und dass du das Format eingehalten hast:\n`Für normale filename: name:id oder für Animierte: a:name:id`**", ephemeral=True)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_emojis_and_stickers=True)
    async def stealemoji(self, interaction: discord.Interaction, emoji: str, name: str):
        """Erstelle das selbe Emoji, wie es ein anderer Server hat, für deinen Server."""
        await interaction.response.defer()
        try:
            emoj = discord.PartialEmoji.from_str(emoji)
            if emoj is None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Der Emoji wurde nicht gefunden. Stelle sicher dass dieses Emoji auf einem Server ist, auf dem ich auch bin und dass du das Format eingehalten hast:\n`Für normale filename: name:id oder für Animierte: a:name:id`**", ephemeral=True)
            async with aiohttp.ClientSession() as session:
                async with session.get(emoj.url) as response:
                    image_bytes = await response.read()
                    emo = await interaction.guild.create_custom_emoji(name=name, image=image_bytes, reason="stealemoji command")
        except:
            return await interaction.followup.send(content="**<:v_x:1264270921452224562> Der Emoji wurde nicht gefunden. Stelle sicher dass dieses Emoji auf einem Server ist, auf dem ich auch bin und dass du das Format eingehalten hast:\n`Für normale filename: name:id oder für Animierte: a:name:id`**", ephemeral=True)
        embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                description=f"**Der Emoji {emo} wurde erstellt.**\nName: {name}")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_image(url=f"{emoj.url}")
        
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def random(self, interaction: discord.Interaction, erstezahl: int, zweitezahl: int):
        """Erhalte eine random Zahl von deinen ausgewählten Zahlen."""
        await interaction.response.defer()
        drittezahl = random.randint(erstezahl, zweitezahl)
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Deine zufällige Zahl zwischen `{erstezahl}` und `{zweitezahl}` ist `{drittezahl}`.**")
        
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def translate(self, interaction: discord.Interaction, sprache: typing.Literal["Arabisch", "Chinesisch", "Deutsch", "Englisch", "Französisch", "Hindi", "Italienisch", "Japanisch", "Portugiesisch", "Russisch", "Spanisch", "Türkisch"], text: str):
        """Übersetze einen Text in mehrere Sprachen."""
        await interaction.response.defer()
        lang = ""
        if sprache == "Deutsch":
            lang += "de"
        if sprache == "Englisch":
            lang += "en"
        if sprache == "Italienisch":
            lang += "it"
        if sprache == "Türkisch":
            lang += "tr"
        if sprache == "Chinesisch":
            lang += "zh-CN"
        if sprache == "Spanisch":
            lang += "es"
        if sprache == "Arabisch":
            lang += "ar"
        if sprache == "Portugiesisch":
            lang += "pt"
        if sprache == "Französisch":
            lang += "fr"
        if sprache == "Russisch":
            lang += "ru"
        if sprache == "Hindi":
            lang += "hi"
        if sprache == "Japanisch":
            lang += "ja"
        translator = Translator()
        translation = translator.translate(text, dest=lang)
        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Übersetzer")
        embed.add_field(name="Vorher", value=translation.origin)
        embed.add_field(name="Nachher", value=translation.text)
        embed.set_thumbnail(url=interaction.user.avatar)
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
    async def bestenliste(self, interaction: discord.Interaction, system: typing.Literal["Economy", "Emojiquiz", "Flaggenquiz", "Levelsystem", "TicTacToe", "Speedgame", "Votes"]):
        """Bekomme Bestenlisten verschiedenster Funktionen."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        if system == "Economy":
            leaderboard = await db["economy"].find().sort([("bank", -1)]).to_list(length=10)
            embed = discord.Embed(title="Bestenliste (Economy)", color=await getcolour(self, interaction.user))
            
            for i, pos in enumerate(leaderboard, start=1):
                bank = pos["bank"]
                rucksack = pos["rucksack"]
                userID = pos["userID"]
                total = int(bank)
                total += int(rucksack)
                name = self.bot.get_user(int(userID))
                if name is None:
                    name = await self.bot.fetch_user(int(userID))
                    if name is None:
                        name = f"Nicht gefunden ({userID})"
                embed.add_field(name=f"{i}. {name} {name.id}", value=f"Total: {total} 🍪", inline=False)
                if i == 10:
                    await interaction.followup.send(embed=embed)
                    break
            if i != 10:
                await interaction.followup.send(embed=embed)
                
        if system == "Emojiquiz":
            leaderboard = await db["eq_leaderboard"].find().sort([("anzahl", -1)]).to_list(length=10)
            
            embed = discord.Embed(title="Bestenliste (Emojiquiz)", color=await getcolour(self, interaction.user))
            
            for i, pos in enumerate(leaderboard, start=1):
                anzahl = pos["anzahl"]
                userID = pos["userID"]
                name = self.bot.get_user(int(userID))
                if name is None:
                    name = await self.bot.fetch_user(int(userID))
                    if name is None:
                        name = f"Nicht gefunden ({userID})"
                embed.add_field(name=f"{i}. {name}", value=f"Gelöste Quizze: {anzahl}", inline=False)
                if i == 10:
                    await interaction.followup.send(embed=embed)
                    return

            await interaction.followup.send(embed=embed)

        if system == "Flaggenquiz":
            leaderboard = await db["fq_leaderboard"].find().sort([("anzahl", -1)]).to_list(length=10)
            
            embed = discord.Embed(title="Bestenliste (Flaggenquiz)", color=await getcolour(self, interaction.user))
            
            for i, pos in enumerate(leaderboard, start=1):
                anzahl = pos["anzahl"]
                userID = pos["userID"]
                name = self.bot.get_user(int(userID))
                if name is None:
                    name = await self.bot.fetch_user(int(userID))
                    if name is None:
                        name = f"Nicht gefunden ({userID})"
                embed.add_field(name=f"{i}. {name}", value=f"Gelöste Quizze: {anzahl}", inline=False)
                if i == 10:
                    await interaction.followup.send(embed=embed)
                    return
            
            await interaction.followup.send(embed=embed)
            
        if system == "Levelsystem":
            if not await getLevelSystemEnabled(self, interaction.guild):
                await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
                return
            
            leaderboard = await db["levelsystem"].find({"guild_id": str(interaction.guild.id)}).sort([("user_level", -1), ("user_xp", -1)]).to_list(length=10)
            embed = discord.Embed(title="Bestenliste (Levelsystem)", color=await getcolour(self, interaction.user))
            
            i = 0
            for eintrag in leaderboard:
                lvl = eintrag['user_level']
                xp = eintrag['user_xp']
                member_id = eintrag['client_id']
                xp_end = 5 * (math.pow(int(lvl) , 2)) + (50 * int(lvl)) + 100
                name = await self.bot.fetch_user(int(member_id))
                if name is None:
                    continue
                i += 1
                embed.add_field(name=f"{i}. {name}", value=f"Level {lvl} Erfahrung: {xp}/{xp_end}", inline=False)
                if i == 10:
                    await interaction.followup.send(embed=embed)
                    return
            
            await interaction.followup.send(embed=embed)
        
        if system == "TicTacToe":
            leaderboard = await db["ttt"].find().sort([("rating", -1)]).to_list(length=10)
            
            embed = discord.Embed(title="Bestenliste (TicTacToe)", color=await getcolour(self, interaction.user))
            
            for i, pos in enumerate(leaderboard, start=1):
                wins = pos["wins"]
                loses = pos["loses"]
                ties = pos["ties"]
                userID = pos["userID"]

                name = self.bot.get_user(int(userID))
                if name is None:
                    name = await self.bot.fetch_user(int(userID))
                    if name is None:
                        name = f"Nicht gefunden ({userID})"
                rating = (wins * 3) + (loses * -1) + (ties * 2)
                embed.add_field(name=f"{i}. {name}", value=f"Rating: {rating}", inline=False)    
                if i == 10:
                    await interaction.followup.send(embed=embed)
                    return

            await interaction.followup.send(embed=embed)
                
        if system == "Speedgame":
            leaderboard = await db["speedgame"].find().sort([("zeit", 1)]).to_list(length=10)
            embed = discord.Embed(title="Bestenliste (Speedgame)", color=await getcolour(self, interaction.user))
            
            for i, pos in enumerate(leaderboard, start=1):
                zeit = pos["zeit"]
                userID = pos["userID"]
                guildID = pos["guildID"]
                
                name = self.bot.get_user(int(userID))
                if name is None:
                    name = await self.bot.fetch_user(int(userID))
                    if name is None:
                        name = f"Nicht gefunden ({userID})"
                
                try:
                    guild = self.bot.get_guild(int(guildID))        
                except discord.errors.NotFound:
                    guild = f"Guild nicht gefunden ({guildID})"
                
                embed.add_field(name=f"{i}. {name}", value=f"{zeit}ms {'(' if guild is not None else ''}{guild.name if guild is not None else ''}{')' if guild is not None else ''}", inline=False)
                if i == 10:
                    await interaction.followup.send(embed=embed)
                    return
                
            await interaction.followup.send(embed=embed)
                
        if system == "Votes":
            leaderboard = await db["topgg"].find().sort([("votes", -1)]).to_list(length=10)
            embed = discord.Embed(title="Bestenliste (Votes)", description="**💎 [VOTE](https://top.gg/bot/925799559576322078/vote) auch du für Vulpo um vielleicht bald in der Top 10 zu sein. 💎**", color=await getcolour(self, interaction.user))
            
            for i, pos in enumerate(leaderboard, start=1):
                votes = pos["votes"]
                userID = pos["userID"]
                name = self.bot.get_user(int(userID))
                if name is None:
                    name = await self.bot.fetch_user(int(userID))
                    if name is None:
                        name = f"Nicht gefunden ({userID})"
                embed.add_field(name=f"{i}. {name}", value=f"{votes} Votes", inline=False)
                if i == 10:
                    await interaction.followup.send(embed=embed)
                    return

            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(meta(bot))