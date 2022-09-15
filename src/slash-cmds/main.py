import os
import discord
from discord.ext import commands
import datetime
import asyncio
import traceback
import sys
from info import giveaway_end, vote_reminder, send_error, random_color, reminder_end
import topgg
import math
from discord.app_commands import AppCommandError
from discord import app_commands
import aiomysql
from googletrans import Translator
from info import discord_timestamp

dbl_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjkyNTc5OTU1OTU3NjMyMjA3OCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjQyODc4ODc1fQ.PJVIOEUe25WxuUbD1E68UF7bXpRZR_k4XXwr8ukue-c"

class Vulpo(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="vulpo!", help_command=None, case_insensitive=True, intents=discord.Intents.all())
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
        
        embed = discord.Embed(colour=discord.Colour.green(), title=f"Neuer server! ({len(bot.guilds)})",
                            description="Hier gibt es detaillierte Informationen:")
        embed.add_field(name="Name", value=guild.name)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Erstellt", value=discord_timestamp(t2, 'R'), inline=False)
        embed.add_field(name="Memberanzahl", value=guild.member_count, inline=False)
        embed.add_field(name="Owner", value=guild.owner, inline=False)
        embed.set_thumbnail(url=guild.icon if guild.icon else "https://cdn.discordapp.com/attachments/971092445435682907/973630982425047050/server_join.png")
        await channels.send(embed=embed)
        try:
            embed = discord.Embed(colour=discord.Colour.blurple(), title=f"✨ Vulpo ✨", description=f"Hallo, ich bin Vulpo, hier um diesen Server fantastisch zu machen! Ich bin jetzt in **{len(bot.guilds)}** Servern!")
            embed.add_field(name="Erster Schritt", value=f"`/help`", inline=False)
            embed.add_field(name="Links", value="**[Support server](https://discord.gg/49jD3VXksp) | [Invite](https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commandst)** | **[Vote](https://top.gg/bot/925799559576322078/vote)**", inline=False)
            embed.set_footer(text=guild.name, icon_url=guild.icon if guild.icon else 'https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024')
            embed.set_author(name="Vielen Dank für die Einladung!", icon_url="https://cdn.discordapp.com/emojis/823981604752982077.gif")
            for channel in guild.text_channels:
                await channel.send(embed=embed)
                break
        except:
            pass
    async def on_guild_remove(self, guild):
        try:
            guilds = bot.get_guild(925729625580113951)
            channels = guilds.get_channel(925732763364106290)
            
            t1 = math.floor(guild.created_at.timestamp())
            t2 = datetime.datetime.fromtimestamp(int(t1))
        
            embed = discord.Embed(colour=discord.Colour.red(), title=f"Server verlassen! ({len(bot.guilds)})",
                                    description="Hier ein paar Informationen:")
            embed.add_field(name="Name", value=guild.name)
            embed.add_field(name="ID", value=guild.id)
            embed.add_field(name="Erstellt", value=discord_timestamp(t2, 'R'), inline=False)
            embed.add_field(name="User count", value=guild.member_count, inline=False)
            embed.add_field(name="Owner", value=guild.owner, inline=False)
            embed.set_thumbnail(url=guild.icon if guild.icon else 'https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024')
            await channels.send(embed=embed)
        except:
            pass

        try:
            embed = discord.Embed(colour=discord.Colour.orange(), title=f"Hallo {guild.owner.name}", description=f"""
            Könnten Sie sich eine Minute Zeit nehmen, um uns zu sagen, warum Sie Vulpo von Ihrem Server `{guild.name}` entfernt haben und ob Sie irgendwelche Vorschläge haben?
            Wenn Sie etwas sagen möchten, antworten Sie innerhalb der nächsten 15 Minuten auf diese DM!

            ~Vinc (Entwickler)""")
            embed.set_thumbnail(url=guild.icon if guild.icon else 'https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024')
            await guild.owner.send(embed=embed)

            def check(m):
                return m.author == guild.owner and m.guild == None
            try:
                input = await bot.wait_for('message', timeout=900, check=check)
            except asyncio.TimeoutError:
                return
            else:
                embed = discord.Embed(colour=discord.Colour.green(), title="Vielen Dank für Ihr Feedback", description="Wenn Sie noch weitere Fragen haben, dann treten Sie dem [Supportserver](https://discord.gg/49jD3VXksp) bei.")
                await guild.owner.send(embed=embed)
                guilds = bot.get_guild(925729625580113951)
                channels = guilds.get_channel(925732763364106290)
                await channels.send(f"**{guild.owner}({guild.owner.id})** hat ein Feedback nach dem Kicken von Vulpo, auf dem Server `{guild.name}({guild.id})` hinterlassen:\n*{input.content}*")
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

                user = await bot.fetch_user(userid)
                if user:
                    embed = discord.Embed(title=f"Danke vielmals {user}!", description=f"{user.mention} hat insgesammt {times} Mal gevotet.\n\nDu kannst **[hier](https://top.gg/bot/925799559576322078/vote)** alle 12 Stunden voten.", colour=discord.Colour.orange())
                    embed.set_thumbnail(url=user.avatar)
                    embed.set_footer(text="Durch einen Vote erhältst du 300 Coins sowie die Voter Rolle", icon_url="https://cdn.discordapp.com/attachments/934190768690704544/934766688791035924/6139-upvote.png")
                    await channel.send(embed=embed)
                else:
                    embed = discord.Embed(title=f"Danke vielmals {userid}!", description=f"{userid} hat insgesammt {times} Mal gevotet.\n\nDu kannst **[hier](https://top.gg/bot/925799559576322078/vote)** alle 12 Stunden voten.", colour=discord.Colour.orange())
                    embed.set_footer(text="Durch einen Vote erhältst du 300 Coins sowie die Voter Rolle", icon_url="https://cdn.discordapp.com/attachments/934190768690704544/934766688791035924/6139-upvote.png")
                    await channel.send(embed=embed)
                await cursor.execute(f"SELECT rucksack, bank, job, stunden FROM economy WHERE userID = {user.id}")
                result = await cursor.fetchone()
                if result is None:
                    await cursor.execute("INSERT INTO economy(rucksack, bank, job, stunden, userID) VALUES(%s, %s, %s, %s, %s)",("0", "0", "Kein Job", "0", user.id))
                    
                    bal = 0
                else:
                    bal = int(result[0])
                new = bal + 300
                await cursor.execute("UPDATE economy SET rucksack = (%s) WHERE userID = (%s)", (new, user.id))
                

                time_to_convert = math.floor(datetime.datetime.utcnow().timestamp() + 43200)
                time_converted = datetime.datetime.fromtimestamp(int(time_to_convert))
                asyncio.create_task(vote_reminder(time_converted, bot, userid))
                await cursor.execute("INSERT INTO vote(userid, endtime) VALUES(%s, %s)", (userid, time_to_convert))
                

                dblpy = topgg.DBLClient(bot, dbl_token, autopost_interval=0)
                votedata = await dblpy.get_bot_info()
                votes = int(votedata["monthly_points"])
                guild = bot.get_guild(925729625580113951)
                votechannel = guild.get_channel(934036446271139860)
                mydate = datetime.datetime.now()
                translator = Translator()
                translation = translator.translate(mydate.strftime("%B") , dest="de")
                await votechannel.edit(name=f"Votes im {translation.text}: {votes}")
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
                guild = bot.get_guild(925729625580113951)
                channel = guild.get_channel(934036224413417472)

                userid = int(data["user"])
                user = await bot.fetch_user(userid)
                if user:
                    embed = discord.Embed(title=f"{user} hat gevotet!", description=f"Testvote erfolgreich\n\nDu kannst **[hier](https://top.gg/bot/925799559576322078/vote)** alle 12 Stunden voten.", colour=discord.Colour.gold())
                    embed.set_thumbnail(url=user.avatar)
                    embed.set_footer(text="Danke für deine Unterstützung", icon_url="https://cdn.discordapp.com/attachments/934190768690704544/934766688791035924/6139-upvote.png")
                    await channel.send(embed=embed)
                else:
                    embed = discord.Embed(title=f"{userid} hat gevotet!", description=f"Testvote erfolgreich\n\nDu kannst **[hier](https://top.gg/bot/925799559576322078/vote)** alle 12 Stunden voten.", colour=discord.Colour.gold())
                    embed.set_footer(text="Danke für deine Unterstützung", icon_url="https://cdn.discordapp.com/attachments/934190768690704544/934766688791035924/6139-upvote.png")
                    await channel.send(embed=embed)

                try:
                    await cursor.execute(f"SELECT votes FROM topgg WHERE userID = {userid}")
                    result = await cursor.fetchone()
                    if result is None or result is False:
                        await cursor.execute(f"INSERT INTO topgg(userID, votes) VALUES(%s, %s)", (userid, 1))
                        times = 1
                    else:
                        await cursor.execute(f"UPDATE topgg SET votes = (%s) WHERE userID = (%s)", (int(result[0]) + 1, userid))
                        times = int(result[0]) + 1
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
                
    async def setup_hook(self):
        try:
            loop = asyncio.get_event_loop()
            pool = await aiomysql.create_pool(host='142.132.233.69', port=3306, user='u64287_BGWSJv8tMk', password='FIuqyfN+Qbl^c3422vps7Xci', db='s64287_Vulpo', loop=loop, autocommit=True, maxsize=25)
            bot.pool = pool
            print(f"✅ Pool erstellt")
        except:
            print(f"❌ Fehler bei der Pool Erstellung")
        async with bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("/dblwebhook", "Vulpo123321")
                    await topgg_webhook.run(25505)
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
            
            for filename in os.listdir("./cogs"):
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
            await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.playing, name="mit Slash-Commands"))
            print("✅ Status bereit")
        except:
            print("❌ Status nicht bereit")

bot = Vulpo()

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await send_error("Fehlende Berechtigungen", "❌ Du hast nicht die Rechte, diesen Command auszuführen.", interaction)
        return
    if isinstance(error,app_commands.CommandInvokeError):
        pass
    if isinstance(error,app_commands.MissingAnyRole):
        await send_error("Fehlende Berechtigungen", "❌ Du brauchst eine bestimmte Rolle um dies zu tun.", interaction)
        return
    if isinstance(error,app_commands.MissingRole):
        await send_error("Fehlende Berechtigungen", "❌ Du brauchst eine bestimmte Rolle um dies zu tun.", interaction)
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
            await send_error("Auf Cooldown", f"❌ Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(seconds)}** Sekunden erneut.", interaction)
            return
        if math.ceil(error.retry_after) <= 3600:  # minutes
            await send_error("Auf Cooldown", f"❌ Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(minutes)}** Minuten and **{math.ceil(seconds)}** Sekunden.", interaction)
            return
        if math.ceil(error.retry_after) <= 86400:  # hours
            await send_error("Auf Cooldown", f"❌ Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(hours)}** Stunden, **{math.ceil(minutes)}** Minuten and **{math.ceil(seconds)}** Sekunden.", interaction)
            return
        if math.ceil(error.retry_after) >= 86400:  # days
            await send_error("Auf Cooldown", f"❌ Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(days)}** Tagen, **{math.ceil(hours)}** Stunden, **{math.ceil(minutes)}** Minuten and **{math.ceil(seconds)}** Sekunden.", interaction)
            return
    if isinstance(error,app_commands.BotMissingPermissions):
        await send_error("Fehlende Berechtigungen", "❌ Ich habe keine Berechtigungen um das zu tun.", interaction)
        return
    if isinstance(error,app_commands.CommandNotFound):
        return
    if isinstance(error,app_commands.NoPrivateMessage):
        await send_error("Kein Zugang", "❌ Dieser Command funktioniert nur in Servern.", interaction)
        return
    else:
        await send_error("Unbekannt", "❌ Ein unbekannter Fehler ist aufgetreten.\nBitte öffne ein Ticket im [Supportserver](https://discord.gg/49jD3VXksp)", interaction)
        guilds = bot.get_guild(925729625580113951)
        channels = guilds.get_channel(925732898634600458)

        traceback_string = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        to_send = f"```py\n {traceback_string}```"

        embed = discord.Embed(colour=discord.Colour.red(), title=type(error), description=to_send)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_author(name=f"{interaction.user} | {interaction.user.id}", icon_url=interaction.user.avatar)
        embed.set_footer(text=f"{interaction.guild.name} | {interaction.guild.id}", icon_url=interaction.guild.icon)
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
            await ctx.send(f"**❌ Synchronisierung fehlgeschlagen**\n```\n{e}```")
    if serverid is not None:
        guild = bot.get_guild(int(serverid))
        if guild:
            try:
                s = await bot.tree.sync(guild=discord.Object(id=guild.id))
                localembed = discord.Embed(color=discord.Color.orange(), title="Synchronisierung", description=f"Die Synchronisierung von `{len(s)} Commands` ist fertig.\nEs wird nur maximal eine Minute dauern, weil sie nur auf dem Server {guild.name} synchronisiert wurden.")
                await ctx.send(embed=localembed)
            except Exception as e:
                await ctx.send(f"**❌ Synchronisierung fehlgeschlagen**\n```\n{e}```")
        if guild is None:
            await ctx.send(f"❌ Der Server mit der ID `{serverid}` wurde nicht gefunden.")

bot.run("OTI1Nzk5NTU5NTc2MzIyMDc4.G1pfSR.RNwGXR2kWHPhVs2d6MLFbjL33Q9lHYT7GcnRVU", reconnect=True, log_handler=None)