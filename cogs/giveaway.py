import discord
from discord.ext import commands
import datetime
import asyncio
import math
from utils.utils import giveaway_end, discord_timestamp, convert
from utils.MongoDB import getMongoDataBase
from discord import app_commands
import typing
import pytz
from utils.utils import getcolour
     
async def teilnahme_angenommen(self, interaction: discord.Interaction, result):
    t2 = datetime.datetime.fromtimestamp(int(result["endtime"]))
    embed = discord.Embed(colour=await getcolour(self, interaction.user), title=result['preis'], description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)

`🎉` · Erfolgreich teilgenommen auf [{interaction.guild.name}]({interaction.message.jump_url})
`⏰` · Das Gewinnspiel endet {discord_timestamp(t2, 'R')}
""")
    embed.set_thumbnail(url=interaction.guild.icon)
    embed.set_image(url="https://media.discordapp.net/attachments/1023508002453594122/1023508199426506782/GW_Pannel_31.png")
    
    await interaction.followup.send("<:v_181:1264268817790664756> Deine Teilnahme an einem Gewinnspiel war **erfolgreich**.", embed=embed, ephemeral=True)
    
    db = getMongoDataBase()
    
    teilnehmer_count = await db["gewinnspiel_teilnehmer"].count_documents({"guildID": str(interaction.guild.id), "channelID": str(interaction.channel.id), "msgID": str(interaction.message.id)})
    
    member = await interaction.guild.fetch_member(int(result['hostID']))
    
    embed = discord.Embed(title=f"🏆 {result['preis']}", description=f"""                                      
<:v_12:1264264683427336259> › __**Informationen**__
<:v_24:1264264867511144479> Erstellt von {member.mention}
<:v_24:1264264867511144479> **{result['winners']}** Gewinner
<:v_24:1264264867511144479> Endet {discord_timestamp(t2, "R")}
<:v_24:1264264867511144479> **{teilnehmer_count}** Teilnehmer

<:v_82:1264266106307215370> › __**Anforderungen**__
<:v_24:1264264867511144479> **Drücke** unten auf **den Button**, um teilzunehmen.""", color=discord.Color.orange())
    
    requirements = ""
    if result["rollenID"]:
        rolle = interaction.guild.get_role(int(result["rollenID"]))
        requirements += f"\n<:v_24:1264264867511144479> Du benötigst die **Rolle {rolle.mention}**."
    if result["nachrichten"]:
        requirements += f"\n<:v_24:1264264867511144479> Du musst mindestens **{result['nachrichten']} neue Nachrichten** schreiben."
    if result["voicezeit"]:
        requirements += f"\n<:v_24:1264264867511144479> Du musst mindestens **{result['voicezeit']} Minuten** in Sprachkanälen verbringen."
    if result["custom_status"]:
        requirements += f"\n<:v_24:1264264867511144479> Du musst **{result['custom_status']}** im Status haben."
    if result["jointime"]:
        requirements += f"\n<:v_24:1264264867511144479> Du musst mindestens seit dem **{result['jointime']}** auf diesem Server sein."
    if result["level"]:
        requirements += f"\n<:v_24:1264264867511144479> Du musst mindestens **Level {result['level']}** bei Vulpos Levelsystem sein."
        
    if requirements != "":
        embed.description += requirements
    embed.set_footer(text="🍀 Viel Glück")
    embed.set_thumbnail(url=interaction.guild.icon)
    await interaction.message.edit(content=interaction.message.content, embed=embed)

           
async def teilnahme_abgelehnt(self, interaction: discord.Interaction, grund, result):
    t2 = datetime.datetime.fromtimestamp(int(result["endtime"]))
    embed = discord.Embed(colour=await getcolour(self, interaction.user), title=result['preis'], description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)

`🎉` · Nicht erfolgreich teilgenommen auf [{interaction.guild.name}]({interaction.message.jump_url})
`⏰` · Das Gewinnspiel endet {discord_timestamp(t2, 'R')}

`❓` · Gründe:
{grund}
""")
    
    embed.set_thumbnail(url=interaction.guild.icon)
    embed.set_image(url="https://media.discordapp.net/attachments/1023508002453594122/1023508199044829294/GW_Pannel_3.png")
    await interaction.followup.send("Deine Teilnahme an einem Gewinnspiel war **nicht erfolgreich**.", embed=embed, ephemeral=True)
    
    
class Gewinnspiel_Teilnehmen(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Teilnehmen', style=discord.ButtonStyle.green, custom_id="dqbckiwluheljvkhgciulehfgk")
    async def teilnehmen(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        member = await interaction.guild.fetch_member(interaction.user.id)
        gründe = ""
        
        db = getMongoDataBase()
        
        result  = await db['gewinnspiele'].find_one({"guildID": str(interaction.guild.id), "channelID": str(interaction.channel.id), "msgID": str(interaction.message.id)})
        #guildID, channelID, msgID, hostID, endtime, preis, winners, status, nachrichten, rollenID, voicezeit, custom_status, jointime
        
        if result is None:
            return
        
        result5 = await db['gewinnspiel_teilnehmer'].find_one({"guildID": str(interaction.guild.id), "channelID": str(interaction.channel.id), "msgID": str(interaction.message.id), "userID": str(interaction.user.id)})
        
        if result5 != None:
            await db['gewinnspiel_teilnehmer'].delete_one({"guildID": str(interaction.guild.id), "channelID": str(interaction.channel.id), "msgID": str(interaction.message.id), "userID": str(interaction.user.id)})
            return await teilnahme_abgelehnt(self, interaction, "`<:v_x:1264270921452224562>` Du warst bereits ein Teilnehmer, hast jedoch nochmal den Button gedrückt. Nun bist du kein Teilnehmer mehr.", result)

        blacklist = await db['gewinnspiel_blacklist'].find({"guildID": str(interaction.guild.id)}).to_list(length=None)

        for id in blacklist:
            rolle = interaction.guild.get_role(int(id["id"]))
            if rolle != None:
                if rolle in member.roles:
                    return await teilnahme_abgelehnt(self, interaction, "`<:v_x:1264270921452224562>` Du stehst auf der Gewinnspiel Blacklist und bist deshalb von jeglichen Gewinnspielen dieses Servers ausgeschlossen.", result)
            if int(id[0]) == interaction.user.id:
                return await teilnahme_abgelehnt(self, interaction, "`<:v_x:1264270921452224562>` Du stehst auf der Gewinnspiel Blacklist und bist deshalb von jeglichen Gewinnspielen dieses Servers ausgeschlossen.", result)
                    
        bypassrollen = await db['gewinnspiele_bypassrolle'].find({"guildID": str(interaction.guild.id)}).to_list(length=None)
        
        for bypassrolle in bypassrollen:
            bpr = interaction.guild.get_role(int(bypassrolle["rollenID"]))
            if bpr == None:
                pass
            if bpr in member.roles:
                
                result4 = await db['gewinnspiel_teilnehmer'].find_one({"guildID": str(interaction.guild.id), "channelID": str(interaction.channel.id), "msgID": str(interaction.message.id), "userID": str(interaction.user.id)})
                
                if result4 != None:
                    await db['gewinnspiel_teilnehmer'].delete_one({"guildID": str(interaction.guild.id), "channelID": str(interaction.channel.id), "msgID": str(interaction.message.id), "userID": str(interaction.user.id)})
                    return await teilnahme_abgelehnt(self, interaction, "`<:v_x:1264270921452224562>` Du warst bereits ein Teilnehmer, hast jedoch nochmal den Button gedrückt. Nun bist du kein Teilnehmer mehr.", result)


                await db['gewinnspiel_teilnehmer'].insert_one({"guildID": str(interaction.guild.id), "channelID": str(interaction.channel.id), "msgID": str(interaction.message.id), "userID": str(interaction.user.id)})
                
                return await teilnahme_angenommen(self, interaction, result)                        


        if result["nachrichten"] is not None:
            result2 = await db['gw_nachrichten'].find_one({"guildID": str(interaction.guild.id), "gwID": str(interaction.message.id), "userID": str(interaction.user.id)})
            
            print(result2)
            
            if result2 is None:
                gründe += f"\n`<:v_x:1264270921452224562>` Du hast bisher 0 Nachrichten geschrieben, benötigst jedoch {result['nachrichten']} Nachrichten um am Gewinnspiel teilzunehmen."
            else:
                nachrichten = result2["anzahl"]
                if nachrichten < int(result["nachrichten"]):
                    gründe += f"\n`<:v_x:1264270921452224562>` Du hast bisher {nachrichten} Nachrichten geschrieben, benötigst jedoch {result['nachrichten']} Nachrichten um am Gewinnspiel teilzunehmen."
                if result["rollenID"] != None:
                    rolle2 = interaction.guild.get_role(int(result["rollenID"]))
                    if rolle2 != None:
                        if rolle2 not in member.roles:
                            gründe += f"\n`<:v_x:1264270921452224562>` Du benötigst die Rolle {rolle2.name} um am Gewinnspiel teilzunehmen."
        
        if result["voicezeit"] != None and result["voicezeit"] != "":
            result2 = await db['gw_voice'].find_one({"guildID": str(interaction.guild.id), "gwID": str(interaction.message.id), "userID": str(interaction.user.id)})
            if result2 == None:
                gründe += f"\n`<:v_x:1264270921452224562>` Du hast bisher 0 Minuten in einem Sprachkanal verbracht, benötigst jedoch {result['voicezeit']} Minuten um am Gewinnspiel teilzunehmen."
            else:
                minuten = int(result2["anzahl"])
                if minuten < int(result["voicezeit"]):
                    gründe += f"\n`<:v_x:1264270921452224562>` Du hast bisher {minuten} Minuten in einem Sprachkanal verbracht, benötigst jedoch {result['voicezeit']} Minuten um am Gewinnspiel teilzunehmen."
        
        if result["custom_status"] != None:
            try:
                member = interaction.guild.get_member(interaction.user.id)
                if str(result["custom_status"]) not in str(member.activity.name):
                    gründe += f"\n`<:v_x:1264270921452224562>` Du musst {result['custom_status']} im Status haben."
            except:
                gründe += f"\n`<:v_x:1264270921452224562>` Du musst {result['custom_status']} im Status haben."

        if result["jointime"] != None:
            join_date = interaction.user.joined_at.replace(tzinfo=pytz.UTC)
            check_date = datetime.datetime.strptime(result["jointime"], '%d.%m.%Y').replace(tzinfo=pytz.UTC)
            if join_date > check_date:
                gründe += f"\n`<:v_x:1264270921452224562>` Du musst vor dem {result['jointime']} gejoint sein, bist aber am {join_date} gejoint."

        if result["level"] != None:
            r = await db['levelsystem'].find_one({"client_id": str(interaction.user.id), "guild_id": str(interaction.guild.id)})
            
            if r is None:
                gründe += f"\n`<:v_x:1264270921452224562>` Du bist hier Level 0, benötigst jedoch Level {result['level']} um am Gewinnspiel teilzunehmen."
            else:
                if int(r["user_level"]) < int(result["level"]):
                    gründe += f"\n`<:v_x:1264270921452224562>` Du bist hier Level {r['user_level']}, benötigst jedoch Level {result['level']} um am Gewinnspiel teilzunehmen."
        if gründe != "":
            return await teilnahme_abgelehnt(self, interaction, gründe, result)
        
        await db["gewinnspiel_teilnehmer"].insert_one({"guildID": str(interaction.guild.id), "channelID": str(interaction.channel.id), "msgID": str(interaction.message.id), "userID": str(interaction.user.id)})
        
        await teilnahme_angenommen(self, interaction, result)

    
class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild is None:
            return
        if msg.author.bot:
            return
        
        db = getMongoDataBase()
        
        result2 = await db["gewinnspiele"].find({"guildID": str(msg.guild.id), "status": "Aktiv"}).to_list(length=None)
        
        if len(result2) == 0:
            return
        
        for gewinnspiel in result2:
            result = await db["gw_nachrichten"].find_one({"guildID": str(msg.guild.id), "userID": str(msg.author.id), "gwID": str(gewinnspiel["msgID"])})
            
            if result is None:
                await db["gw_nachrichten"].insert_one({"guildID": str(msg.guild.id), "userID": str(msg.author.id), "gwID": str(gewinnspiel["msgID"]), "anzahl": 1})
            else:
                await db["gw_nachrichten"].update_one({"guildID": str(msg.guild.id), "userID": str(msg.author.id), "gwID": str(gewinnspiel["msgID"])}, {"$inc": {"anzahl": 1}})
            
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=Gewinnspiel_Teilnehmen(self.bot))
                
    gewinnspiel = app_commands.Group(name='gewinnspiel', description='Verwalte Gewinnspiele.', guild_only=True)
    
    @gewinnspiel.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def starten(self, interaction: discord.Interaction, preis: str, kanal: discord.TextChannel, gewinneranzahl: typing.Literal[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90], endzeit: str, rolle: discord.Role=None, nachrichtenanzahl: int=None, voiceminuten: int=None, text_im_status: str=None, joindatum: str=None, level: int=None):
        """Starte ein Gewinnspiel."""
        
        await interaction.response.defer()
        
        if joindatum:
            try:
                check_date = datetime.datetime.strptime(joindatum, '%d.%m.%Y').replace(tzinfo=pytz.UTC)
            except Exception as e:
                return await interaction.followup.send(f"**Bitte gib ein Datum an. Bsp: 12.6.2023** {e}", ephemeral=True)

        if voiceminuten:
            if voiceminuten > 300:
                return await interaction.followup.send("**Das Maximum für Voiceminuten liegt bei 300 Minuten. Bitte überschreite diese Grenze nicht.**", ephemeral=True)
        if nachrichtenanzahl:
            if nachrichtenanzahl > 10000:
                return await interaction.followup.send("**Das Maximum für eine Mindestnachrichtenanzahl liegt bei 10000. Bitte überschreite diese Grenze nicht.**", ephemeral=True)
        zeit = convert(endzeit)
        if zeit == None:
            return await interaction.followup.send("**Du musst auch eine Zeit angeben, wann das Gewinnspiel enden soll. Du kannst s, m, h, d, w verwenden, um den Zeitraum zu definieren. Beispiel: '1w 3d 5h' oder '2d 45s'.**", ephemeral=True)
        t1 = math.floor(datetime.datetime.now().timestamp() + zeit)
        t2 = datetime.datetime.fromtimestamp(int(t1))

        requirements = ""
        if rolle:
            requirements += f"\n<:v_24:1264264867511144479> Du benötigst die **Rolle {rolle.mention}**."
        if nachrichtenanzahl:
            requirements += f"\n<:v_24:1264264867511144479> Du musst mindestens **{nachrichtenanzahl} neue Nachrichten** schreiben."
        if voiceminuten:
            requirements += f"\n<:v_24:1264264867511144479> Du musst mindestens **{voiceminuten} Minuten** in Sprachkanälen verbringen."
        if text_im_status:
            requirements += f"\n<:v_24:1264264867511144479> Du musst **{text_im_status}** im Status haben."
        if joindatum:
            requirements += f"\n<:v_24:1264264867511144479> Du musst mindestens seit dem **{joindatum}** auf diesem Server sein."
        if level:
            requirements += f"\n<:v_24:1264264867511144479> Du musst mindestens **Level {level}** bei Vulpos Levelsystem sein."

        embed = discord.Embed(title=f"🏆 {preis}", description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)
                                      
<:v_12:1264264683427336259> › __**Informationen**__
<:v_24:1264264867511144479> Erstellt von {interaction.user.mention}
<:v_24:1264264867511144479> **{gewinneranzahl}** Gewinner
<:v_24:1264264867511144479> Endet {discord_timestamp(t2, "R")}
<:v_24:1264264867511144479> **0** Teilnehmer

<:v_82:1264266106307215370> › __**Anforderungen**__
<:v_24:1264264867511144479> **Drücke** unten auf **den Button**, um teilzunehmen.""", color=discord.Color.orange())
        
        if requirements != "":
            embed.description += requirements
        embed.set_footer(text="🍀 Viel Glück")
        embed.set_thumbnail(url=interaction.guild.icon)

        m = await kanal.send("**🎊 Neues Gewinnspiel 🎊**", embed=embed, view=Gewinnspiel_Teilnehmen(self.bot))
        asyncio.create_task(giveaway_end(t2, self.bot, m.id))
                
                
        db = getMongoDataBase()

        if rolle:
            await db["gewinnspiele"].insert_one({"guildID": str(interaction.guild.id), "channelID": str(kanal.id), "msgID": str(m.id), "hostID": str(interaction.user.id), "endtime": t1, "preis": preis, "winners": gewinneranzahl, "status": "Aktiv", "nachrichten": nachrichtenanzahl, "rollenID": str(rolle.id), "voicezeit": voiceminuten, "custom_status": text_im_status, "jointime": joindatum, "level": level})
        else:
            await db["gewinnspiele"].insert_one({"guildID": str(interaction.guild.id), "channelID": str(kanal.id), "msgID": str(m.id), "hostID": str(interaction.user.id), "endtime": t1, "preis": preis, "winners": gewinneranzahl, "status": "Aktiv", "nachrichten": nachrichtenanzahl, "rollenID": None, "voicezeit": voiceminuten, "custom_status": text_im_status, "jointime": joindatum, "level": level})
            
        await interaction.followup.send(f"**Das Gewinnspiel findet nun statt in {kanal.mention}.**", ephemeral=True)

    @gewinnspiel.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def verwalten(self, interaction: discord.Interaction, aktion: typing.Literal["Gewinnspiel beenden (Nachrichten ID erforderlich)","Gewinnspiel neu würfeln (Nachrichten ID erforderlich)","Gewinnspiele anzeigen", "Teilnehmer einsehen (Nachrichten ID erforderlich)"], nachrichtenid: str=None):
        """Verwalte Gewinnspiele."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        #guildID, channelID, msgID, hostID, endtime, preis, winners, status, nachrichten, rollenID, voicezeit, custom_status, jointime, level
        if aktion == "Teilnehmer einsehen (Nachrichten ID erforderlich)":
            if nachrichtenid is None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Du musst eine Nachrichten ID mit angeben beim Befehl.**", ephemeral=True)
            result = await db['gewinnspiele'].find_one({"guildID": str(interaction.guild.id), "msgID": nachrichtenid, "status": "Aktiv"})
            if result == None:
                return await interaction.followup.send(f"**<:v_x:1264270921452224562> Es wurde kein aktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem aktiven Gewinnspiel handelt**", ephemeral=True)
            kanal = interaction.guild.get_channel(int(result["channelID"]))
            if kanal == None:
                return await interaction.followup.send(f"**<:v_x:1264270921452224562> Es wurde kein aktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem aktiven Gewinnspiel handelt**", ephemeral=True)
            nachricht = await kanal.fetch_message(int(nachrichtenid))
            if nachricht == None:
                return await interaction.followup.send(f"**<:v_x:1264270921452224562> Es wurde kein aktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem aktiven Gewinnspiel handelt**", ephemeral=True)
                    
            result2 = await db['gewinnspiel_teilnehmer'].find({"guildID": str(interaction.guild.id), "msgID": nachrichtenid}).to_list(length=None)         
            if result2 is None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Bei diesem Gewinnspiel gibt es bisher noch keine Teilnehmer.**", ephemeral=True)

            embed = discord.Embed(colour=await getcolour(self, interaction.user), title=f"Teilnehmer vom Gewinnspiel {nachrichtenid}", description="Alle Teilnehmer dieses aktiven Gewinnspiels findest du in dieser Liste. Hier kannst du als Beispiel Zweitaccounts von Gewinnspielen verbannen.")
                        
            embed.description += "\n\n__Alle Teilnehmer:__"
            for teilnehmer in result2:
                user = self.bot.get_user(int(teilnehmer['userID']))
                if user is not None:
                    embed.description += f"\n{user.name}"
                else:
                    embed.description += f"\n**{teilnehmer['userID']}** (Server verlassen?) ||Tipp: Von Gewinnspielen blockieren, damit er nicht mehr gewinnen kann.||"
            return await interaction.followup.send(embed=embed)

        if aktion == "Gewinnspiel beenden (Nachrichten ID erforderlich)":
            if nachrichtenid is None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Du musst eine Nachrichten ID mit angeben beim Befehl.**", ephemeral=True)
            result = await db['gewinnspiele'].find_one({"guildID": str(interaction.guild.id), "msgID": nachrichtenid, "status": "Aktiv"})
            if result == None:
                return await interaction.followup.send(f"**<:v_x:1264270921452224562> Es wurde kein aktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem aktiven Gewinnspiel handelt**", ephemeral=True)
            kanal = interaction.guild.get_channel(int(result["channelID"]))
            if kanal == None:
                return await interaction.followup.send(f"**<:v_x:1264270921452224562> Es wurde kein aktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem aktiven Gewinnspiel handelt**", ephemeral=True)
            nachricht = await kanal.fetch_message(int(nachrichtenid))
            if nachricht == None:
                return await interaction.followup.send(f"**<:v_x:1264270921452224562> Es wurde kein aktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem aktiven Gewinnspiel handelt**", ephemeral=True)
            
            await interaction.followup.send("**<:v_checkmark:1264271011818242159> Gewinnspiel wird beendet.**")
            return await giveaway_end(datetime.datetime.now(), self.bot, nachricht.id, "Beenden")
                
        if aktion == "Gewinnspiel neu würfeln (Nachrichten ID erforderlich)":
            if nachrichtenid is None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Du musst eine Nachrichten ID mit angeben beim Befehl.**", ephemeral=True)
            result2 = await db['gewinnspiele'].find_one({"guildID": str(interaction.guild.id), "msgID": nachrichtenid, "status": "Inaktiv"})
            if result2 == None:
                return await interaction.followup.send(f"**<:v_x:1264270921452224562> Es wurde kein inaktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem inaktiven Gewinnspiel handelt**", ephemeral=True)
            kanal2 = interaction.guild.get_channel(int(result2["channelID"]))
            if kanal2 == None:
                return await interaction.followup.send(f"**<:v_x:1264270921452224562> Es wurde kein inaktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem inaktiven Gewinnspiel handelt**", ephemeral=True)
            nachricht2 = await kanal2.fetch_message(int(nachrichtenid))
            if nachricht2 == None:
                return await interaction.followup.send(f"**<:v_x:1264270921452224562> Es wurde kein inaktives Gewinnspiel mit der ID {nachrichtenid} auf diesem Server gefunden. Beachte, dass es sich bei der ID um die ID der Nachricht von einem inaktiven Gewinnspiel handelt**", ephemeral=True)
            t1 = math.floor(datetime.datetime.now().timestamp() + 1)
            t2 = datetime.datetime.fromtimestamp(int(t1))
            await interaction.followup.send("**<:v_checkmark:1264271011818242159> Gewinnspiel wird neu ausgelost.**")
            return await giveaway_end(t2, self.bot, nachricht2.id, "Reroll")
            
        if aktion == "Gewinnspiele anzeigen":
            result3 = await db['gewinnspiele'].find({"guildID": str(interaction.guild.id), "status": "Aktiv"}).to_list(length=None)
            if len(result3) == 0:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Es gibt keine aktiven Gewinnspiele auf diesem Server.**", ephemeral=True)
            
            embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Gewinnspiele", description="Alle aktiven Gewinnspiele von diesem Server findest du in dieser Nachricht.")
            
            for gewinnspiel in result3:
                kanal3 = interaction.guild.get_channel(int(gewinnspiel["channelID"]))
                
                if kanal3 == None:
                    continue
                
                nachricht3 = await kanal3.fetch_message(int(gewinnspiel["msgID"]))
                
                if nachricht3 == None:
                    continue
                
                t2 = datetime.datetime.fromtimestamp(int(gewinnspiel["endtime"]))
                embed.add_field(name=f"{gewinnspiel['preis']} ({gewinnspiel['msgID']})", value=f"Das Gewinnspiel endet {discord_timestamp(t2, 'R')}.", inline=False)
            return await interaction.followup.send(embed=embed)

    @gewinnspiel.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def bypassrolle(self, interaction: discord.Interaction, aktion: typing.Literal["Hinzufügen (Rolle erforderlich)","Entfernen (Rolle erforderlich)","Alle anzeigen"], rolle: discord.Role=None):
        """Bearbeite Rollen, die die Bedingungen umgehen."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        #guildID, channelID, msgID, hostID, endtime, preis, winners, status, nachrichten, rollenID, voicezeit, custom_status, jointime, level
        if aktion == "Hinzufügen (Rolle erforderlich)":
            if rolle == None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Du musst natürlich auch eine Rolle angeben im Command.**", ephemeral=True)
            result = await db['gewinnspiele_bypassrolle'].find_one({"guildID": str(interaction.guild.id), "rollenID": rolle.id})
            if result != None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Diese Bypassrolle existiert bereits.**", ephemeral=True)
            await db["gewinnspiele_bypassrolle"].insert_one({"guildID": str(interaction.guild.id), "rollenID": rolle.id})
            return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Rolle ist nun eine Bypassrolle.**")
        if aktion == "Entfernen (Rolle erforderlich)":
            if rolle == None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Du musst natürlich auch eine Rolle angeben im Command.**", ephemeral=True)
            result2 = await db['gewinnspiele_bypassrolle'].find_one({"guildID": str(interaction.guild.id), "rollenID": rolle.id})
            if result2 == None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Diese Bypassrolle existiert nicht.**", ephemeral=True)
            await db['gewinnspiele_bypassrolle'].delete_one({"guildID": str(interaction.guild.id), "rollenID": rolle.id})
            return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Rolle ist nun keine Bypassrolle mehr.**")
        if aktion == "Alle anzeigen":
            result3 = await db['gewinnspiele_bypassrolle'].find({"guildID": str(interaction.guild.id)}).to_list(length=None)
            if result3 == None:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Auf diesem Server gibt es keine Bypassrollen.**", ephemeral=True)
            
            bypasses = ""
            
            for rolle in result3:
                rolle2 = interaction.guild.get_role(int(rolle["rollenID"]))
                
                if rolle2 == None:
                    continue
                
                bypasses += rolle2.mention + "\n"
            
            embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Gewinnspiele", description=f"""
Die User mit diesen Rollen sind von Anforderungen von Gewinnspielen dieses Servers ausgeschlossen.

{bypasses}
""")
            await interaction.followup.send(embed=embed)
        
    @gewinnspiel.command()
    @app_commands.checks.has_permissions()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def blockieren(self, interaction: discord.Interaction, id: str):
        """Setze Member und Rollen auf die Blacklist."""
        
        await interaction.response.defer()
        
        rolle = interaction.guild.get_role(int(id))

        member = None
        
        try:
            member = await self.bot.fetch_user(int(id))
        except:
            pass
        
        if member == None and rolle == None:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Die ID muss entweder eine Rollen ID oder eine Member ID sein.**", ephemeral=True)

        db = getMongoDataBase()

        if member:
            result = await db['gewinnspiel_blacklist'].find_one({"guildID": str(interaction.guild.id), "id": id})
            if result == None:
                await db['gewinnspiel_blacklist'].insert_one({"guildID": str(interaction.guild.id), "id": id})
                await db['gewinnspiel_teilnehmer'].delete_many({"guildID": str(interaction.guild.id), "userID": id})
                return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> {member} ist nun auf der Blacklist**")
            await db['gewinnspiel_blacklist'].delete_one({"guildID": str(interaction.guild.id), "id": id})
            return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> {member} ist nun nicht mehr auf der Blacklist**")
        if rolle:
            result = await db['gewinnspiel_blacklist'].find_one({"guildID": str(interaction.guild.id), "id": id})
            if result == None:
                await db['gewinnspiel_blacklist'].insert_one({"guildID": str(interaction.guild.id), "id": id})
                for member in interaction.guild.members:
                    if rolle in member.roles:
                        await db['gewinnspiel_teilnehmer'].delete_many({"guildID": str(interaction.guild.id), "userID": str(member.id)})
                return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> {rolle.name} ist nun auf der Blacklist**")
            await db['gewinnspiel_blacklist'].delete_one({"guildID": str(interaction.guild.id), "id": id})
            return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> {rolle.name} ist nun nicht mehr auf der Blacklist**")
        
async def setup(bot):
    await bot.add_cog(giveaway(bot))