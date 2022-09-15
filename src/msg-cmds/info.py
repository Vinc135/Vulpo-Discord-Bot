import discord
import datetime
import mysql.connector
from typing import Literal
import random

def check_member_role(member, role):
    if role in member.roles:
        return True
    else:
        return False

async def vote_reminder(when: datetime.datetime, bot, user_id):
    await discord.utils.sleep_until(when=when)
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute(f"DELETE FROM vote WHERE userid = {user_id}")
    mydb.commit()
    mydb.close()
    user = await bot.fetch_user(user_id)
    if user:
        if int(user.id) == 732993370305069116:
            return
        embed = discord.Embed(title="Voten", description="12 Stunden sind um und du kannst erneut voten. Es würde mich echt dolle supporten, wenn du nochmal votest.", color=discord.Color.green(), url="https://top.gg/bot/925799559576322078/vote")
        embed.set_footer(text="Danke für deine Unterstützung", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/8fbda58cd58e49af67a2ae95ac8b0bdc.webp?size=1024")
        try:
            await user.send(embed=embed)
        except:
            pass
    else:
        pass
    guild = bot.get_guild(925729625580113951)
    member = guild.get_member(int(user_id))
    if member is not None:
        voter = guild.get_role(962753309997932554)
        await member.remove_roles(voter)

async def giveaway_end(when: datetime.datetime, bot, giveaway_id):
    await discord.utils.sleep_until(when=when)
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute(f"SELECT prize, winners, channelID, guildID FROM active_giveaways WHERE gwID = {giveaway_id}")
    result = cursor.fetchone()
    try:
        prize = result[0]
        winner_count = result[1]
        guild = bot.get_guild(int(result[3]))
        channel = guild.get_channel(int(result[2]))
        msg = await channel.fetch_message(int(giveaway_id))
        if guild == None or channel == None or msg == None:
            cursor.execute(f'DELETE FROM active_giveaways WHERE gwID = {giveaway_id}')
            mydb.commit()
            mydb.close()
            return
    except:
        cursor.execute(f'DELETE FROM active_giveaways WHERE gwID = {giveaway_id}')
        mydb.commit()
        mydb.close()
        return

    time_end = int(datetime.datetime.utcnow().timestamp() + 7200)
    timestamp = datetime.datetime.fromtimestamp(int(time_end))

    reactions = [reaction for reaction in msg.reactions if reaction.emoji == "🎉"][0]
    participants = [user async for user in reactions.users()]
    participants.remove(guild.me)
    winner = random.sample(participants, k=len(participants) if len(participants) < int(winner_count) else int(winner_count))

    cursor.execute("SELECT roleID FROM active_giveaways WHERE guildID = (%s) AND gwID = (%s)", (result[3], giveaway_id))
    role = cursor.fetchall()
    if len(winner) < 1:
        errorembed = discord.Embed(title=f"😕 Leider...", description='Es gab keinen Gewinner.',
                               color=discord.Colour.purple())
        errorembed.set_footer(text=f"• Reroll Command: v!greroll {giveaway_id} [gewinneranzahl]")
        if role[0][0] is None:
            pass
        else:
            try:
                r = guild.get_role(int(role[0][0]))
                if r is None:
                    pass
                else:
                    errorembed.add_field(name="🎭 Benötigte Rolle", value=r.mention)
            except:
                pass
        errorembed.add_field(name="⏰ Geendet am", value=f'{discord_timestamp(timestamp, "f")}({discord_timestamp(timestamp, "R")})')
        await msg.edit(content="**🏁 Giveaway beendet 🏁**", embed=errorembed)
        await msg.reply('Es gab zu wenig Teilnehmer beim Giveaway. :c')
        cursor.execute(f'DELETE FROM active_giveaways WHERE gwID = {giveaway_id}')
        if role[0][0] == None:
            cursor.execute(
                'INSERT INTO old_giveaways(guildID, gwID, prize, channelID, winners) VALUES (%s, %s, %s, %s, %s)',
                (guild.id, giveaway_id, prize, channel.id, winner_count))
        else:
            r = guild.get_role(int(role[0][0]))
            cursor.execute(
                'INSERT INTO old_giveaways(guildID, gwID, prize, channelID, winners, roleID) VALUES (%s, %s, %s, %s, %s, %s)',
                (guild.id, giveaway_id, prize, channel.id, winner_count, r.id))
        mydb.commit()
        return
    else:
        winners = ', '.join(win.mention for win in winner)
        winembed = discord.Embed(title=f"🎊 Glückwunsch", description=f'{winners} hat {prize} gewonnen.',
                               color=discord.Colour.purple())
        winembed.set_footer(text=f"• Reroll Command: v!greroll {giveaway_id} [gewinneranzahl]")
        if role[0][0] == None:
            pass
        else:
            try:
                r = guild.get_role(int(role[0][0]))
                if r is None:
                    pass
                else:
                    winembed.add_field(name="🎭 Benötigte Rolle", value=r.mention)
            except:
                pass
        winembed.add_field(name="⏰ Geendet am", value=f'{discord_timestamp(timestamp, "f")}({discord_timestamp(timestamp, "R")})')
        await msg.reply(f':tada: Glückwunsch {winners}! Du hast **{prize}** gewonnen.')
        await msg.edit(content="**🏁 Giveaway beendet 🏁**", embed=winembed)
        cursor.execute(f'DELETE FROM active_giveaways WHERE gwID = {giveaway_id}')
        if role[0][0] == None:
            cursor.execute(
                'INSERT INTO old_giveaways(guildID, gwID, prize, channelID, winners) VALUES (%s, %s, %s, %s, %s)',
                (guild.id, giveaway_id, prize, channel.id, winner_count))
        else:
            r = guild.get_role(int(role[0][0]))
            cursor.execute(
                'INSERT INTO old_giveaways(guildID, gwID, prize, channelID, winners, roleID) VALUES (%s, %s, %s, %s, %s, %s)',
                (guild.id, giveaway_id, prize, channel.id, winner_count, r.id))
    mydb.commit()
    mydb.close()

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
            return False
    except:
        return False

async def get_syntax(ctx):
    cmd = ctx.command
    embed = discord.Embed(colour=discord.Colour.red(), title="❌ Falscher Syntax", description=f"Syntax: v!{cmd.name} {cmd.usage}\n\n**{cmd.help}**")
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
    await ctx.send(embed=embed)
    return

async def levelup_role_check(botobject, guildid, userid, newlevel):
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    guild = botobject.get_guild(int(guildid))
    if guild is None:
        return False
    if guild:
        member = guild.get_member(int(userid))
        if member is None:
            return False
        if member:
            cursor.execute(f"SELECT roleid FROM levelroles WHERE guild_id = (%s) AND level = (%s)", (guild.id, newlevel))
            result2 = cursor.fetchone()
            levelrole = result2[0]
            if levelrole == None or levelrole == False:
                return False
            if levelrole:
                role = guild.get_role(int(levelrole))
                if role is None:
                    return False
                if role:
                    if role not in member.roles:
                        try:
                            await remove_old_levelroles(member, guild)
                        except:
                            pass
                        await member.add_roles(role)
                        return role
                    else:
                        return False
    mydb.close()

async def remove_old_levelroles(member, guild):
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute(f"SELECT roleid FROM levelroles WHERE guild_id = {guild.id}")
    result = cursor.fetchall()
    for i in result:
        role = guild.get_role(int(i[0]))
        if role is None:
            pass
        if role:
            if role not in member.roles:
                pass
            if role in member.roles:
                await member.remove_roles(role)

    mydb.close()