import discord
import datetime
from typing import Literal
import random
import datetime
import math
import asyncio
from utils.MongoDB import getMongoDataBase

class NewTimerName(discord.ui.View):
    def __init__(self, bot=None, beschreibung=None, zeit=None, embed=None):
        super().__init__(timeout=None)
        self.bot = bot
        self.beschreibung = beschreibung
        self.zeit = zeit
        self.embed = embed

    @discord.ui.button(label='Erneute Erinnerung mit gleicher Zeit', style=discord.ButtonStyle.green, custom_id="NewTimerName", emoji="🔁")
    async def newtimerName(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NameModal(bot=self.bot, letzte_beschreibung=self.beschreibung, zeit=self.zeit, button=button, view=self, embed=self.embed))

class NameModal(discord.ui.Modal, title="Beschreibung für Erinnerung"):
    beschreibung = discord.ui.TextInput(
            label="Beschreibung",
            placeholder="",
    )
    
    def __init__(self, bot=None, letzte_beschreibung=None, zeit=None, button=None, view=None, embed=None):
        super().__init__(title='Beschreibung für Erinnerung')
        self.letzte_beschreibung = letzte_beschreibung
        self.zeit = zeit
        self.bot = bot
        self.beschreibung.placeholder = letzte_beschreibung
        self.button = button
        self.view = view
        self.embed = embed

    async def on_submit(self, interaction: discord.Interaction):
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        t1 = math.floor(datetime.datetime.now().timestamp() + int(self.zeit))
        t2 = datetime.datetime.fromtimestamp(int(t1))
        
        id = await db["erinnerungen"].count_documents({}) + 1
        
        await db["erinnerungen"].insert_one({"userID": interaction.user.id, "endtime": t1, "zeit": self.zeit, "beschreibung": self.beschreibung.value, "id": id})
        
        embed = discord.Embed(color=await getcolour(self, interaction.user), title=f"Erinnerung gestellt (ID {id})", description=f"""
<:v_12:1264264683427336259> Erinnerung gesetzt auf {discord_timestamp(t2, 'f')}
<:v_24:1264264867511144479> {self.beschreibung.value}""")
        
        
        asyncio.create_task(reminder_end(t2, self.bot, interaction.user.id, id), name=f"Erinnerung - {id}")
        await interaction.followup.send(embed=embed)
                
        self.button.disabled = True
        await interaction.edit_original_response(embed=self.embed, view=self.view)

async def haspremium(self, user):
    db = getMongoDataBase()
    
    premium = await db["premium"].find_one({"userID": user.id})
    
    if premium == None:
        return False
    
    return premium["status"]

async def haspremium_forserver(self, guild):
    db = getMongoDataBase()
    
    premium = await db["premium"].find_one({"userID": guild.owner.id})
    
    if premium == None:
        return False
    
    return premium["status"]
            
async def getcolour(self, user):
    db = getMongoDataBase()
    
    premium = await db["premium"].find_one({"userID": user.id})
    
    if premium == None:
        return discord.Colour.orange()
    
    if premium["status"] == False:
        return discord.Colour.orange()
    
    farbe = await db["embedfarben"].find_one({"userID": user.id})
    
    if farbe == None:
        return discord.Colour.orange()
    
    return discord.Colour(int(farbe["farbe"], 16))

async def getLevelSystemEnabled(self, guild):
    
    db = getMongoDataBase()
    
    enabled = await db["levelstatus"].find_one({"guild": guild.id})
    
    if enabled == None:
        await db["levelstatus"].insert_one({"guild": guild.id, "enabled": False})
        return False
    
    return enabled["enabled"]

async def voicetime_to_xp(self, member, time, before):
    if member.bot:
        return
    
    db = getMongoDataBase()
    
    if await getLevelSystemEnabled(self, member.guild) == False:
        return
    
    blocked_roles = await db["lb_rollen"].find({"guild": member.guild.id})
    
    for r_id in blocked_roles:
        rolle = member.guild.get_role(int(r_id["role"]))
        if rolle:
            if rolle in member.roles:
                return
    
    blocked_channel = await db["lb_channel"].find({"guild": member.guild.id})
    
    for c_id in blocked_channel:
        if int(c_id["channel"]) == int(before.channel.id):
            return
        
    newxp = random.randint(15, 30) * time
    
    xpboost = await db["xpboost"].find_one({"guild": member.guild.id})
    
    if xpboost != None and xpboost["status"]:
            newxp += newxp * 2
            
    userdata = await db["levelsystem"].find_one({"client": member.id, "guild": member.guild.id})
    
    if userdata == None:
        await db["levelsystem"].insert_one({"client": member.id, "xp": newxp, "level": 0, "guild": member.guild.id})
        return
            
    await db["levelsystem"].update_one({"client": member.id, "guild": member.guild.id}, {"$set": {"xp": userdata["xp"] + newxp}})
                
def limit_characters(string: str, limit: int):
    if len(string) > limit:
        return string[:limit-3] + "..."
    return string

def random_color():
    return discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

async def addwarn(self, user, interaction, grund):
    db = getMongoDataBase()
    warns = await db["warns"].find_one({"guildID": interaction.guild.id, "client": user.id})
    
    if warns == None:
        await db["warns"].insert_one({"guild": interaction.guild.id, "client": user.id, "warns": [{"grund": grund + f"\n`Verwarnung erstellt am {discord.utils.utcnow().__format__('%d.%m.%Y')}`", "time": datetime.datetime.now()}]})
        return await automod(self, user, interaction.guild, 1, interaction)
    
    warnID = len(warns["warns"]) + 1
    await db["warns"].update_one({"guild": interaction.guild.id, "client": user.id}, {"$push": {"warns": {"grund": grund, "time": datetime.datetime.now()}}})
    await automod(self, user, interaction.guild, warnID, interaction)

async def automod(self, user, guild, warnanzahl, interaction):
    db = getMongoDataBase()
    actions = await db["automod"].find_one({"guildID": guild.id, "warnanzahl": warnanzahl})

    if(actions == None):
        return
    
    if "Timeout" in actions["aktion"]:
        time_end = discord.utils.utcnow()
        dt = time_end + datetime.timedelta(seconds=int(actions["time"]))
        await user.timeout(dt ,reason="Automod wurde ausgelöst")
        await interaction.channel.send(f"🚨 **Der Benutzer {user.mention} wurde für {int(actions['time'])} Sekunden getimeoutet.** 🚨\nGrund: Automod wurde ausgelöst ({warnanzahl} Verwarnungen).")
        
    if actions["aktion"] == "Kick":
        await user.kick(reason="Automod wurde ausgelöst")
        await interaction.channel.send(f"🚨 **Der Benutzer {user.mention} wurde gekickt.** 🚨\nGrund: Automod wurde ausgelöst ({warnanzahl} Verwarnungen).")
    
    if actions["aktion"] == "Ban":
        await user.ban(reason="Automod wurde ausgelöst")
        await interaction.channel.send(f"🚨 **Der Benutzer {user.mention} wurde gebannt.** 🚨\nGrund: Automod wurde ausgelöst ({warnanzahl} Verwarnungen).")

def check_member_role(member, role):
    if role in member.roles:
        return True
    else:
        return False

async def reminder_end(when: datetime.datetime, bot, user_id, id):
    await bot.wait_until_ready()
    await discord.utils.sleep_until(when=when)
    
    db = getMongoDataBase()
    user = await bot.fetch_user(user_id)
    
    if not user:
        await db["erinnerungen"].delete_one({"userID": user_id, "id": id})
        return
    
    result = await db["erinnerungen"].find_one({"userID": user_id, "id": id})
    if result == None:
        return
    
    await db["erinnerungen"].delete_one({"userID": user_id, "id": id})
    embed = discord.Embed(title="<:v_65:1264265724386480148> Timer abgelaufen", description=result["beschreibung"], color=discord.Color.green())
    
    try:
        await user.send(embed=embed, view=NewTimerName(bot, result["beschreibung"], result["zeit"], embed))
    except:
        pass
                
async def vote_reminder(when: datetime.datetime, bot, user_id):
    await bot.wait_until_ready()
    await discord.utils.sleep_until(when=when)
    
    db = getMongoDataBase()
    
    guild = await bot.fetch_guild(925729625580113951)
    rolle = await guild.fetch_role(1041046601394815127)
    user = await bot.fetch_user(user_id)
    member = await guild.fetch_member(int(user_id))
    voter = await guild.fetch_role(962753309997932554)
    
    db["vote"].delete_many({"userid": user_id})
    
    if not member:
        return
    
    embed = discord.Embed(title="Du kannst voten", url="https://top.gg/bot/925799559576322078/vote", description="""
<:v_65:1264265724386480148> Der Vote-Cooldown von 12 Stunden ist abgelaufen. Es wäre sehr schön, wenn du wieder für mich votest.
<:herz:941398727501955113> Als Belohnung für einen weiteren Vote bekommst du **300 🍪 im Economy System** und eine besondere **Rolle in [Vulpos Wald](https://discord.gg/49jD3VXksp)**

<:v_12:1264264683427336259> Du kannst Vote Erinnerungen in <#926224205639467108> ausschalten.""", colour=discord.Colour.green())
    
    embed.set_footer(text="Danke für deine Unterstützung", icon_url="https://media.discordapp.net/attachments/965302660871884840/965315155816767548/Vulpo_neu.png?width=1572&height=1572")      
    await member.remove_roles(voter)
    try:
        if rolle in member.roles:
            await user.send(embed=embed)
    except:
        pass
            

async def giveaway_end(when: datetime.datetime, bot, msgID, status=None):
    await bot.wait_until_ready()
    await discord.utils.sleep_until(when=when)
    db = getMongoDataBase()
    
    if(status == None):
        result = await db["gewinnspiele"].find_one({"msgID": msgID, "status": "Aktiv"})
    if(status == "Beenden"):
        result = await db["gewinnspiele"].find_one({"msgID": msgID, "status": "Aktiv"})
    if(status == "Reroll"):
        result = await db["gewinnspiele"].find_one({"msgID": msgID, "status": "Inaktiv"})
        
    if result == None:
        return
    
    guild = await bot.fetch_guild(result["guildID"])
    kanal = await guild.fetch_channel(result["channelID"])
    msg = await kanal.fetch_message(msgID)
    
    if guild == None or kanal == None or msg == None:
        return
    
    await db["gewinnspiele"].update_one({"guildID": guild.id, "channelID": kanal.id, "msgID": msgID}, {"$set": {"status": "Inaktiv"}})
    t1 = int(datetime.datetime.now().timestamp())
    t2 = datetime.datetime.fromtimestamp(int(t1))
    
    participantResults = await db["gewinnspiel_teilnehmer"].find({"guildID": guild.id, "channelID": kanal.id, "msgID": msgID})
    
    if participantResults == None:
        await msg.reply("😢 Es gab leider keine Teilnehmer. Niemand hat gewonnen.")
        embed = discord.Embed(title=f"🏆 {result['gewinn']}", description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)
        
<:v_165:1264268434783604777>
› __**Wer hat gewonnen?**__
<:v_24:1264264867511144479> Niemand hat gewonnen.
<:v_24:1264264867511144479> Das Gewinnspiel endete {discord_timestamp(t2, 'R')}
<:v_24:1264264867511144479> Es gab 0 Teilnehmer.""", color=discord.Color.red())
        
        embed.set_thumbnail(url=msg.guild.icon)
        
        return await msg.edit(content="**⛔️ Gewinnspiel beendet ⛔️**", embed=embed, view=None)
    
    participants = [userid["userID"] for userid in participantResults]
    winner = random.sample(participants, k=len(participants) if len(participants) < result["gewinner"] else result["gewinner"])
    winners = ""
    
    for win in winner:
        member = await guild.fetch_member(int(win))
        
        embed = discord.Embed(colour=discord.Color.gold(), title=result["gewinn"], description=f"""
`🎉` · Gewonnen auf [{guild.name}]({msg.jump_url})
`⏰` · Das Gewinnspiel endete {discord_timestamp(t2, 'R')}
""")
        
        embed.set_thumbnail(url=guild.icon)
                
        try:
            await member.send("Du hast ein Gewinnspiel **gewonnen**!", embed=embed)
        except:
            pass
        if winners == "":
            winners += f"{member.mention}"
        else:
            winners += f", {member.mention}"
            
    await msg.reply(f"{winners} {'hat' if len(winner) == 1 else 'haben'} {result['gewinn']} gewonnen.")
    
    embed = discord.Embed(title=f"🏆 {result[10]}", description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)
        
<:v_165:1264268434783604777>
› __**Wer hat gewonnen?**__
<:v_24:1264264867511144479> {winners} {'hat' if len(winner) == 1 else 'haben'} {result[10]} gewonnen.
<:v_24:1264264867511144479> Das Gewinnspiel endete {discord_timestamp(t2, 'R')}
<:v_24:1264264867511144479> Es gab {len(participantResults)} Teilnehmer.""", color=discord.Color.red())
    embed.set_footer(text=f"🍀 Die Wahrscheinlichkeit zu gewinnen lag bei {round((int(result[5]) / len(participantResults)) * 100)}%")
    embed.set_thumbnail(url=msg.guild.icon)
    await msg.edit(content="**⛔️ Gewinnspiel beendet ⛔️**", embed=embed, view=None)
                

def discord_timestamp(dt: datetime.datetime, style: Literal["t", "T", "d", "D", "f", "F", "R"] = "f") -> str:
    return f"<t:{str(round(dt.timestamp()))}:{style}>"

def convert(time):
    try:
        t = time.split(' ')
        summe = 0
        for tim in t:
            if "s" in str(tim):
                add = int(tim[:-1]) * 1
                summe += add
            if "m" in str(tim):
                add = int(tim[:-1]) * 60
                summe += add
            if "h" in str(tim):
                add = int(tim[:-1]) * 3600
                summe += add
            if "d" in str(tim):
                add = int(tim[:-1]) * 3600*24
                summe += add
            if "w" in str(tim):
                add = int(tim[:-1]) * 3600*24*7
                summe += add
        if int(summe) >= 1:
            return summe
        else:
            return None
    except:
        return None

async def levelup_role_check(bot, guild, user, newlevel):
    
    db = getMongoDataBase()
    
    rollen = await db["levelroles"].find_one({"guild_id": guild.id, "level": newlevel})
    
    if rollen == None:
        return None
    
    for r_id in rollen["roleid"]:
        r_objekt = await guild.fetch_guild(int(r_id))
        if r_objekt:
            if r_objekt not in user.roles:
                await user.add_roles(r_objekt)
                return r_objekt
            else:
                return None
        else:
            return None
    
async def send_error(title, description, interaction):
    embed = discord.Embed(colour=discord.Colour.red(), title=title, description=description)
    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
    
    try:
        await interaction.followup.send(embed=embed, ephemeral=True)
    except Exception as e:
        print(e)
        try:
            await interaction.followup.send("**<:v_9:1264264656831119462> Mir fehlt die Berechtigung 'Nachrichten einbetten'.**", ephemeral=True)
        except:
            pass

async def get_lang(bot, guild):
    
    db = getMongoDataBase()
    
    lang = await db["sprachen"].find_one({"guildID": guild.id})
    
    return lang or "de"
