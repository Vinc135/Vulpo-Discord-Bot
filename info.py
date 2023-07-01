import discord
import datetime
from typing import Literal
import random
import datetime
            
async def haspremium_forserver(self, guild):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT status FROM premium WHERE userID = (%s)", (guild.owner.id))
            status = await cursor.fetchone()
            if status == None:
                return False
            if status[0] == 1:
                return True
            if status[0] == 0:
                return False
            
async def getcolour(self, user):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT status FROM premium WHERE userID = (%s)", (user.id))
            status = await cursor.fetchone()
            if status == None:
                return discord.Colour.orange()
            if status[0] == 0:
                return discord.Colour.orange()
            if status[0] == 1:
                await cursor.execute("SELECT farbe FROM embedfarben WHERE userID = (%s)", (user.id))
                farbe = await cursor.fetchone()
                if farbe == None:
                    return discord.Colour.orange()
                else:
                    return discord.Colour(int(farbe[0], 16))

async def checkstatus(self, guild):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT enabled FROM levelstatus WHERE guild_id = (%s)", (guild.id))
            enabled = await cursor.fetchone()
            if enabled == None:
                await cursor.execute("INSERT INTO levelstatus (guild_id, enabled) VALUES (%s, %s)", (guild.id, 0))
                return False
            if enabled[0] == 1:
                return True
            if enabled[0] == 0:
                return False

async def voicetime_to_xp(self, member, time, before):
    if member.bot:
        return
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            if await checkstatus(self, member.guild) == False:
                return
            
            await cursor.execute(f"SELECT role_id FROM lb_rollen WHERE guild_id = {member.guild.id}")
            lb_rollen = await cursor.fetchall()
            for r_id in lb_rollen:
                rolle = member.guild.get_role(int(r_id[0]))
                if rolle:
                    if rolle in member.roles:
                        return
            
            await cursor.execute(f"SELECT channel_id FROM lb_channel WHERE guild_id = {member.guild.id}")
            lb_channel = await cursor.fetchall()
            for c_id in lb_channel:
                if int(c_id[0]) == int(before.channel.id):
                    return

            newxp = random.randint(15, 30) * time
            await cursor.execute("SELECT user_xp, user_level FROM levelsystem WHERE client_id = (%s) AND guild_id = (%s)", (member.id, member.guild.id))
            userdata = await cursor.fetchone()
            if userdata == None:
                await cursor.execute("INSERT INTO levelsystem (client_id, user_xp, user_level, guild_id) VALUES (%s, %s, %s, %s)", (member.id, newxp, 0, member.guild.id))
                return

            
            #################################################################################################### XP BOOST
            
            await cursor.execute("SELECT status FROM xpboost WHERE guildID = (%s)", (member.guild.id))
            xpboost = await cursor.fetchone()
            if xpboost == None:
                pass
            if xpboost != None:
                if xpboost[0] == 1:
                    newxp += newxp * 2
                if xpboost[0] == 0:
                    pass
            
            #################################################################################################### XP BOOST
            await cursor.execute("UPDATE levelsystem SET user_xp = (%s) WHERE client_id = (%s) AND guild_id = (%s)", (int(userdata[0]) + newxp, member.id, member.guild.id))
                
def limit_characters(string: str, limit: int):
    if len(string) > limit:
        return string[:limit-3] + "..."
    return string

def random_color():
    return discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

async def addwarn(self, user, interaction, grund):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT warnID FROM warns WHERE userID = (%s) AND guildID = (%s)", (user.id, interaction.guild.id))
            result = await cursor.fetchall()
            if result is None:
                await cursor.execute("INSERT INTO warns(guildID, userID, grund, warnID) VALUES(%s, %s, %s, %s)", (interaction.guild.id, user.id, grund + f"\n`Verwarnung erstellt am {discord.utils.utcnow().__format__('%d.%m.%Y')}`", 1))
                
                await automod(self, user, interaction.guild, 1, interaction)
                return
            if result != None:
                warnID = 1
                for warn in result:
                    warnID += 1
                await cursor.execute("INSERT INTO warns(guildID, userID, grund, warnID) VALUES(%s, %s, %s, %s)", (interaction.guild.id, user.id, grund + f"\n`Verwarnung erstellt am {discord.utils.utcnow().__format__('%d.%m.%Y')}`", warnID))
                
                await automod(self, user, interaction.guild, warnID, interaction)

async def automod(self, user, guild, warnanzahl, interaction):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            #for w in range(warnanzahl + 1):
            await cursor.execute("SELECT aktion FROM automod WHERE guildID = (%s) AND warnanzahl = (%s)", (guild.id, warnanzahl))
            result = await cursor.fetchone()
            if result:
                if result[0] == "Timeout":
                    time_end = discord.utils.utcnow()
                    dt = time_end + datetime.timedelta(days=1)
                    await user.timeout(dt ,reason="Automod wurde ausgelöst")
                    await interaction.channel.send(f"🚨 **Der Benutzer {user.mention} wurde getimeoutet.** 🚨\nGrund: Automod wurde ausgelöst ({warnanzahl} Verwarnungen).")
                if result[0] == "Kick":
                    await user.kick(reason="Automod wurde ausgelöst")
                    await interaction.channel.send(f"🚨 **Der Benutzer {user.mention} wurde gekickt.** 🚨\nGrund: Automod wurde ausgelöst ({warnanzahl} Verwarnungen).")
                if result[0] == "Ban":
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
    async with bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            user = await bot.fetch_user(user_id)
            if user:
                await cursor.execute("SELECT beschreibung FROM erinnerungen WHERE userID = (%s) AND id = (%s)", (user_id, id))
                result = await cursor.fetchone()
                await cursor.execute("DELETE FROM erinnerungen WHERE userID = (%s) AND id = (%s)", (user_id, id))
                embed = discord.Embed(title="<:v_zeit:1119585888054296676> Timer abgelaufen", description=result[0], color=discord.Color.green())
                embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                try:
                    await user.send(embed=embed)
                except:
                    pass
            else:
                await cursor.execute("DELETE FROM erinnerungen WHERE userID = (%s) AND id = (%s)", (user_id, id))
                
async def vote_reminder(when: datetime.datetime, bot, user_id):
    await bot.wait_until_ready()
    await discord.utils.sleep_until(when=when)
    async with bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            guild = bot.get_guild(925729625580113951)
            rolle = guild.get_role(1041046601394815127)
            member = guild.get_member(int(user_id))
            await cursor.execute(f"DELETE FROM vote WHERE userid = {user_id}")
            user = await bot.fetch_user(user_id)
            if member:
                embed = discord.Embed(title="Du kannst voten", url="https://top.gg/bot/925799559576322078/vote", description="""
<:v_zeit:1119585888054296676> Der Vote-Cooldown von 12 Stunden ist abgelaufen. Es wäre sehr schön, wenn du wieder für mich votest.
<:herz:941398727501955113> Als Belohnung für einen weiteren Vote bekommst du **300 🍪 im Economy System** und eine besondere **Rolle in [Vulpos Wald](https://discord.gg/49jD3VXksp)**

<:v_info:1119579853092552715> Du kannst Vote Erinnerungen in <#926224205639467108> ausschalten.""", colour=discord.Colour.green())
                embed.set_footer(text="Danke für deine Unterstützung", icon_url="https://media.discordapp.net/attachments/965302660871884840/965315155816767548/Vulpo_neu.png?width=1572&height=1572")
                voter = guild.get_role(962753309997932554)
                await member.remove_roles(voter)
                try:
                    if rolle in member.roles:
                        await user.send(embed=embed)
                except:
                    pass

async def giveaway_end(when: datetime.datetime, bot, msgID, status=None):
    try:
        await bot.wait_until_ready()
        await discord.utils.sleep_until(when=when)
        async with bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if status == None:
                    await cursor.execute("SELECT * FROM gewinnspiele WHERE msgID = (%s) AND status = (%s)", (msgID, "Aktiv"))
                    result = await cursor.fetchone()
                if status == "Beenden":
                    await cursor.execute("SELECT * FROM gewinnspiele WHERE msgID = (%s) AND status = (%s)", (msgID, "Aktiv"))
                    result = await cursor.fetchone()
                if status == "Reroll":
                    await cursor.execute("SELECT * WHERE msgID = (%s) AND status = (%s)", (msgID, "Inaktiv"))
                    result = await cursor.fetchone()
                if result is None:
                    return
                #guildID, channelID, msgID, hostID, endtime, preis, winners, status, nachrichten, rollenID, voicezeit, custom_status, jointime
                try:
                    guild = bot.get_guild(int(result[0]))
                    kanal = guild.get_channel(int(result[1]))
                    msg = await kanal.fetch_message(int(msgID))
                except:
                    pass

                await cursor.execute("UPDATE gewinnspiele SET status = (%s) WHERE guildID = (%s) AND channelID = (%s) AND msgID = (%s)", ("Inaktiv", guild.id, kanal.id, msgID))
                
                t1 = int(datetime.datetime.now().timestamp())
                t2 = datetime.datetime.fromtimestamp(int(t1))
                
                await cursor.execute("SELECT userID FROM gewinnspiel_teilnehmer WHERE guildID = (%s) AND channelID = (%s) AND msgID = (%s)", (guild.id, kanal.id, msgID))
                result2 = await cursor.fetchall()
                if result2 == None or str(result2) == "()":
                    await msg.reply("😢 Es gab leider keine Teilnehmer. Niemand hat gewonnen.")
                    embed = discord.Embed(title=f"🏆 {result[5]}", description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)
            
<:v_geschenk:1119579279274025060> › __**Wer hat gewonnen?**__
 <:v_play:1119582324166770708> Niemand hat gewonnen.
 <:v_play:1119582324166770708> Das Gewinnspiel endete {discord_timestamp(t2, 'R')}
 <:v_play:1119582324166770708> Es gab 0 Teilnehmer.""", color=discord.Color.red())
                    embed.set_thumbnail(url=msg.guild.icon)
                    embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                    return await msg.edit(content="**⛔️ Gewinnspiel beendet ⛔️**", embed=embed, view=None)

                participants = [userid[0] for userid in result2]
                winner = random.sample(participants, k=len(participants) if len(participants) < int(result[5]) else int(result[5]))
                winners = ""
                for win in winner:
                    member = guild.get_member(int(win))
                    embed = discord.Embed(colour=discord.Color.gold(), title=result[10], description=f"""
    `🎉` · Gewonnen auf [{guild.name}]({msg.jump_url})
    `⏰` · Das Gewinnspiel endete {discord_timestamp(t2, 'R')}
    """)
                    embed.set_thumbnail(url=guild.icon)
                    embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                    try:
                        await member.send("Du hast ein Gewinnspiel **gewonnen**!", embed=embed)
                    except:
                        pass
                    if winners == "":
                        winners += f"{member.mention}"
                    else:
                        winners += f", {member.mention}"
                        
                await msg.reply(f"{winners} {'hat' if len(winner) == 1 else 'haben'} {result[10]} gewonnen.")
                embed = discord.Embed(title=f"🏆 {result[10]}", description=f"""
`🤖` · [Lade den Bot hier ein](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands)
            
<:v_geschenk:1119579279274025060> › __**Wer hat gewonnen?**__
 <:v_play:1119582324166770708> {winners} {'hat' if len(winner) == 1 else 'haben'} {result[10]} gewonnen.
 <:v_play:1119582324166770708> Das Gewinnspiel endete {discord_timestamp(t2, 'R')}
 <:v_play:1119582324166770708> Es gab {len(result2)} Teilnehmer.""", color=discord.Color.red())
                embed.set_footer(text=f"🍀 Die Wahrscheinlichkeit zu gewinnen lag bei {round((int(result[5]) / len(result2)) * 100)}%")
                embed.set_thumbnail(url=msg.guild.icon)
                await msg.edit(content="**⛔️ Gewinnspiel beendet ⛔️**", embed=embed, view=None)
    
    except:
        pass
                

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

async def levelup_role_check(botobject, guildobjekt, userobjekt, newlevel):
    async with botobject.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SELECT roleid FROM levelroles WHERE guild_id = (%s) AND level = (%s)", (guildobjekt.id, newlevel))
            rollen = await cursor.fetchall()
            if rollen:
                for r_id in rollen:
                    r_objekt = guildobjekt.get_role(int(r_id[0]))
                    if r_objekt:
                        if r_objekt not in userobjekt.roles:
                            await userobjekt.add_roles(r_objekt)
                            return r_objekt
                        else:
                            return None
            if rollen is None:
                return None
    
async def send_error(title, description, interaction):
    embed = discord.Embed(colour=discord.Colour.red(), title=title, description=description)
    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
    embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
    try:
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except:
        try:
            await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Mir fehlt die Berechtigung 'Nachrichten einbetten'.**", ephemeral=True)
        except:
            pass

async def get_lang(bot, guild):
    async with bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT sprache FROM sprachen WHERE guildID = (%s)", (guild.id))
            result = await cursor.fetchone()
            if result:
                return result[0]
            return "de"
