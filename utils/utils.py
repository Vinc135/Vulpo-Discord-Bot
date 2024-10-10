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
        
        await db["erinnerungen"].insert_one({"userID": str(interaction.user.id), "endtime": t1, "zeit": self.zeit, "beschreibung": self.beschreibung.value, "id": id})
        
        embed = discord.Embed(color=await getcolour(self, interaction.user), title=f"Erinnerung gestellt (ID {id})", description=f"""
<:v_12:1264264683427336259> Erinnerung gesetzt auf {discord_timestamp(t2, 'f')}
<:v_24:1264264867511144479> {self.beschreibung.value}""")
        
        
        asyncio.create_task(reminder_end(t2, self.bot, interaction.user.id, id), name=f"Erinnerung - {id}")
        await interaction.followup.send(embed=embed)
                
        self.button.disabled = True
        await interaction.edit_original_response(embed=self.embed, view=self.view)

async def haspremium(self, user):
    db = getMongoDataBase()
    
    premium = await db["premium"].find_one({"userID": str(user.id)})
    
    if premium == None:
        return False
    
    return premium["status"]

async def haspremium_forserver(self, guild):
    db = getMongoDataBase()
    
    premium = await db["premium"].find_one({"userID": str(guild.owner.id)})
    
    if premium == None:
        return False
    
    return premium["status"]
            
async def getcolour(self, user):
    db = getMongoDataBase()
    
    premium = await db["premium"].find_one({"userID": str(user.id)})
    
    if premium == None:
        return discord.Colour.orange()
    
    if premium["status"] == False:
        return discord.Colour.orange()
    
    farbe = await db["embedfarben"].find_one({"userID": str(user.id)})
    
    if farbe == None:
        return discord.Colour.orange()
    
    return discord.Colour(int(farbe["farbe"], 16))

async def getLevelSystemEnabled(self, guild):
    
    db = getMongoDataBase()
    
    enabled = await db["levelstatus"].find_one({"guildID": str(guild.id)})
    
    if enabled == None:
        await db["levelstatus"].insert_one({"guildID": str(guild.id), "status": "0"})
        return False
    
    return enabled["status"] == "1"

async def voicetime_to_xp(self, member, time, before):
    if member.bot:
        return
    
    db = getMongoDataBase()
    if await getLevelSystemEnabled(self, member.guild) == False:
        return
    
    blocked_roles = await db["lb_rollen"].find({"guild_id": str(member.guild.id)}).to_list(length=None)
    for r_id in blocked_roles:
        rolle = member.guild.get_role(int(r_id["role"]))
        if rolle:
            if rolle in member.roles:
                return
    
    blocked_channel = await db["lb_channel"].find({"guild_id": str(member.guild.id)}).to_list(length=None)
    
    for c_id in blocked_channel:
        if int(c_id["channel"]) == int(before.channel.id):
            return
        
    newxp = random.randint(15, 30) * time
    
    xpboost = await db["xpboost"].find_one({"guildID": str(member.guild.id)})
    
    if xpboost != None and xpboost["status"]:
        newxp += newxp * 2
            
    userdata = await db["levelsystem"].find_one({"client_id": str(member.id), "guild_id": str(member.guild.id)})
    
    if userdata == None:
        await db["levelsystem"].insert_one({"client_id": str(member.id), "user_xp": newxp, "user_level": 0, "guild_id": str(member.guild.id)})
        return
            
    await db["levelsystem"].update_one({"client_id": str(member.id), "guild_id": str(member.guild.id)}, {"$set": {"user_xp": userdata["user_xp"] + newxp}})
    ###
    xp_start = int(userdata["user_xp"])
    lvl_start = int(userdata["user_level"])
    xp_end = 5 * (math.pow(lvl_start , 2)) + (50 * lvl_start) + 100
    #################################################################################################### XP BOOST
    await db['levelsystem'].update_one({"client_id": str(member.id), "guild_id": str(member.id)}, {"$set": {"user_xp": xp_start + newxp}})
    
    if xp_end < (xp_start + newxp):
        await db['levelsystem'].update_one({"client_id": str(member.id), "guild_id": str(member.guild.id)}, {"$set": {"user_level": lvl_start + 1}})
        await db['levelsystem'].update_one({"client_id": str(member.id), "guild_id": str(member.guild.id)}, {"$set": {"user_xp": 1}})
        result = await db["levelup"].find_one({"guild_id": str(member.guild.id)})

        nachricht = ""
        neue_levelrolle = await levelup_role_check(self.bot, member.guild, member, int(lvl_start) + 1)

        if result and "message" in result:
            nachricht = result["message"].replace("%member", str(member.mention)).replace("%level", str(int(lvl_start) + 1))
        else:
            if neue_levelrolle == None:
                nachricht = f"🎉 Glückwunsch {member.mention}! Du hast Level {int (lvl_start) + 1} erreicht."
            else:
                nachricht = f"🎉 Glückwunsch {member.mention}! Du hast Level {int (lvl_start) + 1} erreicht.\nViel Spaß mit deiner neuen Levelrolle **{neue_levelrolle.name}**."
        
        if result and "channel_id" in result:
            if result["channel_id"] == "Privat":
                return await member.send(nachricht)
        
            if result["channel_id"] != None or result["channel_id"] != "Normal":
                kanal = await member.guild.fetch_channel(int(result["channel_id"]))
                
                if kanal == None:
                    return
                
        await kanal.send(nachricht)




def limit_characters(string: str, limit: int):
    if len(string) > limit:
        return string[:limit-3] + "..."
    return string

def random_color():
    return discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

async def addwarn(self, user, interaction, grund):
    db = getMongoDataBase()
    
    warnID = await db["warns"].count_documents({"guildID": str(interaction.guild.id), "userID": str(user.id)}) + 1
    
    date = datetime.datetime.now().strftime("%d.%m.%Y")
    
    grund += f"\n``Verwarnung erstellt am {date}``"
    
    await db["warns"].insert_one({"guildID": str(interaction.guild.id), "userID": str(user.id), "grund": grund, "warnID": warnID, "time": datetime.datetime.now()})
    await automod(self, user, interaction.guild, warnID, interaction)

async def automod(self, user, guild, warnanzahl, interaction):
    db = getMongoDataBase()
    actions = await db["automod"].find_one({"guildID": str(guild.id), "warnanzahl": warnanzahl})

    if(actions == None):
        return
    
    try:
        if "Timeout" in actions["aktion"]:
            time_end = discord.utils.utcnow()

            if "time" in actions:
                dt = time_end + datetime.timedelta(seconds=actions["time"])
            else:
                dt = time_end + datetime.timedelta(seconds=86400)
            await user.timeout(dt ,reason="Automod wurde ausgelöst")
            await interaction.channel.send(f"🚨 **Der Benutzer {user.mention} wurde für {int(actions['time'])} Sekunden getimeoutet.** 🚨\nGrund: Automod wurde ausgelöst ({warnanzahl} Verwarnungen).")

        if actions["aktion"] == "Kick":
            await user.kick(reason="Automod wurde ausgelöst")
            await interaction.channel.send(f"🚨 **Der Benutzer {user.mention} wurde gekickt.** 🚨\nGrund: Automod wurde ausgelöst ({warnanzahl} Verwarnungen).")

        if actions["aktion"] == "Ban":
            await user.ban(reason="Automod wurde ausgelöst")
            await interaction.channel.send(f"🚨 **Der Benutzer {user.mention} wurde gebannt.** 🚨\nGrund: Automod wurde ausgelöst ({warnanzahl} Verwarnungen).")
    except discord.Forbidden as e:
        pass

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
        await db["erinnerungen"].delete_one({"userID": str(user_id), "id": id})
        return
    
    result = await db["erinnerungen"].find_one({"userID": str(user_id), "id": id})
    if result == None:
        return
    
    await db["erinnerungen"].delete_one({"userID": str(user_id), "id": id})
    embed = discord.Embed(title="<:v_stopwatch:1264271803774140608> Timer abgelaufen", description=result["beschreibung"], color=discord.Color.green())
    
    try:
        await user.send(embed=embed, view=NewTimerName(bot, result["beschreibung"], result["zeit"], embed))
    except:
        pass
                
async def vote_reminder(when: datetime.datetime, bot, user_id):
    await bot.wait_until_ready()
    await discord.utils.sleep_until(when=when)
    
    db = getMongoDataBase()
    
    guild = await bot.fetch_guild(925729625580113951)
    rolle = guild.get_role(1041046601394815127)
    user = await bot.fetch_user(user_id)
    member = await guild.fetch_member(int(user_id))
    voter = guild.get_role(962753309997932554)
    
    await db["vote"].delete_many({"userid": str(user_id)})
    
    if not member:
        return
    
    embed = discord.Embed(title="Du kannst voten", url="https://top.gg/bot/925799559576322078/vote", description="""
<:v_clock:1264270994730909726> Der Vote-Cooldown von 12 Stunden ist abgelaufen. Es wäre sehr schön, wenn du wieder für mich votest.
<:v_heart:1265212622735671406> Als Belohnung für einen weiteren Vote bekommst du **300 🍪 im Economy System** und eine besondere **Rolle in [Vulpos Wald](https://discord.gg/49jD3VXksp)**

<:v_12:1264264683427336259> Du kannst Vote Erinnerungen in **Vulpos Wald** ausschalten.""", colour=discord.Colour.green())
    
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
        result = await db["gewinnspiele"].find_one({"msgID": str(msgID), "status": "Aktiv"})
    if(status == "Beenden"):
        result = await db["gewinnspiele"].find_one({"msgID": str(msgID), "status": "Aktiv"})
    if(status == "Reroll"):
        result = await db["gewinnspiele"].find_one({"msgID": str(msgID), "status": "Inaktiv"})
        
    if result == None:
        return
    
    guild = None
    kanal = None
    msg = None
    
    try:
        guild = await bot.fetch_guild(result["guildID"])
        kanal = await guild.fetch_channel(result["channelID"])
        msg = await kanal.fetch_message(msgID)
    except Exception as e:
        print(e)
        return
    
    if guild == None or kanal == None or msg == None:
        return
    
    await db["gewinnspiele"].update_one({"guildID": str(guild.id), "channelID": str(kanal.id), "msgID": str(msgID)}, {"$set": {"status": "Inaktiv"}})
    
    participantResults = await db["gewinnspiel_teilnehmer"].find({"guildID": str(guild.id), "channelID": str(kanal.id), "msgID": str(msgID)}).to_list(length=None)
    
    if len(participantResults) == 0:
        await msg.reply("😢 Es gab leider keine Teilnehmer. Niemand hat gewonnen.")
        embed = discord.Embed(title=f"🏆 {result['preis']}", description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)
        
<:v_165:1264268434783604777> __**Wer hat gewonnen?**__
<:v_24:1264264867511144479> Niemand hat gewonnen.
<:v_24:1264264867511144479> Das Gewinnspiel endete {discord_timestamp(datetime.datetime.now(), 'R')}
<:v_24:1264264867511144479> Es gab 0 Teilnehmer.""", color=discord.Color.red())
        
        embed.set_thumbnail(url=msg.guild.icon)
        
        return await msg.edit(content="**⛔️ Gewinnspiel beendet ⛔️**", embed=embed, view=None)
    
    participants = [userid["userID"] for userid in participantResults]
    winner = random.sample(participants, k=len(participants) if len(participants) < result["winners"] else result["winners"])
    winners = ""
    
    for win in winner:
        member = await guild.fetch_member(int(win))
        
        embed = discord.Embed(colour=discord.Color.gold(), title=result["preis"], description=f"""
`🎉` · Gewonnen auf [{guild.name}]({msg.jump_url})
`⏰` · Das Gewinnspiel endete {discord_timestamp(datetime.datetime.now(), 'R')}
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
            
    await msg.reply(f"{winners} {'hat' if len(winner) == 1 else 'haben'} **{result['preis']}** gewonnen.")
    
    embed = discord.Embed(title=f"🏆 {result['preis']}", description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)
        
<:v_165:1264268434783604777>
› __**Wer hat gewonnen?**__
<:v_24:1264264867511144479> {winners} {'hat' if len(winner) == 1 else 'haben'} {result['preis']} gewonnen.
<:v_24:1264264867511144479> Das Gewinnspiel endete {discord_timestamp(datetime.datetime.now(), 'R')}
<:v_24:1264264867511144479> Es gab {len(participantResults)} Teilnehmer.""", color=discord.Color.red())
    embed.set_footer(text=f"🍀 Die Wahrscheinlichkeit zu gewinnen lag bei {round((int(result['winners']) / len(participantResults)) * 100)}%")
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
    role = await db["levelroles"].find_one({"guild_id": str(guild.id), "level": newlevel})
        
    if role == None:
        return None

    role_object = guild.get_role(int(role['roleid']))
    if role_object and role_object not in user.roles:
        try:
            await user.add_roles(role_object)
            return role_object
        except:
            return None
    return None

    
async def send_error(title, description, interaction):
    embed = discord.Embed(colour=discord.Colour.red(), title=title, description=description)
    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
    
    try:
        await interaction.followup.send(embed=embed, ephemeral=True)
    except Exception as e:
        print(e)
        try:
            await interaction.followup.send("**<:v_x:1264270921452224562> Mir fehlt die Berechtigung 'Nachrichten einbetten'.**", ephemeral=True)
        except:
            pass

async def get_lang(bot, guild):
    
    db = getMongoDataBase()
    
    lang = await db["sprachen"].find_one({"guildID": str(guild.id)})
    
    return lang or "de"

async def fetch_role(guild, role_id):
    return discord.utils.get(guild.roles, id=int(role_id))