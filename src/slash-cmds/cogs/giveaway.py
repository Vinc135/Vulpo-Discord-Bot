import discord
from discord.ext import commands
import datetime
import asyncio
import math
from info import giveaway_end, discord_timestamp, convert
from discord import app_commands
import typing
     
async def teilnahme_angenommen(self, interaction, result):
    t2 = datetime.datetime.fromtimestamp(int(result[1]))
    embed = discord.Embed(colour=discord.Color.green(), title=result[6], description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)

`🎉` · Erfolgreich teilgenommen auf [{interaction.guild.name}]({interaction.message.jump_url})
`⏰` · Das Gewinnspiel endet {discord_timestamp(t2, 'R')}
""")
    embed.set_thumbnail(url=interaction.guild.icon)
    embed.set_image(url="https://media.discordapp.net/attachments/965302660871884840/1011704490598076416/GW_Pannel_31.png")
    await interaction.user.send("<a:teilnehmen:1000813245357105202> Deine Teilnahme an einem Gewinnspiel war **erfolgreich**.", embed=embed)
    
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT userID FROM gewinnspiel_teilnehmer WHERE guildID = (%s) AND channelID = (%s) AND msgID = (%s)", (interaction.guild.id, interaction.channel.id, interaction.message.id))
            teilnehmer = await cursor.fetchall()
            embed = discord.Embed(title=f"🏆 {result[6]}", description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)
                                      
<a:information:1000822286577844395> › __**Informationen**__
<:orangerpfeil:1000823380607516772> Erstellt von {interaction.guild.get_member(int(result[0])).mention}
<:orangerpfeil:1000823380607516772> **{result[2]}** Gewinner
<:orangerpfeil:1000823380607516772> Endet {discord_timestamp(t2, "R")}
<:orangerpfeil:1000823380607516772> **{len(teilnehmer)}** Teilnehmer

<a:anforderungen:1000822478119120906> › __**Anforderungen**__
<:orangerpfeil:1000823380607516772> **Drücke** unten auf **den Button**, um teilzunehmen.""", color=discord.Color.orange())
            
            requirements = ""
            if "Du benötigst die" in interaction.message.embeds[0].description:
                rolle = interaction.guild.get_role(int(result[5]))
                requirements += f"\n<:orangerpfeil:1000823380607516772> Du benötigst die **Rolle {rolle.mention}**."
            if "Du musst mindestens" in interaction.message.embeds[0].description:
                requirements += f"\n<:orangerpfeil:1000823380607516772> Du musst mindestens **{result[3]} neue Nachrichten** schreiben."
            if "bei Vulpo's Levelsystem sein" in interaction.message.embeds[0].description:
                requirements += f"\n<:orangerpfeil:1000823380607516772> Du musst mindestens **Level {result[4]}** bei Vulpo's Levelsystem sein."
                
            if requirements != "":
                embed.description += requirements
            embed.set_footer(text="🍀 Viel Glück")
            embed.set_thumbnail(url=interaction.guild.icon)
            await interaction.message.edit(content=interaction.message.content, embed=embed)

           
async def teilnahme_abgelehnt(self, interaction, grund, result):
    t2 = datetime.datetime.fromtimestamp(int(result[1]))
    embed = discord.Embed(colour=discord.Color.red(), title=result[6], description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)

`🎉` · Nicht erfolgreich teilgenommen auf [{interaction.guild.name}]({interaction.message.jump_url})
`⏰` · Das Gewinnspiel endet {discord_timestamp(t2, 'R')}

`❓` · Gründe:
{grund}
""")
    embed.set_thumbnail(url=interaction.guild.icon)
    embed.set_image(url="https://media.discordapp.net/attachments/965302660871884840/1009692136142286898/GW_Pannel_3.png")
    await interaction.user.send("<a:teilnehmen_fehlgeschlagen:1000814100001079348> Deine Teilnahme an einem Gewinnspiel war **nicht erfolgreich**.", embed=embed)

    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT userID FROM gewinnspiel_teilnehmer WHERE guildID = (%s) AND channelID = (%s) AND msgID = (%s)", (interaction.guild.id, interaction.channel.id, interaction.message.id))
            teilnehmer = await cursor.fetchall()
            embed = discord.Embed(title=f"🏆 {result[6]}", description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)
                                      
<a:information:1000822286577844395> › __**Informationen**__
<:orangerpfeil:1000823380607516772> Erstellt von {interaction.guild.get_member(int(result[0])).mention}
<:orangerpfeil:1000823380607516772> **{result[2]}** Gewinner
<:orangerpfeil:1000823380607516772> Endet {discord_timestamp(t2, "R")}
<:orangerpfeil:1000823380607516772> **{len(teilnehmer)}** Teilnehmer

<a:anforderungen:1000822478119120906> › __**Anforderungen**__
<:orangerpfeil:1000823380607516772> **Drücke** unten auf **den Button**, um teilzunehmen.""", color=discord.Color.orange())            
            requirements = ""
            if "Du benötigst die" in interaction.message.embeds[0].description:
                rolle = interaction.guild.get_role(int(result[5]))
                requirements += f"\n<:orangerpfeil:1000823380607516772> Du benötigst die **Rolle {rolle.mention}**."
            if "Du musst mindestens" in interaction.message.embeds[0].description:
                requirements += f"\n<:orangerpfeil:1000823380607516772> Du musst mindestens **{result[3]} neue Nachrichten** schreiben."
            if "bei Vulpo's Levelsystem sein" in interaction.message.embeds[0].description:
                requirements += f"\n<:orangerpfeil:1000823380607516772> Du musst mindestens **Level {result[4]}** bei Vulpo's Levelsystem sein."
                
            if requirements != "":
                embed.description += requirements
            embed.set_footer(text="🍀 Viel Glück")
            embed.set_thumbnail(url=interaction.guild.icon)
            await interaction.message.edit(content=interaction.message.content, embed=embed)
    
    
class Gewinnspiel_Teilnehmen(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label='Teilnehmen', style=discord.ButtonStyle.green, custom_id="dqbckiwluheljvkhgciulehfgk")
    async def teilnehmen(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(interaction.user.id)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                #Genaue Informationen des Gewinnspiels aus der Datenbank holen
                await cursor.execute("SELECT hostID, endtime, winners, nachrichten, level, rollenID, preis FROM gewinnspiele WHERE guildID = (%s) AND channelID = (%s) AND msgID = (%s)", (interaction.guild.id, interaction.channel.id, interaction.message.id))
                result = await cursor.fetchone()
                if result is None:
                    return
                #Die Gewinnspiel Blacklist überprüfen
                await cursor.execute("SELECT id FROM gewinnspiel_blacklist WHERE guildID = (%s)", (interaction.guild.id))
                blacklist = await cursor.fetchall()
                for id in blacklist:
                    rolle = interaction.guild.get_role(int(id[0]))
                    if rolle != None:
                        if rolle in member.roles:
                            await interaction.response.defer(ephemeral=True, thinking=False)
                            return await teilnahme_abgelehnt(self, interaction, "`❌` Du stehst auf der Gewinnspiel Blacklist und bist deshalb von jeglichen Gewinnspielen dieses Servers ausgeschlossen.", result)
                    if int(id[0]) == interaction.user.id:
                        await interaction.response.defer(ephemeral=True, thinking=False)
                        return await teilnahme_abgelehnt(self, interaction, "`❌` Du stehst auf der Gewinnspiel Blacklist und bist deshalb von jeglichen Gewinnspielen dieses Servers ausgeschlossen.", result)
                    
                await cursor.execute("SELECT msgID, channelID, hostID, endtime, winners, nachrichten, level, rollenID, preis FROM gewinnspiele WHERE guildID = (%s) AND status = (%s)", (interaction.guild.id, "Aktiv"))
                bypassrollen = await cursor.fetchall()
                for bypassrolle in bypassrollen:
                    bpr = interaction.guild.get_role(int(bypassrolle[0]))
                    if bpr == None:
                        pass
                    if bpr in member.roles:#Mitglied besitzt eine bypassrolle
                        await cursor.execute("SELECT userID FROM gewinnspiel_teilnehmer WHERE guildID = (%s) AND channelID = (%s) AND msgID = (%s) AND userID = (%s)", (interaction.guild.id, interaction.channel.id, interaction.message.id, interaction.user.id))
                        result4 = await cursor.fetchone()
                        if result4 != None:
                            await interaction.response.defer(ephemeral=True, thinking=False)
                            await cursor.execute("DELETE FROM gewinnspiel_teilnehmer WHERE guildID = (%s) AND channelID = (%s) AND msgID = (%s) AND userID = (%s)", (interaction.guild.id, interaction.channel.id, interaction.message.id, interaction.user.id))
                            return await teilnahme_abgelehnt(self, interaction, "`❌` Du warst bereits ein Teilnehmer, hast jedoch nochmal den Button gedrückt. Nun bist du kein Teilnehmer mehr.", result)
                            #Mitglied ist kein Teilnehmer mehr
                        #Mitglied war noch kein Teilnehmer
                        await interaction.response.defer(ephemeral=True, thinking=False)
                        await cursor.execute("INSERT INTO gewinnspiel_teilnehmer(guildID, channelID, msgID, userID) VALUES(%s, %s, %s, %s)", (interaction.guild.id, interaction.channel.id, interaction.message.id, interaction.user.id))
                        return await teilnahme_angenommen(self, interaction, result)
                        #Mitglied ist nun Teilnehmer
                #Die Nachrichten Anforderung überprüfen
                if result[3] != None:
                    await cursor.execute("SELECT anzahl FROM gw_nachrichten WHERE gwID = (%s) AND userID = (%s) AND guildID = (%s)", (interaction.message.id, interaction.user.id, interaction.guild.id))
                    result2 = await cursor.fetchall()
                    if result2 == ():
                        await interaction.response.defer(ephemeral=True, thinking=False)
                        return await teilnahme_abgelehnt(self, interaction, f"`🔥` Du hast bisher 0 Nachrichten geschrieben, benötigst jedoch {result[3]} Nachrichten um am Gewinnspiel teilzunehmen.", result)
                    nachrichten = 0
                    for tag in result2:
                        nachrichten += int(tag[0])
                    if nachrichten < int(result[3]):
                        await interaction.response.defer(ephemeral=True, thinking=False)
                        return await teilnahme_abgelehnt(self, interaction, f"`🔥` Du hast bisher {nachrichten} Nachrichten geschrieben, benötigst jedoch {result[3]} Nachrichten um am Gewinnspiel teilzunehmen.", result)
                #Die Level Anforderung überprüfen
                if result[4] != None:
                    await cursor.execute("SELECT user_level FROM levelsystem WHERE client_id = (%s) AND guild_id = (%s)", (member.id, interaction.guild.id))
                    result3 = await cursor.fetchone()
                    if result3 is None:
                        await interaction.response.defer(ephemeral=True, thinking=False)
                        return await teilnahme_abgelehnt(self, interaction, f"`🔥` Du bist hier Level 0, benötigst jedoch Level {result[4]} um am Gewinnspiel teilzunehmen.", result)
                    if int(result3[0]) < int(result[4]):
                        await interaction.response.defer(ephemeral=True, thinking=False)
                        return await teilnahme_abgelehnt(self, interaction, f"`🔥` Du bist hier Level {result3[0]}, benötigst jedoch Level {result[4]} um am Gewinnspiel teilzunehmen.", result)
                #Die Rollen Anforderung überprüfen
                if result[5] != None:
                    rolle2 = interaction.guild.get_role(int(result[5]))
                    if rolle2 != None:
                        if rolle2 not in member.roles:
                            await interaction.response.defer(ephemeral=True, thinking=False)
                            return await teilnahme_abgelehnt(self, interaction, f"`❌` Du benötigst die Rolle {rolle2.name} um am Gewinnspiel teilzunehmen.", result)
                
                #Wenn man bis hier gekommen ist, erfüllt man alle Anforderungen, falls es welche gab
                #Das Mitglied als "möglichen Gewinner" eintragen
                await cursor.execute("SELECT userID FROM gewinnspiel_teilnehmer WHERE guildID = (%s) AND channelID = (%s) AND msgID = (%s) AND userID = (%s)", (interaction.guild.id, interaction.channel.id, interaction.message.id, interaction.user.id))
                result5 = await cursor.fetchone()
                if result5 != None:
                    await interaction.response.defer(ephemeral=True, thinking=False)
                    await cursor.execute("DELETE FROM gewinnspiel_teilnehmer WHERE guildID = (%s) AND channelID = (%s) AND msgID = (%s) AND userID = (%s)", (interaction.guild.id, interaction.channel.id, interaction.message.id, interaction.user.id))
                    return await teilnahme_abgelehnt(self, interaction, "`❌` Du warst bereits ein Teilnehmer, hast jedoch nochmal den Button gedrückt. Nun bist du kein Teilnehmer mehr.", result)
                    #Mitglied ist kein Teilnehmer mehr
                #Mitglied war noch kein Teilnehmer
                await interaction.response.defer(ephemeral=True, thinking=False)
                await cursor.execute("INSERT INTO gewinnspiel_teilnehmer(guildID, channelID, msgID, userID) VALUES(%s, %s, %s, %s)", (interaction.guild.id, interaction.channel.id, interaction.message.id, interaction.user.id))
                await teilnahme_angenommen(self, interaction, result)
                #Mitglied ist nun Teilnehmer

    
class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot:
            return
        if msg.guild != None:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT msgID FROM gewinnspiele WHERE guildID = (%s) AND status = (%s)", (msg.guild.id, "Aktiv"))
                    result2 = await cursor.fetchall()
                    if result2 == ():
                        return
                    for gewinnspiel in result2:
                        await cursor.execute("SELECT anzahl FROM gw_nachrichten WHERE userID = (%s) AND guildID = (%s) AND gwID = (%s)", (msg.author.id, msg.guild.id, gewinnspiel[0]))
                        result = await cursor.fetchone()
                        if result == None:
                            await cursor.execute("INSERT INTO gw_nachrichten(userID, guildID, gwID, anzahl) VALUES(%s, %s, %s, %s)", (msg.author.id, msg.guild.id, gewinnspiel[0], 1))
                        else:
                            await cursor.execute("UPDATE gw_nachrichten SET anzahl = (%s) WHERE guildID = (%s) AND userID = (%s) AND gwID = (%s)", (result[0] + 1, msg.guild.id, msg.author.id, gewinnspiel[0]))
        
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=Gewinnspiel_Teilnehmen(self.bot))
                
    gewinnspiel = app_commands.Group(name='gewinnspiel', description='Verwalte Gewinnspiele.')
    
    @gewinnspiel.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def starten(self, interaction: discord.Interaction, preis: str, kanal: discord.TextChannel, gewinneranzahl: typing.Literal[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90], minuten: typing.Literal["1m","15m","30m","45m"]=None, stunden: typing.Literal["1h","2h","3h","4h","5h","6h","7h","8h","9h","10h","11h","12h","13h","14h","15h","16h","17h","18h","19h","20h","21h","22h","23h"]=None, tage: typing.Literal["1d","2d","3d","4d","5d","6d","7d","14d"]=None, rolle: discord.Role=None, nachrichtenanzahl: int=None, mindestlevel: int=None):
        """Starte ein Gewinnspiel."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                #endzeit umwandeln in timestamp
                zeit_als_string = ""
                if tage:
                    zeit_als_string += f" {tage}"
                if stunden:
                    zeit_als_string += f" {stunden}"
                if minuten:
                    zeit_als_string += f" {minuten}"
                if zeit_als_string == "":
                    return await interaction.response.send_message("**❌ Du musst auch eine Zeit angeben, wann das Gewinnspiel enden soll ;D**", ephemeral=True)
                if nachrichtenanzahl:
                    if nachrichtenanzahl > 10000:
                        return await interaction.response.send_message("**❌ Das Maximum für eine Mindestnachrichtenanzahl liegt bei 10000. Bitte überschreite diese Grenze nicht.**", ephemeral=True)
                zeit = convert(zeit_als_string)
                t1 = math.floor(datetime.datetime.utcnow().timestamp() + zeit)
                t2 = datetime.datetime.fromtimestamp(int(t1))

                #giveaway nachricht (public)
                #requirementsliste
                requirements = ""
                if rolle:
                    requirements += f"\n<:orangerpfeil:1000823380607516772> Du benötigst die **Rolle {rolle.mention}**."
                if nachrichtenanzahl:
                    requirements += f"\n<:orangerpfeil:1000823380607516772> Du musst mindestens **{nachrichtenanzahl} neue Nachrichten** schreiben."
                if mindestlevel:
                    requirements += f"\n<:orangerpfeil:1000823380607516772> Du musst mindestens **Level {mindestlevel}** bei Vulpo's Levelsystem sein."
                embed = discord.Embed(title=f"🏆 {preis}", description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)
                                      
<a:information:1000822286577844395> › __**Informationen**__
<:orangerpfeil:1000823380607516772> Erstellt von {interaction.user.mention}
<:orangerpfeil:1000823380607516772> **{gewinneranzahl}** Gewinner
<:orangerpfeil:1000823380607516772> Endet {discord_timestamp(t2, "R")}
<:orangerpfeil:1000823380607516772> **0** Teilnehmer

<a:anforderungen:1000822478119120906> › __**Anforderungen**__
<:orangerpfeil:1000823380607516772> **Drücke** unten auf **den Button**, um teilzunehmen.""", color=discord.Color.orange())
                if requirements != "":
                    embed.description += requirements
                embed.set_footer(text="🍀 Mit dem Drücken des Buttons stimmst du einer Direktnachricht zu.")
                embed.set_thumbnail(url=interaction.guild.icon)

                m = await kanal.send("**🎊 Neues Gewinnspiel 🎊**", embed=embed, view=Gewinnspiel_Teilnehmen(self.bot))
                asyncio.create_task(giveaway_end(t2, self.bot, m.id))
                

                #In die Datenbank eintragen
                if rolle:
                    await cursor.execute("INSERT INTO gewinnspiele(guildID, channelID, msgID, hostID, endtime, winners, nachrichten, level, rollenID, status, preis) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (interaction.guild.id, kanal.id, m.id, interaction.user.id, t1, gewinneranzahl, nachrichtenanzahl, mindestlevel, rolle.id, "Aktiv", preis))
                else:
                    await cursor.execute("INSERT INTO gewinnspiele(guildID, channelID, msgID, hostID, endtime, winners, nachrichten, level, rollenID, status, preis) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (interaction.guild.id, kanal.id, m.id, interaction.user.id, t1, gewinneranzahl, nachrichtenanzahl, mindestlevel, None, "Aktiv", preis))

                await interaction.response.send_message(f"**✅ Das Gewinnspiel findet nun statt in {kanal.mention}.**")

    @gewinnspiel.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def verwalten(self, interaction: discord.Interaction, aktion: typing.Literal["Gewinnspiel beenden (Nachrichten ID erforderlich)","Gewinnspiel neu würfeln (Nachrichten ID erforderlich)","Gewinnspiele anzeigen"], nachrichtenid: str=None):
        """Verwalte Gewinnspiele."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if aktion == "Gewinnspiel beenden (Nachrichten ID erforderlich)":
                    if nachrichtenid is None:
                        return await interaction.response.send_message("**❌ Du musst eine Nachrichten ID mit angeben beim Befehl.**", ephemeral=True)
                    await cursor.execute("SELECT channelID, hostID, endtime, winners, nachrichten, level, rollenID, preis FROM gewinnspiele WHERE guildID = (%s) AND status = (%s) AND msgID = (%s)", (interaction.guild.id, "Aktiv", nachrichtenid))
                    result = await cursor.fetchone()
                    if result == None:
                        return await interaction.response.send_message(f"**❌ Es wurde kein aktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem aktiven Gewinnspiel handelt**", ephemeral=True)
                    kanal = interaction.guild.get_channel(int(result[0]))
                    if kanal == None:
                        return await interaction.response.send_message(f"**❌ Es wurde kein aktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem aktiven Gewinnspiel handelt**", ephemeral=True)
                    nachricht = await kanal.fetch_message(int(nachrichtenid))
                    if nachricht == None:
                        return await interaction.response.send_message(f"**❌ Es wurde kein aktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem aktiven Gewinnspiel handelt**", ephemeral=True)
                    t1 = math.floor(datetime.datetime.utcnow().timestamp() + 1)
                    t2 = datetime.datetime.fromtimestamp(int(t1))
                    await interaction.response.send_message("**✅ Gewinnspiel wird beendet.**")
                    await giveaway_end(t2, self.bot, nachricht.id, "Beenden")
                
                if aktion == "Gewinnspiel neu würfeln (Nachrichten ID erforderlich)":
                    if nachrichtenid is None:
                        return await interaction.response.send_message("**❌ Du musst eine Nachrichten ID mit angeben beim Befehl.**", ephemeral=True)
                    await cursor.execute("SELECT channelID, hostID, endtime, winners, nachrichten, level, rollenID, preis FROM gewinnspiele WHERE guildID = (%s) AND status = (%s) AND msgID = (%s)", (interaction.guild.id, "Inaktiv", nachrichtenid))
                    result2 = await cursor.fetchone()
                    if result2 == None:
                        return await interaction.response.send_message(f"**❌ Es wurde kein inaktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem inaktiven Gewinnspiel handelt**", ephemeral=True)
                    kanal2 = interaction.guild.get_channel(int(result2[0]))
                    if kanal2 == None:
                        return await interaction.response.send_message(f"**❌ Es wurde kein inaktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem inaktiven Gewinnspiel handelt**", ephemeral=True)
                    nachricht2 = await kanal2.fetch_message(int(nachrichtenid))
                    if nachricht2 == None:
                        return await interaction.response.send_message(f"**❌ Es wurde kein inaktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem inaktiven Gewinnspiel handelt**", ephemeral=True)
                    t1 = math.floor(datetime.datetime.utcnow().timestamp() + 1)
                    t2 = datetime.datetime.fromtimestamp(int(t1))
                    await interaction.response.send_message("**✅ Gewinnspiel wird neu ausgelost.**")
                    await giveaway_end(t2, self.bot, nachricht2.id, "Reroll")
                    
                if aktion == "Gewinnspiele anzeigen":
                    await cursor.execute("SELECT msgID, channelID, hostID, endtime, winners, nachrichten, level, rollenID, preis FROM gewinnspiele WHERE guildID = (%s) AND status = (%s)", (interaction.guild.id, "Aktiv"))
                    result3 = await cursor.fetchall()
                    if result3 == ():
                        return await interaction.response.send_message("**❌ Es gibt keine aktiven Gewinnspiele auf diesem Server.**", ephemeral=True)
                    embed = discord.Embed(colour=discord.Colour.orange(), title="Gewinnspiele", description="Alle aktiven Gewinnspiele von diesem Server findest du in dieser Nachricht.")
                    for gewinnspiel in result3:
                        kanal3 = interaction.guild.get_channel(int(gewinnspiel[1]))
                        if kanal3 == None:
                            pass
                        nachricht3 = await kanal3.fetch_message(int(gewinnspiel[0]))
                        if nachricht3 == None:
                            pass
                        t2 = datetime.datetime.fromtimestamp(int(result3[3]))
                        embed.add_field(name=f"[{result3[8]}]({nachricht3.jump_url()})", value=f"Das Gewinnspiel endet {discord_timestamp(t2, 'R')}.", inline=False)
                    await interaction.response.send_message(embed=embed)

    @gewinnspiel.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def bypassrolle(self, interaction: discord.Interaction, aktion: typing.Literal["Hinzufügen (Rolle erforderlich)","Entfernen (Rolle erforderlich)","Alle anzeigen"], rolle: discord.Role=None):
        """Bearbeite Rollen, die die Bedingungen umgehen."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if aktion == "Hinzufügen (Rolle erforderlich)":
                    if rolle == None:
                        return await interaction.response.send_message("**❌ Du musst natürlich auch eine Rolle angeben im Command.**", ephemeral=True)
                    await cursor.execute("SELECT rollenID FROM gewinnspiele_bypassrolle WHERE rollenID = (%s) AND guildID = (%s)", (rolle.id, interaction.guild.id))
                    result = await cursor.fetchone()
                    if result != None:
                        return await interaction.response.send_message("**❌ Diese Bypassrolle existiert bereits.**", ephemeral=True)
                    await cursor.execute("INSERT INTO gewinnspiele_bypassrolle(guildID, rollenID) VALUES(%s, %s)", (interaction.guild.id, rolle.id))
                    return await interaction.response.send_message("**✅ Die Rolle ist nun eine Bypassrolle.**")
                if aktion == "Entfernen (Rolle erforderlich)":
                    if rolle == None:
                        return await interaction.response.send_message("**❌ Du musst natürlich auch eine Rolle angeben im Command.**", ephemeral=True)
                    await cursor.execute("SELECT rollenID FROM gewinnspiele_bypassrolle WHERE rollenID = (%s) AND guildID = (%s)", (rolle.id, interaction.guild.id))
                    result2 = await cursor.fetchone()
                    if result2 == None:
                        return await interaction.response.send_message("**❌ Diese Bypassrolle existiert nicht.**", ephemeral=True)
                    await cursor.execute("DELETE FROM gewinnspiele_bypassrolle WHERE guildID = (%s) AND rollenID = (%s)", (interaction.guild.id, rolle.id))
                    return await interaction.response.send_message("**✅ Die Rolle ist nun keine Bypassrolle mehr.**")
                if aktion == "Alle anzeigen":
                    await cursor.execute("SELECT rollenID FROM gewinnspiele_bypassrolle WHERE guildID = (%s)", (interaction.guild.id))
                    result3 = await cursor.fetchall()
                    if result3 == None:
                        return await interaction.response.send_message("**❌ Auf diesem Server gibt es keine Bypassrollen.**", ephemeral=True)
                    embed = discord.Embed(colour=discord.Colour.orange(), title="Gewinnspiele", description="Alle aktiven Gewinnspiele von diesem Server findest du in dieser Nachricht.")
                    for rolle in result3:
                        rolle2 = interaction.guild.get_role(int(rolle[0]))
                        if rolle2 == None:
                            pass
                        embed.add_field(name=rolle2.mention, value="Die User mit dieser Rolle sind von Anforderungen von Gewinnspielen dieses Servers ausgeschlossen.", inline=False)
                    await interaction.response.send_message(embed=embed)
                
    @gewinnspiel.command()
    @app_commands.checks.has_permissions()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def blockieren(self, interaction: discord.Interaction, id: str):
        """Setze Member und Rollen auf die Blacklist."""
        try:
            member = self.bot.get_user(int(id))
            rolle = interaction.guild.get_role(int(id))
            if member == None and rolle == None:
                return await interaction.response.send_message("**❌ Die ID muss entweder eine Rollen ID oder eine Member ID sein.**", ephemeral=True)
        except:
            return await interaction.response.send_message("**❌ Die ID muss entweder eine Rollen ID oder eine Member ID sein.**", ephemeral=True)

        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if member:
                    await cursor.execute("SELECT id FROM gewinnspiel_blacklist WHERE guildID = (%s) AND id = (%s)", (interaction.guild.id, id))
                    result = await cursor.fetchone()
                    if result == None:
                        await cursor.execute("INSERT INTO gewinnspiel_blacklist(guildID, id) VALUES(%s, %s)", (interaction.guild.id, id))
                        return await interaction.response.send_message(f"**✅ {member} ist nun auf der Blacklist**")
                    await cursor.execute("DELETE FROM gewinnspiel_blacklist WHERE guildID = (%s) AND id = (%s)", (interaction.guild.id, id))
                    return await interaction.response.send_message(f"**✅ {member} ist nun nicht mehr auf der Blacklist**")
                if rolle:
                    await cursor.execute("SELECT id FROM gewinnspiel_blacklist WHERE guildID = (%s) AND id = (%s)", (interaction.guild.id, id))
                    result = await cursor.fetchone()
                    if result == None:
                        await cursor.execute("INSERT INTO gewinnspiel_blacklist(guildID, id) VALUES(%s, %s)", (interaction.guild.id, id))
                        return await interaction.response.send_message(f"**✅ {rolle.name} ist nun auf der Blacklist**")
                    await cursor.execute("DELETE FROM gewinnspiel_blacklist WHERE guildID = (%s) AND id = (%s)", (interaction.guild.id, id))
                    return await interaction.response.send_message(f"**✅ {rolle.name} ist nun nicht mehr auf der Blacklist**")
        
async def setup(bot):
    await bot.add_cog(giveaway(bot))