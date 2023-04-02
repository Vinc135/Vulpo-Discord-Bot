import typing
import discord
from discord.ext import commands
import random
from discord import app_commands
from easy_pil import Editor, load_image_async, Font
from info import getcolour

class Willkommensnachricht(discord.ui.Modal, title="Willkommensnachricht"):
    def __init__(self, kanal: discord.TextChannel=None, bot=None, alte_nachricht: str=None):
        super().__init__(custom_id="wWk766We676e6Wwe274kwW")
        self.kanal = kanal
        self.bot = bot
        self.alte_nachricht = alte_nachricht
        self.add_item(discord.ui.TextInput(label="Nachricht", style=discord.TextStyle.paragraph, required=True, placeholder="%member-Member#0000 | %name-Member | %mention-@Member | %guild-Servername | %usercount-Memberanzahl", default=str(self.alte_nachricht).replace("B9xV123", "")))
        self.add_item(discord.ui.TextInput(label="Mit Willkommens-Bild?", style=discord.TextStyle.short, required=True, placeholder="Antworte mit 'Ja' oder 'Nein'."))

    async def on_submit(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if str(self.alte_nachricht) == "%member-Member#0000 | %name-Member | %mention-@Member | %guild-Servername | %usercount-Memberanzahl":
                    if str(self.children[1].value).lower() == "ja":
                        await cursor.execute("INSERT INTO welcome (guildID, channelID, msg) VALUES (%s, %s, %s)", (interaction.guild.id, self.kanal.id, f"{self.children[0].value} B9xV123"))
                        return await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Willkommensnachricht ist nun aktiv.**")
                    if str(self.children[1].value).lower() == "nein":
                        await cursor.execute("INSERT INTO welcome (guildID, channelID, msg) VALUES (%s, %s, %s)", (interaction.guild.id, self.kanal.id, self.children[0].value))
                        return await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Willkommensnachricht ist nun aktiv.**")
                    else:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Gib beim nächsten Mal deine Antwort beim Feld '**Mit Bild?**' mit einem klaren 'Ja' oder 'Nein' wider.**", ephemeral=True)
                    
                
                if str(self.children[1].value).lower() == "ja":
                    await cursor.execute("UPDATE welcome SET channelID = (%s) WHERE guildID = (%s)", (self.kanal.id, interaction.guild.id))
                    await cursor.execute("UPDATE welcome SET msg = (%s) WHERE guildID = (%s)", (f"{self.children[0].value} B9xV123", interaction.guild.id))
                    return await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Willkommensnachricht ist nun geändert.**")
                if str(self.children[1].value).lower() == "nein":
                    await cursor.execute("UPDATE welcome SET channelID = (%s) WHERE guildID = (%s)", (self.kanal.id, interaction.guild.id))
                    await cursor.execute("UPDATE welcome SET msg = (%s) WHERE guildID = (%s)", (self.children[0].value, interaction.guild.id))
                    return await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Willkommensnachricht ist nun geändert.**")
                else:
                    return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Gib beim nächsten Mal deine Antwort beim Feld '**Mit Bild?**' mit einem klaren 'Ja' oder 'Nein' wider.**", ephemeral=True)
                

class Verlassensnachricht(discord.ui.Modal, title="Verlassensnachricht"):
    def __init__(self, kanal: discord.TextChannel=None, bot=None, alte_nachricht: str=None):
        super().__init__(custom_id="2Byyy55BNyly55lylm5ml2")
        self.kanal = kanal
        self.bot = bot
        self.alte_nachricht = alte_nachricht
        self.add_item(discord.ui.TextInput(label="Nachricht", style=discord.TextStyle.paragraph, required=True, placeholder="%member-Member#0000 | %name-Member | %mention-@Member | %guild-Servername | %usercount-Memberanzahl", default=self.alte_nachricht))

    async def on_submit(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if str(self.alte_nachricht) == "%member-Member#0000 | %name-Member | %mention-@Member | %guild-Servername | %usercount-Memberanzahl":
                    await cursor.execute("INSERT INTO leavemsg (guildID, channelID, msg) VALUES (%s, %s, %s)", (interaction.guild.id, self.kanal.id, self.children[0].value))
                    return await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Verlassensnachricht ist nun aktiv.**")
                await cursor.execute("UPDATE leavemsg SET channelID = (%s) WHERE guildID = (%s)", (self.kanal.id, interaction.guild.id))
                await cursor.execute("UPDATE leavemsg SET msg = (%s) WHERE guildID = (%s)", (self.children[0].value, interaction.guild.id))
                return await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Verlassensnachricht ist nun geändert.**")

##########

def random_color():
    return discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#welcome message

    @commands.Cog.listener()
    async def on_member_join(self, member):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelID, msg FROM welcome WHERE guildID = {member.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    return
                else:
                    try:
                        ch = member.guild.get_channel(int(result[0]))
                    except:
                        return
                    if "B9xV123" not in str(result[1]):
                        finalmsg = result[1].replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
                        try:
                            embed = discord.Embed(color=await getcolour(self, member), description=finalmsg)
                            await ch.send(finalmsg)
                        except:
                            pass
                    else:
                        finalmsg = result[1].replace("B9xV123", "").replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
                        try:
                            embed = discord.Embed(color=await getcolour(self, member), description=finalmsg)
                            background = Editor("willkommen.png")
                            profile = await load_image_async(str(member.avatar))

                            profile = Editor(profile).resize((125, 125)).circle_image()
                            background.paste(profile.image, (100, 100))
                            poppins_small = Font.poppins("bold", size=30)
                            background.text((380, 145), str(member), font=poppins_small, color="#e67e22")
                            background.text((380, 195), str(member.id), font=poppins_small, color="#e67e22")
                            background.text((500, 245), str(member.guild.member_count), font=poppins_small, color="#e67e22")
                            file = discord.File(fp=background.image_bytes, filename="willkommen.png")

                            embed.set_image(url="attachment://willkommen.png")
                            await ch.send(embed=embed, file=file)
                        except:
                            pass

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def testjoin(self, interaction: discord.Interaction):
        """Sendet die Willkommensnachricht an den Kanal, um zu sehen ob sie funktioniert."""
        member = interaction.user
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelID, msg FROM welcome WHERE guildID = {interaction.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Auf diesem Server ist keine Willkommensnachricht eingerichtet.**", ephemeral=True)
                try:
                    ch = interaction.guild.get_channel(int(result[0]))
                except:
                    return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Auf diesem Server ist keine Willkommensnachricht eingerichtet.**", ephemeral=True)

                if "B9xV123" not in str(result[1]):
                    finalmsg = result[1].replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
                    await ch.send(finalmsg + f"\n\nTest-Willkommensnachricht angefordert von {interaction.user}")
                    return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Die Test-Willkommensnachricht wurde an den Kanal {ch.mention} gesendet.**")

                else:
                    finalmsg = result[1].replace("B9xV123", "").replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
                    background = Editor("willkommen.png")
                    profile = await load_image_async(str(member.avatar))

                    profile = Editor(profile).resize((160, 160)).circle_image()
                    background.paste(profile.image, (100, 100))
                    poppins_small = Font.poppins("bold", size=30)
                    background.text((380, 142), str(member), font=poppins_small, color="#e67e22")
                    background.text((380, 192), str(member.id), font=poppins_small, color="#e67e22")
                    background.text((500, 245), str(member.guild.member_count), font=poppins_small, color="#e67e22")
                    file = discord.File(fp=background.image_bytes, filename="willkommen.png")

                    await ch.send(finalmsg + f"\nTestjoin angefordert von {interaction.user}", file=file)
                    await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Die Test-Willkommensnachricht wurde an den Kanal {ch.mention} gesendet.**")

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def joinmsg(self, interaction: discord.Interaction, argument: typing.Literal["Einrichten (Kanal muss mit angegeben werden)","Anzeigen","Ausschalten"], kanal: discord.TextChannel=None):
        """Stelle die Willkommensnachricht ein."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if argument == "Ausschalten":
                    await cursor.execute(f"SELECT channelID, msg FROM welcome WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    if result == None:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Auf diesem Server ist keine Willkommensnachricht eingerichtet.**", ephemeral=True)
                    await cursor.execute("DELETE FROM welcome WHERE guildID = (%s)", (interaction.guild.id))
                    return await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Willkommensnachricht wurde ausgeschaltet.**")
                if argument == "Einrichten (Kanal muss mit angegeben werden)":
                    if kanal == None:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Beim Einrichten ist auch eine Kanal-Angabe erforderlich.**", ephemeral=True)

                    await cursor.execute(f"SELECT channelID, msg FROM welcome WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    alte_nachricht = ""
                    if result:
                        alte_nachricht += result[1]
                    else:
                        alte_nachricht += "%member-Member#0000 | %name-Member | %mention-@Member | %guild-Servername | %usercount-Memberanzahl"
                    await interaction.response.send_modal(Willkommensnachricht(kanal, self.bot, alte_nachricht))
                if argument == "Anzeigen":
                    await cursor.execute(f"SELECT channelID, msg FROM welcome WHERE guildID = {interaction.guild.id}")
                    wel = await cursor.fetchone()
                    try:
                        ch = interaction.guild.get_channel(int(wel[0]))
                    except:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Der Kanal der Willkommensnachricht existiert nicht mehr. Bitte deaktiviere die Willkommensnachricht und richte sie erneut ein.**", ephemeral=True)

                    embed = discord.Embed(title="Willkommensnachricht", description=f"Die aktuelle Willkommensnachricht:", color=await getcolour(self, interaction.user))
                    embed.add_field(name="Kanal", value=ch.mention, inline=False)
                    embed.add_field(name="Nachricht", value=wel[1], inline=False)
                    await interaction.response.send_message(embed=embed)

#leave message
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelID, msg FROM leavemsg WHERE guildID = {member.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    return
                else:
                    try:
                        ch = member.guild.get_channel(int(result[0]))
                    except:
                        return
                    finalmsg = result[1].replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
                    try:
                        embed = discord.Embed(color=await getcolour(self, member), description=finalmsg)
                        await ch.send(embed=embed)
                    except:
                        pass
            
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def testleave(self, interaction: discord.Interaction):
        """Sendet die Verlassensnachricht an den Kanal, um zu sehen ob sie funktioniert."""
        member = interaction.user
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelID, msg FROM leavemsg WHERE guildID = {interaction.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Auf diesem Server ist keine Verlassensnachricht eingerichtet. Deaktiviere diese zuerst!**", ephemeral=True)
                try:
                    ch = interaction.guild.get_channel(int(result[0]))
                except:
                    return
                finalmsg = result[1].replace("%member", str(member)).replace("%name", str(member.name)).replace("%mention", str(member.mention)).replace("%guild", str(member.guild)).replace("%usercount", str(member.guild.member_count))
                try:
                    embed = discord.Embed(color=await getcolour(self, interaction.user), description=finalmsg)
                    embed.set_footer(text=f"Test-Verlassensnachricht angefordert von {interaction.user}")
                    await ch.send(embed=embed)
                    await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Die Test-Verlassensnachricht wurde an den Kanal {ch.mention} gesendet.**")
                except:
                    pass

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def leavemsg(self, interaction: discord.Interaction, argument: typing.Literal["Einrichten (Kanal muss mit angegeben werden)","Anzeigen","Ausschalten"], kanal: discord.TextChannel=None):
        """Stelle die Verlassensnachricht ein."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if argument == "Ausschalten":
                    await cursor.execute(f"SELECT channelID, msg FROM leavemsg WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    if result == None:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Auf diesem Server ist keine Verlassensnachricht eingerichtet.**", ephemeral=True)
                    await cursor.execute("DELETE FROM leavemsg WHERE guildID = (%s)", (interaction.guild.id))
                    return await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Verlassensnachricht wurde ausgeschaltet.**")
                if argument == "Einrichten (Kanal muss mit angegeben werden)":
                    if kanal == None:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Beim Einrichten ist auch eine Kanal-Angabe erforderlich.**", ephemeral=True)

                    await cursor.execute(f"SELECT channelID, msg FROM leavemsg WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    alte_nachricht = ""
                    if result:
                        alte_nachricht += result[1]
                    else:
                        alte_nachricht += "%member-Member#0000 | %name-Member | %mention-@Member | %guild-Servername | %usercount-Memberanzahl"
                    await interaction.response.send_modal(Verlassensnachricht(kanal, self.bot, alte_nachricht))
                if argument == "Anzeigen":
                    await cursor.execute(f"SELECT channelID, msg FROM leavemsg WHERE guildID = {interaction.guild.id}")
                    wel = await cursor.fetchone()
                    try:
                        ch = interaction.guild.get_channel(int(wel[0]))
                    except:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Der Kanal der Verlassensnachricht existiert nicht mehr. Bitte deaktiviere die Verlassensnachricht und richte sie erneut ein.**", ephemeral=True)

                    embed = discord.Embed(title="Verlassensnachricht", description=f"Die aktuelle Verlassensnachricht:", color=await getcolour(self, interaction.user))
                    embed.add_field(name="Kanal", value=ch.mention, inline=False)
                    embed.add_field(name="Nachricht", value=wel[1], inline=False)
                    await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(message(bot))