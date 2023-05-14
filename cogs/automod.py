import datetime
import typing
import discord
from discord.ext import commands
from discord import app_commands
from info import getcolour, haspremium_forserver, addwarn

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(5, 2.5, commands.BucketType.user)

    automod = app_commands.Group(name='automod', description='Nehme Einstellungen am Automod vor.', guild_only=True)
    

    @automod.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def addaction(self, interaction: discord.Interaction, warnanzahl: typing.Literal[1,2,3,4,5,6,7,8,9,10], aktion: typing.Literal["Kick","Ban","Timeout"]):
        """Füge eine Aktion für die automatische Moderation hinzu."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT aktion FROM automod WHERE guildID = (%s)", (interaction.guild.id))
                a = await cursor.fetchall()
                premium_status = await haspremium_forserver(self, interaction.guild)
                if premium_status == False:
                    if len(a) >= 3:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du kannst keine weiteren Aktionen erstellen, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")

                await cursor.execute("SELECT aktion FROM automod WHERE guildID = (%s) AND warnanzahl = (%s)", (interaction.guild.id, warnanzahl))
                result = await cursor.fetchone()
                if result != None:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du kannst für eine Warnanzahl nur eine Aktion hinzufügen. Bitte wähle eine andere Warnanzahl oder entferne diese Aktion mit `/automod removeaction <warnanzahl>`.**", ephemeral=True)
                    return
                await cursor.execute("INSERT INTO automod(guildID, warnanzahl, aktion) VALUES(%s,%s,%s)", (interaction.guild.id, warnanzahl, aktion))
                
                await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Eintrag erstellt. Jeder User mit einer Anzahl an Verwarnungen von {warnanzahl} wird erhält bei der nächsten Verwarnung einen {aktion}.**")

    @automod.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def removeaction(self, interaction: discord.Interaction, warnanzahl: typing.Literal[1,2,3,4,5,6,7,8,9,10]):
        """Entferne eine Aktion von der automatischen Moderation."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT aktion FROM automod WHERE guildID = (%s) AND warnanzahl = (%s)", (interaction.guild.id, warnanzahl))
                result = await cursor.fetchone()
                if result == None:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Dieser Eintrag existiert nicht. Bitte wähle eine andere Warnanzahl oder füge eine Aktion mit `/automod addaction <warnanzahl> <aktion>` hinzu**", ephemeral=True)
                    return
                await cursor.execute("DELETE FROM automod WHERE guildID = (%s) AND warnanzahl = (%s)", (interaction.guild.id, warnanzahl))
                
                await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Eintrag gelöscht.**")

    @automod.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def liste(self, interaction: discord.Interaction):
        """Erhalte eine Liste von den Automod Aktionen."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT aktion, warnanzahl FROM automod WHERE guildID = (%s)", (interaction.guild.id))
                result = await cursor.fetchall()
                if result == None:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Hier wurden keine Aktionen gefunden. Füge eine Aktion mit `/automod addaction <warnanzahl> <aktion>` hinzu**", ephemeral=True)
                    return
                embed = discord.Embed(title="Alle Aktionen vom Automod", description="Hier nähere Infos:", color=await getcolour(self, interaction.user))
                for i in result:
                    embed.add_field(name=i[0], value=f"Verwarnungen benötigt: {i[1]}")
                embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, user: discord.User, grund: str):
        """Warnt einen Benutzer."""
        await addwarn(self, user, interaction, grund)
        embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                description=f"Der Benutzer {user} (**{user.id}**) wurde verwarnt.")
        embed.add_field(name=f"🎛 Server:", value=f"{interaction.guild.name}", inline=False)
        embed.add_field(name=f"👮 Moderator:", value=f"{interaction.user} (**{interaction.user.id}**)", inline=False)
        embed.add_field(name=f"📄 Grund:", value=f"{grund}", inline=False)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)

        dm = discord.Embed(colour=await getcolour(self, interaction.user),
                            description=f"Hey {user.mention}! \nDu wurdest auf dem Server **{interaction.guild.name}** verwarnt! Genauere Informationen hier:")
        dm.add_field(name=f"🎛 Server:", value=f"{interaction.guild.name}", inline=False)
        dm.add_field(name=f"👮 Moderator:", value=f"{interaction.user.mention}", inline=False)
        dm.add_field(name=f"📄 Grund:", value=f"{grund}", inline=False)
        dm.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        dm.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        try:
            await user.send(embed=dm)
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message(embed=embed)
        
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def unwarn(self, interaction: discord.Interaction, user: discord.User, warnid: str):
        """Entwarnt eine Warnung."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT grund FROM warns WHERE guildID = (%s) AND userID = (%s) AND warnID = (%s)", (interaction.guild.id, user.id, warnid))
                result = await cursor.fetchone()
                if result is None:
                    await interaction.response.send_message(f"**<:v_kreuz:1049388811353858069> Die Verwarnung mit der ID {warnid} von {user} wurde nicht gefunden.**")
                    return
                await cursor.execute("DELETE FROM warns WHERE userID = (%s) AND guildID = (%s) AND warnID = (%s)", (user.id, interaction.guild.id, warnid))
        
        embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                description=f"Die Verwarnung mit der ID {warnid} von {user} (**{user.id}**) wurde entfernt.")
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        embed.add_field(name=f"🎛️ Server:", value=f"{interaction.guild.name}", inline=False)
        embed.add_field(name=f"👮 Moderator:", value=f"{interaction.user} (**{interaction.user.id}**)", inline=False)
        embed.add_field(name=f"📄 Verwarnung:", value=f"{result[0]}", inline=False)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def listwarns(self, interaction: discord.Interaction, user: discord.User):
        """Bekomme eine Liste an Warns eines bestimmten Benutzers."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT grund, warnID FROM warns WHERE guildID = (%s) AND userID = (%s)", (interaction.guild.id, user.id))
                result = await cursor.fetchall()
        if result is None:
            await interaction.response.send_message(f"Der User {user} hat keine Verwarnungen hier.")
            return
        warnembed = discord.Embed(colour=await getcolour(self, interaction.user), description=f"Alle Verwarnungen von {user} (**{user.id}**).")
        warnembed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        warnembed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        a = 0
        for warn in result:
            a += 1
            warnembed.add_field(name=f"Verwarnung {warn[1]}", value=f"{warn[0]}", inline=False)
        if a != 0:
            await interaction.response.send_message(embed=warnembed)
        if a == 0:
            await interaction.response.send_message(f"**<:v_kreuz:1049388811353858069> Der User {user} hat keine Verwarnungen hier.**", ephemeral=True) 
    
    blacklist = app_commands.Group(name='blacklist', description='Nehme Einstellungen am Blacklist-System vor.', guild_only=True)

    @blacklist.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def show(self, interaction: discord.Interaction):
        """Zeigt alle Wörter auf der Blacklist an."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT word FROM blacklist WHERE guildID = {interaction.guild.id}")
                result = await cursor.fetchall()
                if result is None:
                    await interaction.response.send_message(f"Die Blacklist dieses Servers ist leer.\nWort der Blacklist hinzufügen: `/blacklist add <wort>\n`Wort von der Blacklist entfernen: `/blacklist remove <wort>`")
                    return
                desc = ""
                for word in result:
                    desc += f"{word[0]}\n"
                if desc == "":
                    desc = f"Die Blacklist dieses Servers ist leer.\nWort der Blacklist hinzufügen: `/blacklist add <wort>\n`Wort von der Blacklist entfernen: `/blacklist remove <wort>`"
                embed = discord.Embed(title="Die Blacklist", description=desc + f"\nWort der Blacklist hinzufügen: `/blacklist add <wort>\n`Wort von der Blacklist entfernen: `/blacklist remove <wort>`", color=await getcolour(self, interaction.user))
                embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                await interaction.response.send_message(embed=embed)

    @blacklist.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def add(self, interaction: discord.Interaction, wort: str):
        """Füge ein Wort der Blacklist hinzu."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT word FROM blacklist WHERE guildID = (%s) AND word = (%s)", (interaction.guild.id, wort))
                result = await cursor.fetchone()
                if result != None:
                    await interaction.response.send_message(f"**<:v_kreuz:1049388811353858069> Das Wort `{wort}` existiert bereits in der Blacklist.**", ephemeral=True)
                    return
                
                await cursor.execute("SELECT word FROM blacklist WHERE guildID = (%s)", (interaction.guild.id))
                a = await cursor.fetchall()
                premium_status = await haspremium_forserver(self, interaction.guild)
                if premium_status == False:
                    if len(a) >= 15:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du kannst keine weiteren Wörter hinzufügen, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")

                
                await cursor.execute("INSERT INTO blacklist(guildID, word) VALUES(%s, %s)", (interaction.guild.id, wort))
                await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Das Wort `{wort}` ist nun auf der Blacklist.**")

    @blacklist.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def remove(self, interaction: discord.Interaction, wort: str=None):
        """Entferne ein Wort von der Blacklist."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT word FROM blacklist WHERE guildID = (%s) AND word = (%s)", (interaction.guild.id, wort))
                result = await cursor.fetchone()
                if result is None or result == "()":
                    await interaction.response.send_message(f"**<:v_kreuz:1049388811353858069> Das Wort `{wort}` existiert nicht in der Blacklist.**", ephemeral=True)
                    return
                await cursor.execute("DELETE FROM blacklist WHERE word = (%s) AND guildID = (%s)", (wort, interaction.guild.id))
                await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Das Wort `{wort}` ist nun nicht mehr auf der Blacklist.**")

    @automod.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def caps(self, interaction: discord.Interaction, modus: typing.Literal["Anschalten (Prozent Angabe erforderlich)", "Ausschalten"], prozent: typing.Literal[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]=None):
        """Füge einen Caps Filter hinzu."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if modus == "Anschalten (Prozent Angabe erforderlich)":
                    if prozent == None:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Eine Prozentangabe ist zum Aktivieren erforderlich.", ephemeral=True)
                    await cursor.execute("SELECT prozent FROM caps WHERE guildID = (%s)", (interaction.guild.id))
                    result = await cursor.fetchone()
                    if result != None:
                        await cursor.execute("UPDATE caps SET prozent = (%s) WHERE guildID = (%s)", (prozent, interaction.guild.id))
                        return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Jede Nachricht die mindestens {prozent} Caps beihnaltet, wird ab sofort gelöscht und der User verwarnt.**")
                    if result == None:
                        await cursor.execute("INSERT INTO caps(guildID, prozent) VALUES(%s, %s)", (interaction.guild.id, prozent))
                        return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Jede Nachricht die mindestens {prozent} Caps beihnaltet, wird ab sofort gelöscht und der User verwarnt.**")
                if modus == "Ausschalten":
                    await cursor.execute("DELETE FROM caps WHERE guildID = (%s)", (interaction.guild.id))
                    return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Der Caps Filter wurde deaktiviert.**")
    
    @automod.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def spam(self, interaction: discord.Interaction, modus: typing.Literal["Anschalten (5 Nachrichten in 2,5 Sekunden gilt als Spam)", "Ausschalten"]):
        """Füge einen Spam Filter hinzu."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if modus == "Anschalten (5 Nachrichten in 2,5 Sekunden gilt als Spam)":
                    await cursor.execute("SELECT status FROM spam WHERE guildID = (%s)", (interaction.guild.id))
                    result = await cursor.fetchone()
                    if result != None:
                        await cursor.execute("UPDATE spam SET status = (%s) WHERE guildID = (%s)", (1, interaction.guild.id))
                        return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Jeder User, der mindestens 5 Nachrichten in 2,5 Sekunden sendet, wird verwarnt. Außerdem werden die Nachrichten gelöscht.**")
                    if result == None:
                        await cursor.execute("INSERT INTO spam(guildID, status) VALUES(%s, %s)", (interaction.guild.id, 1))
                        return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Jeder User, der mindestens 5 Nachrichten in 2,5 Sekunden sendet, wird verwarnt. Außerdem werden die Nachrichten gelöscht.**")
                if modus == "Ausschalten":
                    await cursor.execute("DELETE FROM spam WHERE guildID = (%s)", (interaction.guild.id))
                    return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Der Spam Filter wurde deaktiviert.**")
            
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot:
            return
        try:
            if msg.author.guild_permissions.manage_messages:
                return
        except:
            pass
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    bucket = self._cd.get_bucket(msg)
                    retry_after = bucket.update_rate_limit()
                    if retry_after:
                        await cursor.execute("SELECT status FROM spam WHERE guildID = (%s)", (msg.guild.id))
                        result = await cursor.fetchone()
                        if result:
                            if result[0] == 1:
                                time_end = discord.utils.utcnow()
                                dt = time_end + datetime.timedelta(minutes=1, seconds=7200)
                                await msg.author.timeout(dt ,reason="Hat die Spam Grenze von 5 Nachrichten innerhalb 2,5 Sekunden überschritten.")
                                await msg.channel.send(f"{msg.author.mention} Bitte unterlasse Nachrichten-Spam. Du wurdest verwarnt!")
                                await addwarn(self, msg.author, msg, f"Hat die Spam Grenze von 5 Nachrichten innerhalb 2,5 Sekunden überschritten.")

                                await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {msg.guild.id}")
                                result = await cursor.fetchone()
                                if result != None:
                                    chan = msg.guild.get_channel(int(result[0]))
                                    if chan:
                                        embed = discord.Embed(colour=await getcolour(self, msg.author),
                                                        description=f"Der Benutzer {msg.author} (**{msg.author.id}**) wurde verwarnt.")
                                        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                                        embed.add_field(name=f"🎛️ Server:", value=f"{msg.guild.name}", inline=False)
                                        embed.add_field(name=f"👮 Moderator:", value=f"Vulpo#3749", inline=False)
                                        embed.add_field(name=f"📄 Grund:", value=f"Hat die Spam Grenze von 5 Nachrichten innerhalb 2,5 Sekunden überschritten.", inline=False)
                                        embed.set_author(name=msg.author, icon_url=msg.author.avatar)
                                        await chan.send(embed=embed)
                except:
                    pass
                                
                try:
                    await cursor.execute(f"SELECT prozent FROM caps WHERE guildID = {msg.guild.id}")
                    prozent = await cursor.fetchone()
                    if prozent:
                        if len(msg.content) > 5:
                            upper = 0
                            for character in msg.content:
                                if character.isupper():
                                    pass
                                else:
                                    upper += 1
                            multiplication = 100 / len(msg.content)
                            procent = round((len(msg.content) - upper) * multiplication)
                            if int(procent) >= int(prozent[0]):
                                await msg.delete()
                                await msg.channel.send(f"{msg.author.mention} Bitte unterlasse diese große Anzahl an Caps. Du wurdest verwarnt!")
                                await addwarn(self, msg.author, msg, f"Hat die Caps Sperre von {prozent[0]}% überschritten. Die Nachricht beinhaltete {procent}% Caps.")

                                await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {msg.guild.id}")
                                result = await cursor.fetchone()
                                if result != None:
                                    chan = msg.guild.get_channel(int(result[0]))
                                    if chan:
                                        embed = discord.Embed(colour=await getcolour(self, msg.author),
                                                        description=f"Der Benutzer {msg.author} (**{msg.author.id}**) wurde verwarnt.")
                                        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                                        embed.add_field(name=f"🎛️ Server:", value=f"{msg.guild.name}", inline=False)
                                        embed.add_field(name=f"👮 Moderator:", value=f"Vulpo#3749", inline=False)
                                        embed.add_field(name=f"📄 Grund:", value=f"Hat die Caps Sperre von {prozent[0]}% überschritten. Die Nachricht beinhaltete {procent}% Caps.", inline=False)
                                        embed.set_author(name=msg.author, icon_url=msg.author.avatar)
                                        await chan.send(embed=embed)
                except:
                    pass

                try:
                    await cursor.execute(f"SELECT word FROM blacklist WHERE guildID = {msg.guild.id}")
                    result = await cursor.fetchall()
                    if result:
                        for word in result:
                            if str(word[0].lower()) in str(msg.content.lower()):
                                await msg.delete()
                                await addwarn(self, msg.author, msg, f"Hat ein verbotenes Wort gesendet: ||{word[0]}||")

                                await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {msg.guild.id}")
                                result = await cursor.fetchone()
                                if result != None:
                                    chan = msg.guild.get_channel(int(result[0]))
                                    if chan != None:
                                        embed = discord.Embed(colour=await getcolour(self, msg.author),
                                                        description=f"Der Benutzer {msg.author} (**{msg.author.id}**) wurde verwarnt.")
                                        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
                                        embed.add_field(name=f"🎛️ Server:", value=f"{msg.guild.name}", inline=False)
                                        embed.add_field(name=f"👮 Moderator:", value=f"Vulpo#3749", inline=False)
                                        embed.add_field(name=f"📄 Grund:", value=f"Hat ein verbotenes Wort gesendet. ||{msg.content}||", inline=False)
                                        embed.set_author(name=msg.author, icon_url=msg.author.avatar)
                                        await chan.send(embed=embed)
                                await msg.channel.send(f"{msg.author.mention} Bitte unterlasse diesen Ausdruck. Du wurdest verwarnt!")
                except:
                    pass
                    
async def setup(bot):
    await bot.add_cog(Automod(bot))