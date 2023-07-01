import os
import discord
from discord.ext import commands
import datetime
import asyncio
import traceback
import sys
from info import giveaway_end, vote_reminder, send_error, random_color, reminder_end, limit_characters
import topgg
import math
from discord.app_commands import AppCommandError, CommandTree
from discord import app_commands
import aiomysql
from googletrans import Translator
from info import discord_timestamp
import time


dbl_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjkyNTc5OTU1OTU3NjMyMjA3OCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjQyODc4ODc1fQ.PJVIOEUe25WxuUbD1E68UF7bXpRZR_k4XXwr8ukue-c"

class voteView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        votebutton = discord.ui.Button(label="Auch voten", style=discord.ButtonStyle.grey, url="https://top.gg/bot/925799559576322078/vote")
        self.add_item(votebutton)
    
class reportmsg(discord.ui.View):
    def __init__(self, message=None, bot=None):
        super().__init__(timeout=None)
        self.message = message
        self.bot = bot

    @discord.ui.button(label='Gemeldeten Nutzer verwarnen', style=discord.ButtonStyle.red, custom_id="fbiuwerzgfiuwzevfizuk", emoji="🔨")
    async def warn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.edit(content=f"**🔒 Dieser Nutzer wurde von {interaction.user.mention} verwarnt.**", embed=interaction.message.embeds[0], view=None)
        user = self.message.author
        grund = "Unangemessene Nachricht"

        #warn + automod anfang
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                warnID = 1
                await cursor.execute("SELECT warnID FROM warns WHERE userID = (%s) AND guildID = (%s)", (user.id, interaction.guild.id))
                result = await cursor.fetchall()
                if result is None:
                    await cursor.execute("INSERT INTO warns(guildID, userID, grund, warnID) VALUES(%s, %s, %s, %s)", (interaction.guild.id, user.id, grund + f"\n`Verwarnung erstellt am {discord.utils.utcnow().__format__('%d.%m.%Y')}`", 1))
                    
                    warnID += 1
                    return
                if result != None:
                    for warn in result:
                        warnID += 1
                    await cursor.execute("INSERT INTO warns(guildID, userID, grund, warnID) VALUES(%s, %s, %s, %s)", (interaction.guild.id, user.id, grund + f"\n`Verwarnung erstellt am {discord.utils.utcnow().__format__('%d.%m.%Y')}`", warnID))

                await cursor.execute("SELECT aktion FROM automod WHERE guildID = (%s) AND warnanzahl = (%s)", (interaction.guild.id, warnID))
                result2 = await cursor.fetchone()
                if result2:
                    if result2[0] == "Timeout":
                        time_end = discord.utils.utcnow()
                        dt = time_end + datetime.timedelta(days=1)
                        await user.timeout(dt ,reason="Automod wurde ausgelöst")
                        await interaction.channel.send(f"🚨 **Der Benutzer {user.mention} wurde getimeoutet.** 🚨\nGrund: Automod wurde ausgelöst ({warnID} Verwarnungen).")
                    if result2[0] == "Kick":
                        await user.kick(reason="Automod wurde ausgelöst")
                        await interaction.channel.send(f"🚨 **Der Benutzer {user.mention} wurde gekickt.** 🚨\nGrund: Automod wurde ausgelöst ({warnID} Verwarnungen).")
                    if result2[0] == "Ban":
                        await user.ban(reason="Automod wurde ausgelöst")
                        await interaction.channel.send(f"🚨 **Der Benutzer {user.mention} wurde gebannt.** 🚨\nGrund: Automod wurde ausgelöst ({warnID} Verwarnungen).")
        #warn + automod ende


        await interaction.response.send_message("**<:v_haken:1119579684057907251> Nutzer wurde verwarnt.**", ephemeral=True)

class MyTree(CommandTree):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        try:
            user = interaction.user
            guild = bot.get_guild(925729625580113951)
            banned_users = [ban async for ban in guild.bans()]
            for entry in banned_users:
                banned_user = entry.user
                if int(user.id) == int(banned_user.id):
                    embed = discord.Embed(title="<:v_mod:1119581819122241621> Du bist gebannt", description=f"""
    > <:v_info:1119579853092552715> Mit einem Bann hast du keinen Zugang mehr zu Vulpo's Befehlen. Außerdem hast du keinen Zutritt zum Supportserver "Vulpo's Wald".
     <:v_play:1119582324166770708> Grund: {entry.reason}
    <:v_play:1037065922134945853> Falls du denkst, dass du dich geändert hast, oder du zu unrecht bestraft wurdest, kannst du einen [Entbannungsantrag](https://forms.gle/NH1Jb1gVNEPuTLA58) stellen.
    """, colour=0xac0000)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return False
            return True
        except:
            pass

class Vulpo(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix="vulpo!", help_command=None, case_insensitive=True, intents=discord.Intents.all(), tree_cls=MyTree)
        self.giveaways = False
        self.votes = False
        self.reminder = False

    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot is True:
            return
        if msg.mentions:
            if msg.mentions[0] == bot.user:
                if msg.reference:
                    return
                embed = discord.Embed(colour=random_color(), title="VULPO", description="""
    Hey ich bin Vulpo, hier um den Server zu verbessern. Ich verfüge __nur__ über Slash Commands. Um mein volles Potential zu nutzen, müsstest du mich über [diesen Link](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands) einladen.
    Ich zeichne mich durch meine große Anzahl an verschiedensten smarten Systemen und Commands aus. Du kannst mich gerne auf dem [Supportserver](https://discord.gg/49jD3VXksp) testen, damit ich dich überzeugen kann, falls noch nicht.""", url="https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands")
                embed.set_author(name=msg.author, icon_url=msg.author.avatar)
                embed.set_thumbnail(url=msg.guild.icon)
                embed.set_footer(text=f"{len(bot.guilds)} Server vertrauen mir. Vielleicht auch bald du?")
                await msg.channel.send(embed=embed)
                return await bot.process_commands(msg)
            else:
                await bot.process_commands(msg)
        await bot.process_commands(msg)
        
    async def on_guild_join(self, guild):
        guilds = bot.get_guild(925729625580113951)
        channels = guilds.get_channel(925732763364106290)
        
        t1 = math.floor(guild.created_at.timestamp())
        t2 = datetime.datetime.fromtimestamp(int(t1))
        msg = f"""
        <:v_info:1119579853092552715> **Informationen**
        <:v_cookie:1119578273580593232> {guild.name} ({guild.id})
        <:v_krone:1119580951794696224> {guild.owner} ({guild.owner.id})
        <:v_user:1119585450923929672> {guild.member_count}
        <:v_zeit:1119585888054296676> {discord_timestamp(t2, 'R')}
       	
        <:v_info:1119579853092552715> **Vulpo ist jetzt auf {len(bot.guilds)} Servern drauf! Yay 🎉**
        """
        embed = discord.Embed(colour=discord.Colour.green(), title=f"Vulpo wurde auf {guild.name} eingeladen!", description=msg)
        embed.set_thumbnail(url=guild.icon if guild.icon else "https://cdn.discordapp.com/attachments/971092445435682907/973630982425047050/server_join.png")
        await channels.send(embed=embed)

    async def on_guild_remove(self, guild):
        try:
            guilds = bot.get_guild(925729625580113951)
            channels = guilds.get_channel(925732763364106290)
            
            t1 = math.floor(guild.created_at.timestamp())
            t2 = datetime.datetime.fromtimestamp(int(t1))
        	
            msg = f"""
            <:v_info:1119579853092552715> **Informationen**
            <:v_cookie:1119578273580593232> {guild.name} ({guild.id})
            <:v_krone:1119580951794696224> {guild.owner} ({guild.owner.id})
            <:v_user:1119585450923929672> {guild.member_count}
            <:v_zeit:1119585888054296676> {discord_timestamp(t2, 'R')}

            <:v_info:1119579853092552715> **Vulpo ist jetzt auf {len(bot.guilds)} Servern drauf!**
            """
            
            embed = discord.Embed(colour=discord.Colour.red(), title=f"Vulpo wurde aus {guild.name} rausgeschmissen!", description=msg)
            embed.set_thumbnail(url=guild.icon if guild.icon else 'https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549')
            await channels.send(embed=embed)
        except:
            pass
    
    async def on_dbl_vote(self, data):
        if data["type"] == "test":
            return bot.dispatch('dbl_test', data)
        async with bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                userid = int(data["user"])

                guild = bot.get_guild(925729625580113951)
                channel = guild.get_channel(934036224413417472)
                await cursor.execute(f"SELECT votes FROM topgg WHERE userID = {userid}")
                result = await cursor.fetchone()
                if result is None or result is False:
                    await cursor.execute(f"INSERT INTO topgg(userID, votes) VALUES(%s, %s)", (userid, 1))
                    
                    times = 1
                else:
                    await cursor.execute(f"UPDATE topgg SET votes = (%s) WHERE userID = (%s)", (int(result[0]) + 1, userid))
                    
                    times = int(result[0]) + 1

                time_to_convert = math.floor(datetime.datetime.now().timestamp() + 43200)
                time_converted = datetime.datetime.fromtimestamp(int(time_to_convert))
                asyncio.create_task(vote_reminder(time_converted, bot, userid))
                await cursor.execute("INSERT INTO vote(userid, endtime) VALUES(%s, %s)", (userid, time_to_convert))

                user = await bot.fetch_user(userid)
                rolle = guild.get_role(1041046601394815127)
                member = guild.get_member(int(userid))
                if user:
                    embed = discord.Embed(title=f"Danke vielmals {user}!", description=f"{user.mention} hat insgesammt {times} Mal gevotet.", colour=discord.Colour.orange())
                    embed.set_thumbnail(url=user.avatar)
                    if member:
                        embed.set_footer(text="Durch einen Vote erhältst du 300 Cookies und die Voter Rolle", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508227117289472/herz.png")
                        if rolle in member.roles:
                            embed.description += f"\n<:v_zeit:1119585888054296676> Du wirst in 12 Stunden erinnert, wieder zu voten."
                        else:
                            embed.description += f"\n<:v_zeit:1119585888054296676> Deine Vote Erinnerungen sind aus. Du kannst sie in <#926224205639467108> aktivieren."
                    if member == None:
                        embed.set_footer(text="Durch einen Vote erhältst du 300 Cookies", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508227117289472/herz.png")
                    await channel.send(embed=embed, view=voteView())
                else:
                    embed = discord.Embed(title=f"Danke vielmals {userid}!", description=f"{userid} hat insgesammt {times} Mal gevotet.", colour=discord.Colour.orange())
                    embed.set_footer(text="Durch einen Vote erhältst du 300 Cookies", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508227117289472/herz.png")
                    await channel.send(embed=embed, view=voteView())
                await cursor.execute(f"SELECT rucksack, bank, job, stunden FROM economy WHERE userID = {user.id}")
                result = await cursor.fetchone()
                if result is None:
                    await cursor.execute("INSERT INTO economy(rucksack, bank, job, stunden, userID) VALUES(%s, %s, %s, %s, %s)",("0", "0", "Kein Job", "0", user.id))
                    
                    bal = 0
                else:
                    bal = int(result[0])
                new = bal + 300
                await cursor.execute("UPDATE economy SET rucksack = (%s) WHERE userID = (%s)", (new, user.id))
                

                dblpy = topgg.DBLClient(bot, dbl_token, autopost_interval=0)
                votedata = await dblpy.get_bot_info()
                votes = int(votedata["monthly_points"])
                guild = bot.get_guild(925729625580113951)
                votechannel = guild.get_channel(934036446271139860)
                mydate = datetime.datetime.now()
                translator = Translator()
                translation = translator.translate(f'Month {mydate.strftime("%B")}' , dest="de")
                await votechannel.edit(name=f"Votes {translation.text}: {votes}")
                try:
                    m = guild.get_member(userid)
                    if m is not None:
                        voter = guild.get_role(962753309997932554)
                        await m.add_roles(voter)
                        if int(times) >= 200:
                            votemeister = guild.get_role(962753328679358515)
                            await m.add_roles(votemeister)
                            return
                        if int(times) >= 100:
                            megavoter = guild.get_role(962753332139663390)
                            await m.add_roles(megavoter)
                            return
                        if int(times) >= 50:
                            ehrenhaftervoter = guild.get_role(962753335507701780)
                            await m.add_roles(ehrenhaftervoter)
                            return
                        if int(times) >= 20:
                            aktivervoter = guild.get_role(962753338666008607)
                            await m.add_roles(aktivervoter)
                            return
                except:
                    pass
                
    async def on_dbl_test(self, data):
        async with bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                userid = int(data["user"])

                guild = bot.get_guild(925729625580113951)
                channel = guild.get_channel(934036224413417472)
                await cursor.execute(f"SELECT votes FROM topgg WHERE userID = {userid}")
                result = await cursor.fetchone()
                times = result[0]

                rolle = guild.get_role(1041046601394815127)
                member = guild.get_member(int(userid))

                user = await bot.fetch_user(userid)
                if user:
                    embed = discord.Embed(title=f"Danke vielmals {user}!", description=f"{user.mention} hat insgesammt {times} Mal gevotet.", colour=discord.Colour.yellow())
                    embed.set_thumbnail(url=user.avatar)
                    embed.set_author(name="Testvote erfolgreich", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1037064093124788284/v_info.png")
                    if member:
                        embed.set_footer(text="Durch einen Vote erhältst du 300 Cookies und die Voter Rolle", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508227117289472/herz.png")
                        if rolle in member.roles:
                            embed.description += f"\n<:v_zeit:1119585888054296676> Du wirst in 12 Stunden erinnert, wieder zu voten."
                        else:
                            embed.description += f"\n<:v_zeit:1119585888054296676> Deine Vote Erinnerungen sind aus. Du kannst sie in <#926224205639467108> aktivieren."
                    if member == None:
                        embed.set_footer(text="Durch einen Vote erhältst du 300 Cookies", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508227117289472/herz.png")
                    await channel.send(embed=embed, view=voteView())
                else:
                    embed = discord.Embed(title=f"Danke vielmals {userid}!", description=f"{userid} hat insgesammt {times} Mal gevotet.", colour=discord.Colour.yellow())
                    embed.set_footer(text="Durch einen Vote erhältst du 300 Cookies", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508227117289472/herz.png")
                    embed.set_author(name="Testvote erfolgreich", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1037064093124788284/v_info.png")
                    await channel.send(embed=embed, view=voteView())
                
    async def setup_hook(self):
        try:
            loop = asyncio.get_event_loop()
            pool = await aiomysql.create_pool(host='157.90.72.7', port=3306, user='databaseAdmin', password='OkUyBflP3l3i8ax$*A4', db='VulpoDB', loop=loop, autocommit=True, maxsize=100)
            bot.pool = pool
            print(f"✅ Pool erstellt")
        except:
            print(f"❌ Fehler bei der Pool Erstellung")
        async with bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("/dblwebhook", "Vulpo123321")
                    await topgg_webhook.run(5000)
                    print("✅ Verbunden mit der topgg api")
                except:
                    print("❌ Verbindung zur topgg api fehlgeschlagen")
                    
                try:
                    if self.giveaways is False:
                        self.giveaways = True
                        await cursor.execute("SELECT endtime, msgID FROM gewinnspiele WHERE status = (%s)", ("Aktiv"))
                        result = await cursor.fetchall()
                        if str(result) == "()":
                            return print(f"✅ Asyncio tasks für Giveaways bereit(0)")
                        a = 0
                        for i in result:
                            time_to_convert = int(i[0])
                            time_converted = datetime.datetime.fromtimestamp(int(time_to_convert))
                            a += 1
                            asyncio.create_task(giveaway_end(time_converted, bot, int(i[1])))
                        print(f"✅ Asyncio tasks für Giveaways bereit({a})")
                except Exception as e:
                    print(f"❌ Asyncio tasks für Giveaways nicht bereit\n\n{e}")
                    
                try:
                    if self.votes is False:
                        self.votes = True
                        await cursor.execute("SELECT userid, endtime FROM vote")
                        result = await cursor.fetchall()
                        a = 0
                        for c in result:
                            time_to_convert = int(c[1])
                            time_converted = datetime.datetime.fromtimestamp(int(time_to_convert))
                            a += 1
                            asyncio.create_task(vote_reminder(time_converted, bot, int(c[0])))
                        print(f"✅ Asyncio tasks für Vote bereit({a})")
                except Exception as e:
                    print(f"❌ Asyncio tasks für Vote nicht bereit\n\n{e}")
                    
                try:
                    if self.reminder is False:
                        self.reminder = True
                        await cursor.execute("SELECT userID, endtime, id FROM erinnerungen")
                        result = await cursor.fetchall()
                        a = 0
                        for c in result:
                            time_to_convert = int(c[1])
                            time_converted = datetime.datetime.fromtimestamp(int(time_to_convert))
                            a += 1
                            asyncio.create_task(reminder_end(time_converted, bot, c[0], c[2]))
                        print(f"✅ Asyncio tasks für Erinnerungen bereit({a})")
                except Exception as e:
                    print(f"❌ Asyncio tasks für Vote Erinnerungen bereit\n\n{e}")
        try:
            geladen = 0
            fehler = 0
            await bot.load_extension("jishaku")
            
            for filename in os.listdir("cogs"):
                if filename.endswith(".py"):
                    try:
                        await bot.load_extension(f"cogs.{filename[:-3]}")
                        geladen += 1
                    except:
                        fehler += 1
                        print(f'❌ cogs.{filename[:-3]} konnte nicht geladen werden', file=sys.stderr)
                        traceback.print_exc()		
                        print('\n\n--------------------------------------------\n\n')
     
            print(f"✅ {geladen}/{geladen + fehler} Cogs geladen")
        except Exception as e:
            print(f"❌ Es gab einen Fehler beim Laden der Cogs\n{e}")
        ##########                   ##########
        print("   ___        _ _             ")
        print("  / _ \ _ __ | (_)_ __   ___  ")
        print(" | | | | '_ \| | | '_ \ / _ \ ")
        print(" | |_| | | | | | | | | |  __/ ")
        print("  \___/|_| |_|_|_|_| |_|\___| ")
        
    async def on_ready(self):
        try:
            await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.playing, name="mit vulpo-bot.de"))
            print("✅ Status bereit")
        except:
            print("❌ Status nicht bereit")
        bot.add_view(view=reportmsg(None, bot))
        print("✅ Alle System sind nun bereit.")

bot = Vulpo()

@bot.event
async def on_error(ctx, error):
    return 

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await send_error("Fehlende Berechtigungen", "<:v_kreuz:1119580775411621908> Du hast nicht die Rechte, diesen Command auszuführen.", interaction)
        return
    if isinstance(error,app_commands.CommandInvokeError):
        pass
    if isinstance(error,app_commands.MissingAnyRole):
        await send_error("Fehlende Berechtigungen", "<:v_kreuz:1119580775411621908> Du brauchst eine bestimmte Rolle um dies zu tun.", interaction)
        return
    if isinstance(error,app_commands.MissingRole):
        await send_error("Fehlende Berechtigungen", "<:v_kreuz:1119580775411621908> Du brauchst eine bestimmte Rolle um dies zu tun.", interaction)
        return
    if isinstance(error, app_commands.CommandOnCooldown):

        seconds_in_day = 86400
        seconds_in_hour = 3600
        seconds_in_minute = 60

        seconds = error.retry_after

        days = seconds // seconds_in_day
        seconds = seconds - (days * seconds_in_day)

        hours = seconds // seconds_in_hour
        seconds = seconds - (hours * seconds_in_hour)

        minutes = seconds // seconds_in_minute
        seconds = seconds - (minutes * seconds_in_minute)
        if math.ceil(error.retry_after) <= 60:  # seconds
            await send_error("Auf Cooldown", f"<:v_kreuz:1119580775411621908> Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(seconds)}** Sekunden erneut.", interaction)
            return
        if math.ceil(error.retry_after) <= 3600:  # minutes
            await send_error("Auf Cooldown", f"<:v_kreuz:1119580775411621908> Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(minutes)}** Minuten and **{math.ceil(seconds)}** Sekunden.", interaction)
            return
        if math.ceil(error.retry_after) <= 86400:  # hours
            await send_error("Auf Cooldown", f"<:v_kreuz:1119580775411621908> Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(hours)}** Stunden, **{math.ceil(minutes)}** Minuten and **{math.ceil(seconds)}** Sekunden.", interaction)
            return
        if math.ceil(error.retry_after) >= 86400:  # days
            await send_error("Auf Cooldown", f"<:v_kreuz:1119580775411621908> Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(days)}** Tagen, **{math.ceil(hours)}** Stunden, **{math.ceil(minutes)}** Minuten and **{math.ceil(seconds)}** Sekunden.", interaction)
            return
    if isinstance(error,app_commands.BotMissingPermissions):
        await send_error("Fehlende Berechtigungen", "<:v_kreuz:1119580775411621908> Ich habe keine Berechtigungen um das zu tun.", interaction)
        return
    if isinstance(error,app_commands.CommandNotFound):
        return
    if isinstance(error,app_commands.NoPrivateMessage):
        await send_error("Kein Zugang", "<:v_kreuz:1119580775411621908> Dieser Command funktioniert nur in Servern.", interaction)
        return
    if isinstance(error,app_commands.TransformerError):
        await send_error("Nicht gefunden", "<:v_kreuz:1119580775411621908> Die ausgewählte Person o.Ä. konnte nicht gefunden werden.", interaction)
        return
    else:
        await send_error("Unbekannt", "<:v_kreuz:1119580775411621908> Ein unbekannter Fehler ist aufgetreten.\nBitte öffne ein Ticket im [Supportserver](https://discord.gg/49jD3VXksp)", interaction)
        guilds = bot.get_guild(925729625580113951)
        channels = guilds.get_channel(925732898634600458)

        traceback_string = traceback.format_exception(type(error), error, error.__traceback__)

        embed = discord.Embed(colour=discord.Colour.red(), title="Error (Application Command)", description=f"""
<:v_info:1119579853092552715> **Informationen**
<:v_user:1119585450923929672> {interaction.user.mention}
<:v_mod:1119581819122241621> `{interaction.guild.name}` | {interaction.guild.id} ({interaction.guild.member_count})
<:v_auge:1119578772207849472> {interaction.channel.mention}
<:v_zeit:1119585888054296676> <t:{int(time.time())}:R>
<:v_haken:1119579684057907251> `/{interaction.command.name}`""")
        embed.add_field(name="<:v_pfeil_rechts:1119582171930300438> Error", value=f"```py\n" + limit_characters(''.join(traceback_string[-1]), 1010) + "```", inline=False)
        embed.add_field(name="<:v_pfeil_rechts:1119582171930300438> Traceback", value=f"```py\n" + limit_characters(''.join(traceback_string), 1010) + "```", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/811730903822368833/823531509461942294/2000px-Dialog-error-round.svg.png")
        await channels.send(embed=embed)
        return

@bot.command()
@commands.is_owner()
async def sync(ctx, serverid: int=None):
    """Synchronisiere bestimmte Commands."""
    if serverid is None:
        try:
            s = await bot.tree.sync()
            globalembed = discord.Embed(color=discord.Color.orange(), title="Synchronisierung", description=f"Die Synchronisierung von `{len(s)} Commands` wurde eingeleitet.\nEs wird ungefähr eine Stunde dauern, damit sie global angezeigt werden.")
            await ctx.send(embed=globalembed)
        except Exception as e:
            await ctx.send(f"**<:v_kreuz:1119580775411621908> Synchronisierung fehlgeschlagen**\n```\n{e}```")
    if serverid is not None:
        guild = bot.get_guild(int(serverid))
        if guild:
            try:
                s = await bot.tree.sync(guild=discord.Object(id=guild.id))
                localembed = discord.Embed(color=discord.Color.orange(), title="Synchronisierung", description=f"Die Synchronisierung von `{len(s)} Commands` ist fertig.\nEs wird nur maximal eine Minute dauern, weil sie nur auf dem Server {guild.name} synchronisiert wurden.")
                await ctx.send(embed=localembed)
            except Exception as e:
                await ctx.send(f"**<:v_kreuz:1119580775411621908> Synchronisierung fehlgeschlagen**\n```\n{e}```")
        if guild is None:
            await ctx.send(f"<:v_kreuz:1119580775411621908> Der Server mit der ID `{serverid}` wurde nicht gefunden.")

@bot.tree.context_menu(name="Nachricht melden")
async def nachricht_melden(interaction: discord.Interaction, message: discord.Message):
    async with bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SELECT channelID FROM reportlog WHERE guildID = {interaction.guild.id}")
            result = await cursor.fetchone()
            if result == None:
                return await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Diese Funktion ist hier nicht aktiviert.**", ephemeral=True)
            try:
                channel = interaction.guild.get_channel(int(result[0]))
                if channel == None:
                    return await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Der Kanal des Reportlogs existiert nicht mehr. Bitte melde dies dem lokalen Serverteam.**", ephemeral=True)
                else:
                    embed = discord.Embed(title="Nachricht Meldung", description=f"""
Der User {interaction.user.mention} hat eine Nachricht von {message.author.mention} gemeldet.

`Nachricht`: {message.content}
""", color=discord.Color.red())
                    embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                    embed.set_thumbnail(url=interaction.guild.icon)
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    await channel.send(embed=embed, view=reportmsg(message, bot))
                    await interaction.response.send_message(f"`Du hast eine Nachricht von` {message.author.mention} `gemeldet.`", ephemeral=True)
            except:
                return await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Der Kanal des Reportlogs existiert nicht mehr. Bitte melde dies dem lokalen Serverteam.**", ephemeral=True)


bot.run("OTI1Nzk5NTU5NTc2MzIyMDc4.GcwvXN.EkMMDxTqykR8em6L4lJqOouGfvAvH1J1rq9nJQ", reconnect=True)