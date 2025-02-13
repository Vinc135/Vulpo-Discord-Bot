import datetime
import typing
import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import getcolour, haspremium_forserver, addwarn, convert
from utils.MongoDB import getMongoDataBase

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(5, 2.5, commands.BucketType.user)

    automod = app_commands.Group(name='automod', description='Nehme Einstellungen am Automod vor.', guild_only=True)

    @automod.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def addaction(self, interaction: discord.Interaction, warnanzahl: typing.Literal[1,2,3,4,5,6,7,8,9,10], aktion: typing.Literal["Kick","Ban","Timeout (Bitte Zeit angeben)"], time: str = None):
        """Füge eine Aktion für die automatische Moderation hinzu."""
        await interaction.response.defer()
        
        guild_id = str(interaction.guild.id)
        db = getMongoDataBase()
        
        existing_actions = await db['automod'].find({"guildID": guild_id}).to_list(length=None)
        
        existing_action = await db['automod'].find_one({"guildID": guild_id, "warnanzahl": warnanzahl})
        if existing_action is not None:
            await interaction.followup.send("**<:v_x:1264270921452224562> Du kannst für eine Warnanzahl nur eine Aktion hinzufügen. Bitte wähle eine andere Warnanzahl oder entferne diese Aktion mit `/automod removeaction <warnanzahl>`.**", ephemeral=True)
            return

        if aktion == "Timeout (Bitte Zeit angeben)":
            if time == None or time == "":
                return await interaction.followup.send("**<:v_x:1264270921452224562> Bitte gib eine Zeit an, wie lange der Timeout dauern soll.**", ephemeral=True)
                
            seconds = convert(time)
            
            if seconds == None or seconds == 0:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Bitte gib eine gültige Zeit an.**", ephemeral=True)
            
            await db['automod'].insert_one({"guildID": guild_id, "warnanzahl": warnanzahl, "aktion": f"Timeout ({time})", "time": seconds})
            
            return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Eintrag erstellt. Jeder User mit einer Anzahl an Verwarnungen von {warnanzahl} wird erhält bei der nächsten Verwarnung einen Timeout von {time}.**")
            

        await db['automod'].insert_one({"guildID": guild_id, "warnanzahl": warnanzahl, "aktion": aktion})
        
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Eintrag erstellt. Jeder User mit einer Anzahl an Verwarnungen von {warnanzahl} wird erhält bei der nächsten Verwarnung einen {aktion}.**")

    @automod.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)     
    async def removeaction(self, interaction: discord.Interaction, warnanzahl: typing.Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
        """Entferne eine Aktion von der automatischen Moderation."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        guild_id = str(interaction.guild.id)
        
        existing_action = await db['automod'].find_one({"guildID": guild_id, "warnanzahl": warnanzahl})
        if existing_action is None:
            await interaction.followup.send("**<:v_x:1264270921452224562> Dieser Eintrag existiert nicht. Bitte wähle eine andere Warnanzahl oder füge eine Aktion mit `/automod addaction <warnanzahl> <aktion>` hinzu**", ephemeral=True)
            return

        await db['automod'].delete_one({"guildID": guild_id, "warnanzahl": warnanzahl})
        
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Eintrag gelöscht.**")

    @automod.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def liste(self, interaction: discord.Interaction):
        """Erhalte eine Liste von den Automod Aktionen."""
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        guild_id = str(interaction.guild.id)
        
        result = await db['automod'].find({"guildID": guild_id}).to_list(length=None)
        
        if len(result) == 0:
            await interaction.followup.send("**<:v_x:1264270921452224562> Hier wurden keine Aktionen gefunden. Füge eine Aktion mit `/automod addaction <warnanzahl> <aktion>` hinzu**", ephemeral=True)
            return
        
        embed = discord.Embed(title="Alle Aktionen vom Automod", description="Hier nähere Infos:", color=await getcolour(self, interaction.user))
        
        for i in result:
            embed.add_field(name=i["aktion"], value=f"Verwarnungen benötigt: {i['warnanzahl']}")
            
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, user: discord.User, grund: str):
        """Warnt einen Benutzer."""
        await interaction.response.defer()
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
        
        
        try:
            await user.send(embed=dm)
        except:
            pass
        await interaction.followup.send(embed=embed)
        
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def unwarn(self, interaction: discord.Interaction, user: discord.User, warnid: int):
        """Entwarnt eine Warnung."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = await db['warns'].find_one({"guildID": str(interaction.guild.id), "userID": str(user.id), "warnID": warnid})
        if result is None:
            await interaction.followup.send(f"**<:v_x:1264270921452224562> Die Verwarnung mit der ID {warnid} von {user} wurde nicht gefunden.**")
            return
        await db['warns'].delete_one({"guildID": str(interaction.guild.id), "userID": str(user.id), "warnID": warnid})
        
        embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                description=f"Die Verwarnung mit der ID {warnid} von {user} (**{user.id}**) wurde entfernt.")
        
        embed.add_field(name=f"🎛️ Server:", value=f"{interaction.guild.name}", inline=False)
        embed.add_field(name=f"👮 Moderator:", value=f"{interaction.user} (**{interaction.user.id}**)", inline=False)
        embed.add_field(name=f"📄 Verwarnung:", value=f"{result['grund']}", inline=False)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.followup.send(embed=embed)
        
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def listwarns(self, interaction: discord.Interaction, user: discord.User):
        """Bekomme eine Liste an Warns eines bestimmten Benutzers."""
        
        await interaction.response.defer()
        
        result = await getMongoDataBase()['warns'].find({"guildID": str(interaction.guild.id), "userID": str(user.id)}).to_list(length=None)
        
        if result is None:
            await interaction.followup.send(f"Der User {user} hat keine Verwarnungen hier.")
            return
        
        warnembed = discord.Embed(colour=await getcolour(self, interaction.user), description=f"Alle Verwarnungen von {user} (**{user.id}**).")
        warnembed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        a = 0
        for warn in result:
            a += 1
            warnembed.add_field(name=f"Verwarnung {warn['warnID']}", value=f"{warn['grund']}", inline=False)
        if a != 0:
            await interaction.followup.send(embed=warnembed)
        if a == 0:
            await interaction.followup.send(f"**<:v_x:1264270921452224562> Der User {user} hat keine Verwarnungen hier.**", ephemeral=True) 
    
    blacklist = app_commands.Group(name='blacklist', description='Nehme Einstellungen am Blacklist-System vor.', guild_only=True)

    @blacklist.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def show(self, interaction: discord.Interaction):
        """Zeigt alle Wörter auf der Blacklist an."""
        
        await interaction.response.defer()
        
        result = await getMongoDataBase()['blacklist'].find({"guildID": str(interaction.guild.id)}).to_list(length=None)
        if result is None:
            await interaction.followup.send(f"Die Blacklist dieses Servers ist leer.\nWort der Blacklist hinzufügen: `/blacklist add <wort>\n`Wort von der Blacklist entfernen: `/blacklist remove <wort>`")
            return
        desc = ""
        for word in result:
            desc += f"{word[0]}\n"
        if desc == "":
            desc = f"Die Blacklist dieses Servers ist leer.\nWort der Blacklist hinzufügen: `/blacklist add <wort>\n`Wort von der Blacklist entfernen: `/blacklist remove <wort>`"
        embed = discord.Embed(title="Die Blacklist", description=desc + f"\nWort der Blacklist hinzufügen: `/blacklist add <wort>\n`Wort von der Blacklist entfernen: `/blacklist remove <wort>`", color=await getcolour(self, interaction.user))
        
        await interaction.followup.send(embed=embed)

    @blacklist.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def add(self, interaction: discord.Interaction, wort: str):
        """Füge ein Wort der Blacklist hinzu."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = await db['blacklist'].find_one({"guildID": str(interaction.guild.id), "word": wort})
        
        if result != None:
            await interaction.followup.send(f"**<:v_x:1264270921452224562> Das Wort `{wort}` existiert bereits in der Blacklist.**", ephemeral=True)
            return
        
        existing_words = await db['blacklist'].find({"guildID": str(interaction.guild.id)}).to_list(length=None)
        
        await db['blacklist'].insert_one({"guildID": str(interaction.guild.id), "word": wort})
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Das Wort `{wort}` ist nun auf der Blacklist.**")

    @blacklist.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def remove(self, interaction: discord.Interaction, wort: str=None):
        """Entferne ein Wort von der Blacklist."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = await db['blacklist'].find_one({"guildID": str(interaction.guild.id), "word": wort})
        if result is None or result == "()":
            await interaction.followup.send(f"**<:v_x:1264270921452224562> Das Wort `{wort}` existiert nicht in der Blacklist.**", ephemeral=True)
            return
        await db['blacklist'].delete_one({"guildID": str(interaction.guild.id), "word": wort})
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Das Wort `{wort}` ist nun nicht mehr auf der Blacklist.**")

    @automod.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def caps(self, interaction: discord.Interaction, modus: typing.Literal["Anschalten (Prozent Angabe erforderlich)", "Ausschalten"], prozent: typing.Literal[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]=None):
        """Füge einen Caps Filter hinzu."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        if modus == "Anschalten (Prozent Angabe erforderlich)":
            result = await db['caps'].find_one({"guildID": str(interaction.guild.id)})

            if result != None:
                await db['caps'].update_one({"guildID": str(interaction.guild.id)}, {"$set": {"prozent": prozent}})
                return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Jede Nachricht die mindestens {prozent} Caps beihnaltet, wird ab sofort gelöscht und der User verwarnt.**")
            if result == None:
                await db['caps'].insert_one({"guildID": str(interaction.guild.id), "prozent": prozent})
                return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Jede Nachricht die mindestens {prozent} Caps beihnaltet, wird ab sofort gelöscht und der User verwarnt.**")
        if modus == "Ausschalten":
            await db['caps'].delete_one({"guildID": str(interaction.guild.id)})
            return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Der Caps Filter wurde deaktiviert.**")
    
    @automod.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def spam(self, interaction: discord.Interaction, modus: typing.Literal["Anschalten (5 Nachrichten in 2,5 Sekunden gilt als Spam)", "Ausschalten"]):
        """Füge einen Spam Filter hinzu."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        if modus == "Anschalten (5 Nachrichten in 2,5 Sekunden gilt als Spam)":
            result = await db['spam'].find_one({"guildID": str(interaction.guild.id)})
            if result != None:
                await db['spam'].update_one({"guildID": str(interaction.guild.id)}, {"$set": {"status": True}})
                return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Jeder User, der mindestens 5 Nachrichten in 2,5 Sekunden sendet, wird verwarnt. Außerdem werden die Nachrichten gelöscht.**")
            if result == None:
                await db['spam'].insert_one({"guildID": str(interaction.guild.id), "status": True})
                return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Jeder User, der mindestens 5 Nachrichten in 2,5 Sekunden sendet, wird verwarnt. Außerdem werden die Nachrichten gelöscht.**")
        if modus == "Ausschalten":
            await db['spam'].delete_one({"guildID": str(interaction.guild.id)})
            return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Der Spam Filter wurde deaktiviert.**")
            
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
                
                db = getMongoDataBase()
                
                try:
                    bucket = self._cd.get_bucket(msg)
                    retry_after = bucket.update_rate_limit()
                    if retry_after:
                        result = await db['spam'].find_one({"guildID": msg.guild.id})
                        if result:
                            if result["enabled"] == True:
                                time_end = discord.utils.utcnow()
                                dt = time_end + datetime.timedelta(hours=2)
                                await msg.author.timeout(dt ,reason="Hat die Spam Grenze von 5 Nachrichten innerhalb 2,5 Sekunden überschritten.")
                                await msg.channel.send(f"{msg.author.mention} Bitte unterlasse Nachrichten-Spam. Du wurdest verwarnt!")
                                await addwarn(self, msg.author, msg, f"Hat die Spam Grenze von 5 Nachrichten innerhalb 2,5 Sekunden überschritten.")

                                result = await db['modlog'].find_one({"guildID": msg.guild.id})
                                if result != None:
                                    chan = await msg.guild.fetch_channel(int(result["channelID"]))
                                    if chan:
                                        embed = discord.Embed(colour=await getcolour(self, msg.author),
                                                        description=f"Der Benutzer {msg.author} (**{msg.author.id}**) wurde verwarnt.")
                                        
                                        embed.add_field(name=f"🎛️ Server:", value=f"{msg.guild.name}", inline=False)
                                        embed.add_field(name=f"👮 Moderator:", value=f"Vulpo#3749", inline=False)
                                        embed.add_field(name=f"📄 Grund:", value=f"Hat die Spam Grenze von 5 Nachrichten innerhalb 2,5 Sekunden überschritten.", inline=False)
                                        embed.set_author(name=msg.author, icon_url=msg.author.avatar)
                                        await chan.send(embed=embed)
                except:
                    pass
                                
                try:
                    prozent = await db['caps'].find_one({"guildID": msg.guild.id})
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

                                result = await db['modlog'].find_one({"guildID": msg.guild.id})
                                if result != None:
                                    chan = await msg.guild.fetch_channel(int(result["channelID"]))
                                    if chan:
                                        embed = discord.Embed(colour=await getcolour(self, msg.author),
                                                        description=f"Der Benutzer {msg.author} (**{msg.author.id}**) wurde verwarnt.")
                                        
                                        embed.add_field(name=f"🎛️ Server:", value=f"{msg.guild.name}", inline=False)
                                        embed.add_field(name=f"👮 Moderator:", value=f"Vulpo#3749", inline=False)
                                        embed.add_field(name=f"📄 Grund:", value=f"Hat die Caps Sperre von {prozent[0]}% überschritten. Die Nachricht beinhaltete {procent}% Caps.", inline=False)
                                        embed.set_author(name=msg.author, icon_url=msg.author.avatar)
                                        await chan.send(embed=embed)
                except:
                    pass

                try:
                    result = await db["blacklist"].find({"guildID": msg.guild.id}).to_list(length=None)
                    if result:
                        for word in result:
                            if str(word[0].lower()) in str(msg.content.lower()):
                                await msg.delete()
                                await addwarn(self, msg.author, msg, f"Hat ein verbotenes Wort gesendet: ||{word[0]}||")

                                result = await db['modlog'].find_one({"guildID": msg.guild.id})
                                if result != None:
                                    chan = await msg.guild.fetch_channel(int(result["channelID"]))
                                    if chan != None:
                                        embed = discord.Embed(colour=await getcolour(self, msg.author),
                                                        description=f"Der Benutzer {msg.author} (**{msg.author.id}**) wurde verwarnt.")
                                        
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