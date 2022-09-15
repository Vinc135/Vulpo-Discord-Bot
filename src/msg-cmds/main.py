import discord
from discord.ext import commands
import mysql.connector
import datetime
import asyncio
import traceback
import sys
from info import giveaway_end, vote_reminder
import topgg
import math

class Dropdown(discord.ui.Select):
    def __init__(self):
        selectOptions = [
            discord.SelectOption(label="Information", emoji="👀"),
            discord.SelectOption(label="Economy", emoji="🍪"),
            discord.SelectOption(label="Levelsystem", emoji="🆙"),
            discord.SelectOption(label="Giveaway", emoji="🎉"),
            discord.SelectOption(label="Bilder", emoji="🖼"),
            discord.SelectOption(label="NSFW", emoji="🔞"),
            discord.SelectOption(label="Fun", emoji="😂"),
            discord.SelectOption(label="Moderation", emoji="🚨"),
            discord.SelectOption(label="Server-Management", emoji="🎛"),
            discord.SelectOption(label="Settings & Setup", emoji="🛠"),
            discord.SelectOption(label="Logging & Chats", emoji="📝"),
            discord.SelectOption(label="Bot", emoji="🤖"),
        ]
        super().__init__(placeholder="Wähle eine Seite", min_values=1, max_values=1, options=selectOptions, custom_id="Dropdown-Help")
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Information":
            cog = bot.get_cog("meta")
            commands = cog.get_commands()
            anzeige = ""
            for command in commands:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '} - {command.help if command.help else 'Keine Beschreibung'}\n"
            embed = discord.Embed(colour=discord.Colour.orange(), description=anzeige)
            embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Economy":
            cog = bot.get_cog("economy")
            commands = cog.get_commands()
            anzeige = ""
            for command in commands:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            embed = discord.Embed(colour=discord.Colour.orange(), description=anzeige)
            embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Levelsystem":
            cog = bot.get_cog("levelsystem")
            commands = cog.get_commands()
            anzeige = ""
            for command in commands:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            embed = discord.Embed(colour=discord.Colour.orange(), description=anzeige)
            embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Giveaway":
            cog = bot.get_cog("giveaway")
            commands = cog.get_commands()
            anzeige = ""
            for command in commands:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            embed = discord.Embed(colour=discord.Colour.orange(), description=anzeige)
            embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Bilder":
            cog = bot.get_cog("bilder")
            commands = cog.get_commands()
            anzeige = ""
            for command in commands:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            embed = discord.Embed(colour=discord.Colour.orange(), description=anzeige)
            embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "NSFW":
            if interaction.channel.is_nsfw():
                cog = bot.get_cog("Nsfw")
                commands = cog.get_commands()
                anzeige = ""
                for command in commands:
                    anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
                embed = discord.Embed(colour=discord.Colour.orange(), description=anzeige)
                embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
                embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
                return await interaction.response.edit_message(embed=embed)
            else:
                embed = discord.Embed(colour=discord.Colour.orange(), description="Du kannst die NSFW Commands nur in einem NSFW Kanal einsehen.")
                embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
                embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
                return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Fun":
            cog = bot.get_cog("fun")
            commands = cog.get_commands()
            anzeige = ""
            for command in commands:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            embed = discord.Embed(colour=discord.Colour.orange(), description=anzeige)
            embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Moderation":
            cog = bot.get_cog("moderation")
            commands = cog.get_commands()
            anzeige = ""
            for command in commands:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            embed = discord.Embed(colour=discord.Colour.orange(), description=anzeige)
            embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Server-Management":
            cog = bot.get_cog("server")
            commands = cog.get_commands()
            anzeige = ""
            for command in commands:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            embed = discord.Embed(colour=discord.Colour.orange(), description=anzeige)
            embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Settings & Setup":
            cog = bot.get_cog("joinrole")
            cog2 = bot.get_cog("tempchannel")
            cog3 = bot.get_cog("reactionrole")
            commands = cog.get_commands()
            commands2 = cog2.get_commands()
            commands3 = cog3.get_commands()
            anzeige = "**prefix** - Damit kannst du das Prefix deines Servers ändern.\n**createpanel** - Erstelle ein Panel für Tickets."
            for command in commands:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            for command in commands2:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            for command in commands3:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            embed = discord.Embed(colour=discord.Colour.orange(), description=anzeige)
            embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Logging & Chats":
            cog = bot.get_cog("logging")
            cog2 = bot.get_cog("message")
            commands = cog.get_commands()
            commands2 = cog2.get_commands()
            anzeige = "**globalchat [channel]** - Erstelle einen Globalchat für deinen Server.\n**count [channel]** - Lege einen Kanal fest, indem gezählt wird.\n**setcount <zahl>** - Lege eine neue Zahl fest, ab der begonnen wird zu zählen."
            for command in commands:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            for command in commands2:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            embed = discord.Embed(colour=discord.Colour.orange(), description=anzeige)
            embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
            return await interaction.response.edit_message(embed=embed)
        if self.values[0] == "Bot":
            cog = bot.get_cog("vulpo")
            commands = cog.get_commands()
            anzeige = ""
            for command in commands:
                anzeige += f"**{command.name}** {f'`{command.usage}`' if command.usage else ' '}- {command.help if command.help else 'Keine Beschreibung'}\n"
            embed = discord.Embed(colour=discord.Colour.orange(), description=anzeige)
            embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
            embed.set_author(name=f"Command Menü | {self.values[0]}", icon_url="https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
            return await interaction.response.edit_message(embed=embed)


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())


dbl_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjkyNTc5OTU1OTU3NjMyMjA3OCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjQyODc4ODc1fQ.PJVIOEUe25WxuUbD1E68UF7bXpRZR_k4XXwr8ukue-c"

def get_prefix(bot, message):
    try:
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo",
            auth_plugin = "mysql_native_password"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT prefix FROM prefixes WHERE guild_id = {message.guild.id}")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO prefixes (guild_id, prefix) VALUES (%s , %s)", (message.guild.id, "v!"))
            mydb.commit()
            return "v!"

        if result is not None:
            pre = result[0]
            return pre

        mydb.close()
    except:
        pass

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
    
class Vulpo(commands.Bot):      
    def __init__(self):
        super().__init__(command_prefix=(get_prefix), help_command=None, case_insensitive=True, intents=intents)
        self.initial_extensions = [
            "cogs.bilder",
            "cogs.economy",
            "cogs.error",
            "cogs.fun",
            "cogs.giveaway",
            "cogs.guild",
            "cogs.joinrole",
            "cogs.levels",
            "cogs.logging",
            "cogs.message",
            "cogs.meta",
            "cogs.mod",
            "cogs.nsfw",
            "cogs.owner",
            "cogs.reactionrole",
            "cogs.ticketsystem",
            "cogs.vulpo",
            "cogs.tempchannel",
            "cogs.globalchat",
            "cogs.counting"
        ]
        self.giveaways = False
        self.votes = False
    async def on_guild_join(self, guild):
        guilds = bot.get_guild(925729625580113951)
        channels = guilds.get_channel(925732763364106290)
        embed = discord.Embed(colour=discord.Colour.green(), title=f"Neuer server! ({len(bot.guilds)})",
                            description="Hier ein paar Informationen:")
        embed.add_field(name="Name", value=f"{guild.name}", inline=False)
        embed.add_field(name="ID", value=f"{guild.id}", inline=False)
        embed.add_field(name="Erstellt", value=f"{guild.created_at.__format__('am %d.%m.%Y %X')}",
                        inline=False)
        embed.add_field(name="Memberanzahl", value=f"{guild.member_count}", inline=False)
        embed.add_field(name="Owner", value=f"{guild.owner}", inline=False)
        embed.set_thumbnail(url=guild.icon if guild.icon else 'https://cdn.discordapp.com/icons/925729625580113951/63a2e510fb885f12da3173da3413864c.png?size=1024')
        await channels.send(embed=embed)
        try:
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT prefix FROM prefixes WHERE guild_id = {guild.id}")
            result = cursor.fetchone()
            if result == None:
                cursor.execute("INSERT INTO prefixes (guild_id, prefix) VALUES (%s , %s)", (guild.id, "v!"))
                mydb.commit()
                pre = "v!"

            if result is not None:
                pre = result[0]

            mydb.close()
            embed = discord.Embed(colour=discord.Colour.blurple(), title=f"✨ Vulpo ✨", description=f"Hallo, ich bin Vulpo, hier um diesen Server fantastisch zu machen! Ich bin jetzt in **{len(bot.guilds)}** Servern!")
            embed.add_field(name="Erste Schritte", value=f"Prefix: `{pre}`\nListe von all meinen Commands: `{pre}help`", inline=False)
            embed.add_field(name="Links", value="**[Support server](https://discord.gg/49jD3VXksp) | [Invite](https://discord.com/api/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot)** | **[Vote](https://top.gg/bot/925799559576322078/vote)**", inline=False)
            embed.set_footer(text=guild.name, icon_url=guild.icon if guild.icon else 'https://cdn.discordapp.com/icons/925729625580113951/63a2e510fb885f12da3173da3413864c.png?size=1024')
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
            embed = discord.Embed(colour=discord.Colour.red(), title=f"Server verlassen! ({len(bot.guilds)})",
                                    description="Hier ein paar Informationen:")
            embed.add_field(name="Name", value=f"{guild.name}", inline=False)
            embed.add_field(name="ID", value=f"{guild.id}", inline=False)
            embed.add_field(name="Erstellt", value=f"{guild.created_at.__format__('am %d.%m.%Y %X')}",
                            inline=False)
            embed.add_field(name="User count", value=f"{guild.member_count}", inline=False)
            embed.add_field(name="Owner", value=f"{guild.owner}", inline=False)
            embed.set_thumbnail(url=guild.icon if guild.icon else 'https://cdn.discordapp.com/icons/925729625580113951/63a2e510fb885f12da3173da3413864c.png?size=1024')
            await channels.send(embed=embed)
        except:
            pass

        try:
            embed = discord.Embed(colour=discord.Colour.orange(), title=f"Hallo {guild.owner.name}", description=f"""
            Könnten Sie sich eine Minute Zeit nehmen, um uns zu sagen, warum Sie Vulpo von Ihrem Server `{guild.name}` entfernt haben und ob Sie irgendwelche Vorschläge haben?
            Wenn Sie etwas sagen möchten, antworten Sie innerhalb der nächsten 15 Minuten auf diese DM!

            ~Vinc (Entwickler)""")
            embed.set_thumbnail(url=guild.icon if guild.icon else 'https://cdn.discordapp.com/icons/925729625580113951/63a2e510fb885f12da3173da3413864c.png?size=1024')
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
        
        userid = int(data["user"])

        guild = bot.get_guild(925729625580113951)
        channel = guild.get_channel(934036224413417472)

        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT votes FROM topgg WHERE userID = {userid}")
        result = cursor.fetchone()
        if result is None or result is False:
            cursor.execute(f"INSERT INTO topgg(userID, votes) VALUES(%s, %s)", (userid, 1))
            times = 1
        else:
            cursor.execute(f"UPDATE topgg SET votes = (%s) WHERE userID = (%s)", (int(result[0]) + 1, userid))
            times = int(result[0]) + 1
        mydb.commit()
        mydb.close()

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

        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT rucksack, bank, job, stunden FROM economy WHERE userID = {user.id}")
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO economy(rucksack, bank, job, stunden, userID) VALUES(%s, %s, %s, %s, %s)",("0", "0", "Kein Job", "0", user.id))
            mydb.commit()
            bal = 0
        else:
            bal = int(result[0])
        new = bal + 300
        cursor.execute("UPDATE economy SET rucksack = (%s) WHERE userID = (%s)", (new, user.id))

        time_to_convert = math.floor(datetime.datetime.utcnow().timestamp() + 50400)
        time_converted = datetime.datetime.fromtimestamp(int(time_to_convert))
        asyncio.create_task(vote_reminder(time_converted, bot, userid))
        cursor.execute("INSERT INTO vote(userid, endtime) VALUES(%s, %s)", (userid, time_to_convert))
        mydb.commit()
        mydb.close()

        dblpy = topgg.DBLClient(bot, dbl_token, autopost_interval=0)
        votedata = await dblpy.get_bot_info()
        votes = int(votedata["monthly_points"])
        guild = bot.get_guild(925729625580113951)
        votechannel = guild.get_channel(934036446271139860)
        await votechannel.edit(name=f"Votes im April: {votes}")
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
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )

            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT votes FROM topgg WHERE userID = {userid}")
            result = cursor.fetchone()
            if result is None or result is False:
                cursor.execute(f"INSERT INTO topgg(userID, votes) VALUES(%s, %s)", (userid, 1))
                times = 1
            else:
                cursor.execute(f"UPDATE topgg SET votes = (%s) WHERE userID = (%s)", (int(result[0]) + 1, userid))
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
        mydb.commit()
        mydb.close()

    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot is True:
            return
        try:
            if msg.mentions == "[]":
                return await bot.process_commands(msg)
            if msg.mentions[0] == bot.user:
                if msg.reference:
                    return
                prefix = get_prefix(bot, msg)
                await msg.channel.send(f"*Habe ich hier etwa meinen Namen gehört?*\n**Mein Prefix für diesen Server ist `{prefix}`**")
                return await bot.process_commands(msg)
            else:
                await bot.process_commands(msg)
        except:
            await bot.process_commands(msg)
    async def setup_hook(self):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        gel = 0
        fehl = 0
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS active_giveaways(guildID TEXT, endtime TEXT, gwID TEXT, prize TEXT, channelID TEXT, winners TEXT, roleID TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS old_giveaways(guildID TEXT, gwID TEXT, prize TEXT, channelID TEXT, winners TEXT, roleID TEXT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS levelsystem(user_xp INT, user_level INT, client_id TEXT, guild_id TEXT, enabled INT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS levelroles(guild_id TEXT, roleid TEXT, level INT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS tempchannels(guild_id TEXT, channel_id TEXT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS joinroles(guild_id TEXT, role_id TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS botroles(guild_id TEXT, role_id TEXT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute('CREATE TABLE IF NOT EXISTS reactionroles(guild_id TEXT, emoji TEXT, msg_id TEXT, role_id TEXT)')
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS welcome(msg TEXT, guildID TEXT, channelID TEXT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS leavemsg(msg TEXT, guildID TEXT, channelID TEXT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute('CREATE TABLE IF NOT EXISTS prefixes(guild_id TEXT, prefix TEXT)')
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS topgg(userID TEXT, votes TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS vote(endtime TEXT, userid TEXT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS messagelog(guildid TEXT, channelid TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS modlog(guildid TEXT, channelid TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS ticketlog(guildid TEXT, channelid TEXT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS panels(guildID TEXT, msgID TEXT, role TEXT, categoryID TEXT, archivID TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS tickets(guildID TEXT, channelID TEXT, userID TEXT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS warns(guildID TEXT, userID TEXT, grund TEXT, warnID TEXT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS blacklist(guildID TEXT, word TEXT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS economy(userID TEXT, rucksack INT, bank INT, stunden INT, job TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS economy_items(userID TEXT, titel TEXT, beschreibung TEXT, preis TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS economy_shop(guildID TEXT, titel TEXT, beschreibung TEXT, preis TEXT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS globalchat(guildID TEXT, channelID TEXT)")
            gel += 1
        except:
            fehl += 1
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS counting(guildID TEXT, channelID TEXT, zahl INT)")
            gel += 1
        except:
            fehl += 1
        try:
            topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("/dblwebhook", "Vulpo123321")
            await topgg_webhook.run(25002)
            print("✅ Verbunden mit der topgg api")
        except:
            print("❌ Verbindung zur topgg api fehlgeschlagen")
        try:
            if self.giveaways is True:
                return
            
            self.giveaways = True
            cursor.execute("SELECT gwID, endtime FROM active_giveaways")
            result = cursor.fetchall()
            a = 0
            for i in result:
                time_to_convert = int(i[1])
                time_converted = datetime.datetime.fromtimestamp(int(time_to_convert))
                a += 1
                asyncio.create_task(giveaway_end(time_converted, bot, i[0]))
            print(f"✅ Asyncio tasks für Giveaways bereit({a})")
        except Exception as e:
            print(f"❌ Asyncio tasks für Giveaways nicht bereit\n\n{e}")
        try:
            if self.votes is True:
                return

            self.votes = True
            cursor.execute("SELECT userid, endtime FROM vote")
            result = cursor.fetchall()
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
            geladen = 0
            fehler = 0
            await bot.load_extension("jishaku")
            for extension in self.initial_extensions:
                try:	
                    await bot.load_extension(extension)
                    geladen += 1
                except:
                    fehler += 1
                    print(f'{extension} konnte nicht geladen werden', file=sys.stderr)
                    traceback.print_exc()		
                    print('\n\n---------------------------------------------\n\n')
            print(f"✅ {geladen}/{geladen + fehler} Cogs geladen")
        except Exception as e:
            print(f"❌ Es gab einen Fehler beim Laden der Cogs\n{e}")
        print(f"✅ {gel}/{gel + fehl} Datenbanksysteme für Funktionen bereit")
        bot.add_view(view=DropdownView())
        ##########                   ##########
        print("   ___        _ _             ")
        print("  / _ \ _ __ | (_)_ __   ___  ")
        print(" | | | | '_ \| | | '_ \ / _ \ ")
        print(" | |_| | | | | | | | | |  __/ ")
        print("  \___/|_| |_|_|_|_| |_|\___| ")
		##########                   ##########
        mydb.commit()
        mydb.close()
        
    async def on_ready(self):
        try:
            await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.listening, name="ping 4 prefix"))
            print("✅ Status bereit")
        except:
            print("❌ Status nicht bereit")

bot = Vulpo()

@bot.command()
@commands.guild_only()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix=None):
    """Lege einen Serverprefix für den Bot Vulpo fest!"""
    if prefix == None:
        return await ctx.send(f"❌ Bitte gib einen Prefix an. Versuch es beim nächsten Mal so: `{ctx.prefix}prefix <neuer Prefix>`")
    mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
    cursor = mydb.cursor(buffered=True)
    cursor.execute(f"SELECT prefix FROM prefixes WHERE guild_id = {ctx.guild.id}")
    result = cursor.fetchone()
    if result == None:
        cursor.execute("INSERT INTO prefixes (guild_id, prefix) VALUES (%s , %s)", (ctx.guild.id, prefix))

    if result is not None:
        cursor.execute("UPDATE prefixes SET prefix = (%s) WHERE guild_id = (%s)", (prefix, ctx.guild.id))

    await ctx.send(f"**<:vulpo:939503518241411112> Der neue Serverprefix ist {prefix}**")
    mydb.commit()
    mydb.close()

@bot.command()
@commands.guild_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx, command: str=None): 
    """Liste von allen Commands oder Infos zu einem bestimmten Command."""
    if command == None:
        view = DropdownView()
        embed = discord.Embed(colour=discord.Colour.orange(), description=f"Wähle unten eine Kategorie aus, um alle Commands der Kategorie einzusehen.")
        embed.set_author(name="Command Menü", icon_url="https://cdn.discordapp.com/icons/925729625580113951/63a2e510fb885f12da3173da3413864c.png?size=1024")
        embed.set_image(url="https://cdn.discordapp.com/attachments/925736875728203786/938812140314296400/vulpo.gif")
        embed.add_field(name="⛓ Links", value="**[Support server](https://discord.gg/49jD3VXksp) | [Invite](https://discord.com/api/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot) | [Vote](https://top.gg/bot/925799559576322078/vote)**", inline=False)
        await ctx.send(embed=embed, view=view)
    if command != None:
        try:
            cmd = bot.get_command(command)
            embed = discord.Embed(colour=discord.Colour.blue(), description=f"**{ctx.prefix}{cmd.name} {cmd.usage if cmd.usage else ' '}**\n{cmd.help if cmd.help else 'Keine Beschreibung.'}")
            embed.set_author(name=f"Command Menü", icon_url="https://cdn.discordapp.com/icons/925729625580113951/63a2e510fb885f12da3173da3413864c.png?size=1024")
            await ctx.send(embed=embed)
            return
        except:
            embed = discord.Embed(colour=discord.Colour.orange(), description=f"Command **{command}** wurde nicht gefunden. Benutze **{ctx.prefix}help** um all meine Commands zu sehen.")
            embed.set_author(name=f"Command Menü", icon_url="https://cdn.discordapp.com/icons/925729625580113951/63a2e510fb885f12da3173da3413864c.png?size=1024")
            await ctx.send(embed=embed)
        return

bot.run("OTI1Nzk5NTU5NTc2MzIyMDc4.YcyYBw.ieu6ueJ_zkp8w8PQBzJRyi5kVgY")