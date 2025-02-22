import os
import discord
from discord.ext import commands
import datetime
import asyncio
import traceback
import sys
from utils.utils import giveaway_end, vote_reminder, send_error, random_color, reminder_end, limit_characters, addwarn
import topgg
import math
from discord.app_commands import AppCommandError, CommandTree
from discord import app_commands
import aiomysql
from googletrans import Translator
from utils.utils import discord_timestamp, fetch_role
import time
from utils.MongoDB import getMongoDataBase
from cogs.economy import update_account
from dotenv import load_dotenv

load_dotenv()

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
        
        await interaction.response.send_message("**<:v_checkmark:1264271011818242159> Nutzer wurde verwarnt.**", ephemeral=True)
        await addwarn(self, user, interaction, grund)
 
class MyTree(CommandTree):
    async def interaction_check(self, interaction: discord.Interaction):
        return True
    #     try:
    #         user = interaction.user
    #         result = await getMongoDataBase()["banned"].find_one({"userID": str(user.id)})
    #         if result is not None:
    #                 embed = discord.Embed(title="<:v_168:1264268507193806900> Du bist gebannt", description=f"""
    # > <:v_12:1264264683427336259> Mit einem Bann hast du keinen Zugang mehr zu Vulpo's Befehlen. Außerdem hast du keinen Zutritt zum Supportserver "Vulpo's Wald".
    # <:v_24:1264264867511144479> Grund: {result["reason"]}
    # <:v_17:1264264737810550814> Falls du denkst, dass du dich geändert hast, oder du zu unrecht bestraft wurdest, kannst du einen [Entbannungsantrag](https://forms.gle/NH1Jb1gVNEPuTLA58) stellen.
    # """, colour=0xac0000)
    #                 await interaction.followup.send(embed=embed, ephemeral=True)
    #                 return False
    #         return True
    #     except:
    #         pass
        

class Vulpo(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix="vulpodev!", help_command=None, case_insensitive=True, intents=discord.Intents.all(), tree_cls=MyTree)
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
        guilds = await bot.fetch_guild(925729625580113951)
        channels = await guilds.fetch_channel(925732763364106290)
        
        t1 = math.floor(guild.created_at.timestamp())
        t2 = datetime.datetime.fromtimestamp(int(t1))
        msg = f"""
        <:v_12:1264264683427336259> **Informationen**
        🍪 {guild.name} ({guild.id})
        <:v_user:1264270983636975666> {guild.owner} ({guild.owner.id})
        <:v_arrow_left:1264271794936746054> {guild.member_count}
        <:v_stopwatch:1264271803774140608> {discord_timestamp(t2, 'R')}
       	
        <:v_12:1264264683427336259> **Vulpo ist jetzt auf {len(bot.guilds)} Servern drauf! Yay 🎉**
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
            <:v_12:1264264683427336259> **Informationen**
            🍪 {guild.name} ({guild.id})
            <:v_user:1264270983636975666> {guild.owner} ({guild.owner.id})
            <:v_arrow_left:1264271794936746054> {guild.member_count}
            <:v_stopwatch:1264271803774140608> {discord_timestamp(t2, 'R')}

            <:v_12:1264264683427336259> **Vulpo ist jetzt auf {len(bot.guilds)} Servern drauf!**
            """
            
            embed = discord.Embed(colour=discord.Colour.red(), title=f"Vulpo wurde aus {guild.name} rausgeschmissen!", description=msg)
            embed.set_thumbnail(url=guild.icon if guild.icon else 'https://media.discordapp.net/attachments/1023508002453594122/1023508257022672936/Vulpo_neu.png?width=1549&height=1549')
            await channels.send(embed=embed)
        except:
            pass
    
    async def on_dbl_vote(self, data):
        if data["type"] == "test":
            return bot.dispatch('dbl_test', data)
        
        db = getMongoDataBase()
        
        userid = int(data["user"])
        guild = await bot.fetch_guild(925729625580113951)
        channel = await guild.fetch_channel(934036224413417472)
        result = await db['topgg'].find_one({"userID": str(userid)})
        if result is None or result is False:
            await db['topgg'].insert_one({"userID": str(userid), "votes": 1})
            
            times = 1
        else:
            await db['topgg'].update_one({"userID": str(userid)}, {"$set": {"votes": int(result["votes"]) + 1}})
            
            times = int(result["votes"]) + 1

        time_to_convert = math.floor(datetime.datetime.now().timestamp() + 43200)
        time_converted = datetime.datetime.fromtimestamp(int(time_to_convert))
        asyncio.create_task(vote_reminder(time_converted, bot, userid))
        await db['vote'].insert_one({"userid": str(userid), "endtime": time_to_convert})

        user = await bot.fetch_user(userid)
        rolle = await fetch_role(guild, 1041046601394815127)
        member = await guild.fetch_member(userid)
        if user:
            embed = discord.Embed(title=f"Danke vielmals {user.name}!", description=f"{user.mention} hat insgesammt {times} Mal gevotet.", colour=discord.Colour.orange())
            embed.set_thumbnail(url=user.avatar)
            if member:
                embed.set_footer(text="Durch einen Vote erhältst du 300 Cookies und die Voter Rolle", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508227117289472/herz.png")
                if rolle in member.roles:
                    embed.description += f"\n<:v_stopwatch:1264271803774140608> Du wirst in 12 Stunden erinnert, wieder zu voten."
                else:
                    embed.description += f"\n<:v_stopwatch:1264271803774140608> Deine Vote Erinnerungen sind aus. Du kannst sie in **Kanäle und Rollen** aktivieren."
            if member == None:
                embed.set_footer(text="Durch einen Vote erhältst du 300 Cookies", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508227117289472/herz.png")
            await channel.send(embed=embed, view=voteView())
        else:
            embed = discord.Embed(title=f"Danke vielmals {userid}!", description=f"{userid} hat insgesamt {times} Mal gevotet.", colour=discord.Colour.orange())
            embed.set_footer(text="Durch einen Vote erhältst du 300 Cookies", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508227117289472/herz.png")
            await channel.send(embed=embed, view=voteView())
        

        await update_account(self, user, "rucksack", 300, 0)       

        dblpy = topgg.DBLClient(bot, os.getenv("dbl_token"), autopost_interval=0)
        votedata = await dblpy.get_bot_info()
        votes = int(votedata["monthly_points"])
        guild = await bot.fetch_guild(925729625580113951)
        votechannel = await guild.fetch_channel(934036446271139860)
        mydate = datetime.datetime.now()
        translator = Translator()
        translation = translator.translate(f'Month {mydate.strftime("%B")}' , dest="de")
        await votechannel.edit(name=f"Votes {translation.text}: {votes}")
        try:
            if member is not None:
                voter = await fetch_role(guild, 962753309997932554)
                await member.add_roles(voter)
                if int(times) >= 200:
                    votemeister = await fetch_role(guild, 962753328679358515)
                    await member.add_roles(votemeister)
                    return
                if int(times) >= 100:
                    megavoter = await fetch_role(guild, 962753332139663390)
                    await member.add_roles(megavoter)
                    return
                if int(times) >= 50:
                    ehrenhaftervoter = await fetch_role(guild, 962753335507701780)
                    await member.add_roles(ehrenhaftervoter)
                    return
                if int(times) >= 20:
                    aktivervoter = await fetch_role(guild, 962753338666008607)
                    await member.add_roles(aktivervoter)
                    return
        except:
            pass
        
    async def on_dbl_test(self, data):
        userid = int(data["user"])

        db = getMongoDataBase()

        guild = await bot.fetch_guild(925729625580113951)
        channel = await guild.fetch_channel(934036224413417472)
        result = await db['topgg'].find_one({"userID": str(userid)})
        times = result["votes"]

        rolle = fetch_role(guild, 1041046601394815127)
        member = await guild.fetch_member(int(userid))

        user = await bot.fetch_user(userid)
        if user:
            embed = discord.Embed(title=f"Danke vielmals {user}!", description=f"{user.mention} hat insgesammt {times} Mal gevotet.", colour=discord.Colour.yellow())
            embed.set_thumbnail(url=user.avatar)
            embed.set_author(name="Testvote erfolgreich", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1037064093124788284/v_info.png")
            if member:
                embed.set_footer(text="Durch einen Vote erhältst du 300 Cookies und die Voter Rolle", icon_url="https://media.discordapp.net/attachments/1023508002453594122/1023508227117289472/herz.png")
                if rolle in member.roles:
                    embed.description += f"\n<:v_stopwatch:1264271803774140608> Du wirst in 12 Stunden erinnert, wieder zu voten."
                else:
                    embed.description += f"\n<:v_stopwatch:1264271803774140608> Deine Vote Erinnerungen sind aus. Du kannst sie in **Kanäle und Rollen** aktivieren."
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
            topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("/dblwebhook", "Vulpo123321")
            await topgg_webhook.run(8000)
            print("✅ Verbunden mit der topgg api")
        except:
            print("❌ Verbindung zur topgg api fehlgeschlagen")
              
        db = getMongoDataBase()
                    
        if self.giveaways is False:
            self.giveaways = True
            result = await db["gewinnspiele"].find({"status": "Aktiv"}).to_list(length=None)
            if str(result) == "()":
                print(f"✅ Asyncio tasks für Giveaways bereit(0)")
            else:
                a = 0
                for giveaway in result:
                    time_to_convert = int(giveaway["endtime"])
                    try:
                        time_converted = datetime.datetime.fromtimestamp(time_to_convert)
                        a += 1
                        asyncio.create_task(giveaway_end(time_converted, bot, int(giveaway['msgID'])))
                    except OSError as e:
                        pass
                print(f"✅ Asyncio tasks für Giveaways bereit({a})")
                    
        if self.votes is False:
            self.votes = True
            result = await db["vote"].find({}).to_list(length=None)
            a = 0
            for c in result:
                time_to_convert = int(c["endtime"])
                try:
                    time_converted = datetime.datetime.fromtimestamp(time_to_convert)
                    a += 1
                    asyncio.create_task(vote_reminder(time_converted, bot, int(c['userid'])))
                except OSError as e:
                    pass
            print(f"✅ Asyncio tasks für Vote bereit({a})")
                    
        if self.reminder is False:
            self.reminder = True
            result = await db["erinnerungen"].find({}).to_list(length=None)
            a = 0
            for c in result:
                time_to_convert = int(c["endtime"])
                try:
                    time_converted = datetime.datetime.fromtimestamp(time_to_convert)
                    a += 1
                    asyncio.create_task(reminder_end(time_converted, bot, c['userID'], c['id']))
                except OSError as e:
                    pass
            print(f"✅ Asyncio tasks für Erinnerungen bereit({a})")
        
        await db["banned"].delete_many({})
        
        guild = await bot.fetch_guild(925729625580113951)
        banned_users = [ban async for ban in guild.bans()]
        for entry in banned_users:
            banned_user = entry.user
            await db['banned'].update_one({"userID": banned_user.id}, {"$setOnInsert": {"userID": banned_user.id, "reason": entry.reason}}, upsert=True)
            
        print ("✅ Banned User wurden geladen")
            
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
        print("✅ Alle System sind nun bereit.")

bot = Vulpo()

@bot.event
async def on_error(ctx, error):
    return 

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: AppCommandError):    
    
    if not interaction.response.is_done():
        await interaction.response.defer()
    
    if isinstance(error, app_commands.MissingPermissions):
        await send_error("Fehlende Berechtigungen", "<:v_x:1264270921452224562> Du hast nicht die Rechte, diesen Command auszuführen.", interaction)
        return
    if isinstance(error,app_commands.CommandInvokeError):
        pass
    if isinstance(error,app_commands.MissingAnyRole):
        await send_error("Fehlende Berechtigungen", "<:v_x:1264270921452224562> Du brauchst eine bestimmte Rolle um dies zu tun.", interaction)
        return
    if isinstance(error,app_commands.MissingRole):
        await send_error("Fehlende Berechtigungen", "<:v_x:1264270921452224562> Du brauchst eine bestimmte Rolle um dies zu tun.", interaction)
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
            await send_error("Auf Cooldown", f"<:v_x:1264270921452224562> Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(seconds)}** Sekunden erneut.", interaction)
            return
        if math.ceil(error.retry_after) <= 3600:  # minutes
            await send_error("Auf Cooldown", f"<:v_x:1264270921452224562> Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(minutes)}** Minuten und **{math.ceil(seconds)}** Sekunden erneut.", interaction)
            return
        if math.ceil(error.retry_after) <= 86400:  # hours
            await send_error("Auf Cooldown", f"<:v_x:1264270921452224562> Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(hours)}** Stunden, **{math.ceil(minutes)}** Minuten und **{math.ceil(seconds)}** Sekunden erneut.", interaction)
            return
        if math.ceil(error.retry_after) >= 86400:  # days
            await send_error("Auf Cooldown", f"<:v_x:1264270921452224562> Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(days)}** Tagen, **{math.ceil(hours)}** Stunden, **{math.ceil(minutes)}** Minuten und **{math.ceil(seconds)}** Sekunden erneut.", interaction)
            return
    if isinstance(error,app_commands.BotMissingPermissions):
        await send_error("Fehlende Berechtigungen", "<:v_x:1264270921452224562> Ich habe keine Berechtigungen um das zu tun.", interaction)
        return
    if isinstance(error,app_commands.CommandNotFound):
        return
    if isinstance(error,app_commands.NoPrivateMessage):
        await send_error("Kein Zugang", "<:v_x:1264270921452224562> Dieser Command funktioniert nur in Servern.", interaction)
        return
    if isinstance(error,app_commands.TransformerError):
        await send_error("Nicht gefunden", "<:v_x:1264270921452224562> Die ausgewählte Person o.Ä. konnte nicht gefunden werden.", interaction)
        return
    else:
        await send_error("Unbekannt", "<:v_x:1264270921452224562> Ein unbekannter Fehler ist aufgetreten.\nBitte öffne ein Ticket im [Supportserver](https://discord.gg/49jD3VXksp)", interaction)
        guilds = await bot.fetch_guild(925729625580113951)
        channels = await guilds.fetch_channel(925732898634600458)

        traceback_string = traceback.format_exception(type(error), error, error.__traceback__)

        embed = discord.Embed(colour=discord.Colour.red(), title="Error (Application Command)", description=f"""
<:v_12:1264264683427336259> **Informationen**
<:v_arrow_left:1264271794936746054> {interaction.user.mention}
<:v_168:1264268507193806900> `{interaction.guild.name}` | {str(interaction.guild.id)} ({interaction.guild.member_count})
<:v_104:1264266670810071202> {interaction.channel.mention}
<:v_stopwatch:1264271803774140608> <t:{int(time.time())}:R>
<:v_checkmark:1264271011818242159> `/{interaction.command.name}`""")
        embed.add_field(name="<:v_24:1264264867511144479> Error", value=f"```py\n" + limit_characters(''.join(traceback_string[-1]), 1010) + "```", inline=False)
        embed.add_field(name="<:v_24:1264264867511144479> Traceback", value=f"```py\n" + limit_characters(''.join(traceback_string), 1010) + "```", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/811730903822368833/823531509461942294/2000px-Dialog-error-round.svg.png")
        await channels.send(embed=embed)
        return

@bot.command()
@commands.is_owner()
async def sync(ctx, serverid=None):
    """Synchronisiere bestimmte Commands."""
    if serverid is None:
        try:
            s = await bot.tree.sync()
            globalembed = discord.Embed(color=discord.Color.orange(), title="Synchronisierung", description=f"Die Synchronisierung von `{len(s)} Commands` wurde eingeleitet.\nEs wird ungefähr eine Stunde dauern, damit sie global angezeigt werden.")
            await ctx.send(embed=globalembed)
        except Exception as e:
            await ctx.send(f"**<:v_x:1264270921452224562> Synchronisierung fehlgeschlagen**\n```\n{e}```")
    if serverid is not None:
        guild = await bot.fetch_guild(int(serverid))
        if guild:
            try:
                s = await bot.tree.sync(guild=discord.Object(id=guild.id))
                localembed = discord.Embed(color=discord.Color.orange(), title="Synchronisierung", description=f"Die Synchronisierung von `{len(s)} Commands` ist fertig.\nEs wird nur maximal eine Minute dauern, weil sie nur auf dem Server {guild.name} synchronisiert wurden.")
                await ctx.send(embed=localembed)
            except Exception as e:
                await ctx.send(f"**<:v_x:1264270921452224562> Synchronisierung fehlgeschlagen**\n```\n{e}```")
        if guild is None:
            await ctx.send(f"<:v_x:1264270921452224562> Der Server mit der ID `{serverid}` wurde nicht gefunden.")

@bot.tree.context_menu(name="Nachricht melden")
async def nachricht_melden(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer()
    result = await getMongoDataBase()["reportlog"].find_one({"guildID": str(interaction.guild.id)})
    if result == None:
        return await interaction.followup.send("**<:v_x:1264270921452224562> Diese Funktion ist hier nicht aktiviert.**", ephemeral=True)
    try:
        channel = await interaction.guild.fetch_channel(int(result["channelID"]))
        if channel == None:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Der Kanal des Reportlogs existiert nicht mehr. Bitte melde dies dem lokalen Serverteam.**", ephemeral=True)
        else:
            embed = discord.Embed(title="Nachricht Meldung", description=f"""
Der User {interaction.user.mention} hat eine Nachricht von {message.author.mention} gemeldet.

`Nachricht`: {message.content}
""", color=discord.Color.red())
            
            embed.set_thumbnail(url=interaction.guild.icon)
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            await channel.send(embed=embed, view=reportmsg(message, bot))
            await interaction.followup.send(f"`Du hast eine Nachricht von` {message.author.mention} `gemeldet.`", ephemeral=True)
    except:
        return await interaction.followup.send("**<:v_x:1264270921452224562> Der Kanal des Reportlogs existiert nicht mehr. Bitte melde dies dem lokalen Serverteam.**", ephemeral=True)


bot.run(os.getenv("token"), reconnect=True)