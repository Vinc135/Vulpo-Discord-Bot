import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import typing
from utils.utils import getcolour, haspremium_forserver
from utils.MongoDB import getMongoDataBase

class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #reportlog
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def reportlog(self, interaction: discord.Interaction, argument: typing.Literal["Einrichten (Kanal muss mit angegeben werden)","Anzeigen","Ausschalten"], kanal: discord.TextChannel=None):
                """Lege einen Kanal fest für gemeldete Nachrichten von Usern."""
                
                await interaction.response.defer()
                
                db = getMongoDataBase()
                
                if argument == "Ausschalten":
                    result = db["reportlog"].find_one({"guildID": interaction.guild.id})
                    if result == None:
                        return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Auf diesem Server ist kein Reportlog eingerichtet.**", ephemeral=True)
                    await db["reportlog"].delete_one({"guildID": interaction.guild.id})
                    return await interaction.followup.send("**<:v_haken:1119579684057907251> Der Reportlog wurde ausgeschaltet.**")
                if argument == "Einrichten (Kanal muss mit angegeben werden)":
                    if kanal == None:
                        return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Beim Einrichten ist auch eine Kanal-Angabe erforderlich.**", ephemeral=True)

                    result = db["reportlog"].find_one({"guildID": interaction.guild.id})

                    if result:
                        await db["reportlog"].update_one({"guildID": interaction.guild.id}, {"$set": {"channelID": kanal.id}})
                    else:
                        await db["reportlog"].insert_one({"guildID": interaction.guild.id, "channelID": kanal.id})
                    await interaction.followup.send(f"**<:v_haken:1119579684057907251> Der Reportlog ist nun aktiv in {kanal.mention}.**")
                if argument == "Anzeigen":
                    result = db["reportlog"].find_one({"guildID": interaction.guild.id})
                    try:
                        channel = await interaction.guild.fetch_channel(int(result["channelID"]))
                    except:
                        return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Der Kanal des Reportlogs existiert nicht mehr. Bitte deaktiviere den Reportlog und richte ihn erneut ein.**", ephemeral=True)

                    embed = discord.Embed(title="Reportlog", description=f"Der aktuelle Reportlog ist aktiv in {channel.mention}", color=await getcolour(self, interaction.user))
                    
                    await interaction.followup.send(embed=embed)
    #messagelog

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def messagelog(self, interaction: discord.Interaction, modus: typing.Literal["An","Aus"], kanal: discord.TextChannel):
        """Setze den Nachrichtenlog."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        if modus == "An":
            result = await db["messagelog"].find_one({"guildID": interaction.guild.id})
            if result is None:
                await db["messagelog"].insert_one({"guildID": interaction.guild.id, "channelID": kanal.id})                

                embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Nachrichtenlog", description=f"Der Nachrichtenlog ist nun aktiv in {kanal.mention}.")
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)

                await interaction.followup.send(embed=embed)
                return
            if result != None:
                await db["messagelog"].update_one({"guildID": interaction.guild.id}, {"$set": {"channelID": kanal.id}})
                        
                embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Nachrichtenlog", description=f"Der Nachrichtenlog ist nun aktiv in {kanal.mention}.")
                        
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                await interaction.followup.send(embed=embed)
                return
            
        if modus == "Aus":
            result = await db["messagelog"].find_one({"guildID": interaction.guild.id})
            if result is None:
                embed = discord.Embed(colour=discord.Colour.orange(), title="Messagelog", description=f"Der Nachrichtenlog ist nicht aktiviert auf diesem Server.")
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        
                await interaction.followup.send(embed=embed)
                return
            if result != None:
                await db["messagelog"].delete_one({"guildID": interaction.guild.id})                        

                embed = discord.Embed(colour=discord.Colour.orange(), title="Messagelog deaktiviert", description=f"Der Nachrichtenlog ist nun deaktiviert auf diesem Server.")
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        
                await interaction.followup.send(embed=embed)
                return
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild == None:
            return
        
        try:
            result = await getMongoDataBase()["messagelog"].find_one({"guildID": message.guild.id})
            if result is None:
                return
            if result != None:
                channel = await message.guild.fetch_channel(int(result["channelID"]))
                if channel is None:
                    return
                else:
                    embed = discord.Embed(title="Eine Nachricht wurde gelöscht", color=discord.Color.orange(), timestamp=datetime.now())
                    embed.add_field(name="<:v_user:1119585450923929672> Autor", value=message.author)
                    embed.add_field(name="<:v_auge:1119578772207849472> Kanal", value=message.channel.mention)
                    embed.add_field(name="<:v_chat:1119577968457568327> Nachricht", value=message.content)
                    
                    await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        
        db = getMongoDataBase()
        
        result = await db["messagelog"].find_one({"guildID": messages[0].guild.id})
        if result is None:
            return
        if result != None:
            channel = await messages.guild.fetch_channel(int(result["channelID"]))
            if channel is None:
                return
            else:
                embed = discord.Embed(description=f"**{len(messages)} Nachrichten in {messages.channel.mention} gelöscht**", color=discord.Color.orange(), timestamp=datetime.now())
                
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
                if after.guild == None:
                    return
                
                db = getMongoDataBase()
                
                try:
                    result = await db["messagelog"].find_one({"guildID": after.guild.id})
                    if result is None:
                        return
                    if result != None:
                        channel = await after.guild.fetch_channel(int(result["channelID"]))
                        if channel is None:
                            return
                        else:
                            if before.pinned == False and after.pinned == True:
                                embed = discord.Embed(description=f"**Die folgende Nachricht({after.id}) wurde in {after.channel.mention} angeheftet:**\n{after.content}", color=discord.Color.gold(), timestamp=datetime.now())
                                embed.set_author(name=after.author, icon_url=after.author.avatar)
                                embed.set_footer(text=f"Autor-ID: {after.author.id}")

                                await channel.send(embed=embed)
                                return
                                
                            if before.pinned == True and after.pinned == False:
                                embed = discord.Embed(description=f"**Die folgende Nachricht({after.id}) wurde in {after.channel.mention} losgelöst:**\n{after.content}", color=discord.Color.gold(), timestamp=datetime.now())
                                embed.set_author(name=after.author, icon_url=after.author.avatar)
                                embed.set_footer(text=f"Autor-ID: {after.author.id}")

                                await channel.send(embed=embed)
                                
                            if before.content != after.content:
                                if before.pinned == True and after.pinned == True:
                                    embed = discord.Embed(description=f"**Die folgende angeheftete Nachricht({after.id}) wurde in {after.channel.mention} bearbeitet:*", color=discord.Color.gold(), timestamp=datetime.now())
                                    embed.add_field(name="<:v_pfeil_links:1119582015042371604> Vorher", value=before.content, inline=False)
                                    embed.add_field(name="<:v_pfeil_rechts:1119582171930300438> Nachher", value=after.content, inline=False)
                                    embed.set_author(name=after.author, icon_url=after.author.avatar)
                                    embed.set_footer(text=f"Autor-ID: {after.author.id}")

                                    await channel.send(embed=embed)
                                else:
                                    embed = discord.Embed(description=f"**Nachricht({after.id}) wurde in {after.channel.mention} bearbeitet**", color=discord.Color.gold(), timestamp=datetime.now())
                                    embed.add_field(name="<:v_pfeil_links:1119582015042371604> Vorher", value=before.content, inline=False)
                                    embed.add_field(name="<:v_pfeil_rechts:1119582171930300438> Nachher", value=after.content, inline=False)
                                    embed.set_author(name=after.author, icon_url=after.author.avatar)
                                    embed.set_footer(text=f"Autor-ID: {after.author.id}")

                                    await channel.send(embed=embed)
                except:
                    pass

    #modlog

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def modlog(self, interaction: discord.Interaction,  modus: typing.Literal["An","Aus"], kanal: discord.TextChannel):
                """Setze den Modlog."""
                
                await interaction.response.defer()
                
                db = getMongoDataBase()
                
                if modus == "An":
                    result = await db["modlog"].find_one({"guildID": interaction.guild.id})
                    if result is None:
                        await db["modlog"].insert_one({"guildID": interaction.guild.id, "channelID": kanal.id})                        

                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Modlog", description=f"Der Modlog ist nun aktiv in {kanal.mention}.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        
                        await interaction.followup.send(embed=embed)
                        return
                    if result != None:
                        await db["modlog"].update_one({"guildID": interaction.guild.id}, {"$set": {"channelID": kanal.id}})                        

                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Modlog", description=f"Der Modlog ist nun aktiv in {kanal.mention}.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        
                        await interaction.followup.send(embed=embed)
                        return
                
                if modus == "Aus":
                    result = await db["modlog"].find_one({"guildID": interaction.guild.id})
                    if result is None:
                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Modlog", description=f"Der Modlog ist nicht aktiviert auf diesem Server.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        
                        await interaction.followup.send(embed=embed)
                        return
                    if result != None:
                        await db["modlog"].delete_one({"guildID": interaction.guild.id})

                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Modlog deaktiviert", description=f"Der Modlog ist auf diesem Server nun deaktiviert.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        
                        await interaction.followup.send(embed=embed)
                        return

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        result = await getMongoDataBase()["modlog"].find_one({"guildID": guild.id})
        if result is None:
            return
        if result != None:
            channel = await guild.fetch_channel(int(result["channelID"]))
            if channel is None:
                return
            else:
                async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                    embed = discord.Embed(title="Jemand wurde gebannt", color=discord.Color.orange(), timestamp=datetime.now())
                    embed.add_field(name="<:v_user:1119585450923929672> User", value=f"{entry.target.mention}({entry.target})")
                    embed.add_field(name="<:v_mod:1119581819122241621> Moderator", value=f"{entry.user.mention}({entry.user})")
                    embed.add_field(name="<:v_warnung:1119585706310905886> Grund", value=entry.reason if entry.reason else 'Kein grund angegeben')
                    
                    await channel.send(embed=embed)
                    break

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        result = await getMongoDataBase()["modlog"].find_one({"guildID": guild.id})
        if result is None:
            return
        if result != None:
            channel = await guild.fetch_channel(int(result["channelID"]))
            if channel is None:
                return
            else:
                async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                    embed = discord.Embed(title="Jemand wurde entbannt", color=discord.Color.orange(), timestamp=datetime.now())
                    embed.add_field(name="<:v_user:1119585450923929672> User", value=f"{entry.target.mention}({entry.target})")
                    embed.add_field(name="<:v_mod:1119581819122241621> Moderator", value=f"{entry.user.mention}({entry.user})")
                    embed.add_field(name="<:v_warnung:1119585706310905886> Grund", value=entry.reason if entry.reason else 'Kein grund angegeben')
                    
                    await channel.send(embed=embed)
                    break

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        try:
            result = await getMongoDataBase()["modlog"].find_one({"guildID": channel.guild.id})
            if result is None:
                return
            if result != None:
                chan = await channel.guild.fetch_channel(int(result["channelID"]))
                if chan is None:
                    return
                else:
                    async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
                        embed = discord.Embed(title=f"Ein {entry.target.type}kanal wurde erstellt", color=discord.Color.orange(), timestamp=datetime.now())
                        embed.add_field(name="<:v_chat:1119577968457568327> Name", value=f"{entry.target.mention}({entry.target.name})")
                        embed.add_field(name="<:v_user:1119585450923929672> User", value=f"{entry.user.mention}({entry.user})")
                        embed.add_field(name="<:v_einstellungen:1119578559086874636> Kategorie", value=entry.target.category)
                        
                        await chan.send(embed=embed)
                        break
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
            try:
                result = await getMongoDataBase()["modlog"].find_one({"guildID": after.guild.id})
                if result is None:
                    return
                if result != None:
                    chan = await after.guild.fetch_channel(int(result["channelID"]))
                    if chan is None:
                        return
                    else:
                        async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update):
                            if before.name != after.name:
                                embed = discord.Embed(title="Ein Kanal wurde umbenannt", color=discord.Color.orange(), timestamp=datetime.now())
                                embed.add_field(name="<:v_pfeil_links:1119582015042371604> Alt", value=before.name)
                                embed.add_field(name="<:v_pfeil_rechts:1119582171930300438> Neu", value=after.name)
                                embed.add_field(name="<:v_user:1119585450923929672> User", value=f"{entry.user.mention}({entry.user})")
                                
                                await chan.send(embed=embed)
                                break
                            if before.topic != after.topic:
                                embed = discord.Embed(title="Eine Kanalbeschreibung wurde geändert", color=discord.Color.orange(), timestamp=datetime.now())
                                embed.add_field(name="<:v_pfeil_links:1119582015042371604> Alt", value=before.topic if before.topic else 'Keine Beschreibung')
                                embed.add_field(name="<:v_pfeil_rechts:1119582171930300438> Neu", value=after.topic if after.topic else 'Keine Beschreibung')
                                embed.add_field(name="<:v_user:1119585450923929672> User", value=f"{entry.user.mention}({entry.user})")
                                
                                await chan.send(embed=embed)
                                break
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        try:
            result = await getMongoDataBase()["modlog"].find_one({"guildID": channel.guild.id})
            if result is None:
                return
            if result != None:
                chan = await channel.guild.fetch_channel(int(result["channelID"]))
                if chan is None:
                    return
                else:
                    async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
                        embed = discord.Embed(title=f"Ein {channel.type}kanal wurde gelöscht", color=discord.Color.orange(), timestamp=datetime.now())
                        embed.add_field(name="<:v_chat:1119577968457568327> Name", value=f"{channel.name}")
                        embed.add_field(name="<:v_user:1119585450923929672> User", value=f"{entry.user.mention}({entry.user})")
                        
                        await chan.send(embed=embed)
                        break
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        result = await getMongoDataBase()["modlog"].find_one({"guildID": role.guild.id})
        if result is None:
            return
        if result != None:
            chan = await role.guild.fetch_channel(int(result["channelID"]))
            if chan is None:
                return
            else:
                async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
                    embed = discord.Embed(title=f"Eine Rolle wurde erstellt", color=discord.Color.orange(), timestamp=datetime.now())
                    embed.add_field(name="<:v_chat:1119577968457568327> Name", value=f"{role.name}")
                    embed.add_field(name="<:v_user:1119585450923929672> User", value=f"{entry.user.mention}({entry.user})")
                    
                    await chan.send(embed=embed)
                    break

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        result = await getMongoDataBase()["modlog"].find_one({"guildID": role.guild.id})
        if result is None:
            return
        if result != None:
            chan = await role.guild.fetch_channel(int(result["channelID"]))
            if chan is None:
                return
            else:
                async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
                    embed = discord.Embed(title=f"Eine Rolle wurde gelöscht", color=discord.Color.orange(), timestamp=datetime.now())
                    embed.add_field(name="<:v_chat:1119577968457568327> Name", value=f"{role.name}")
                    embed.add_field(name="<:v_user:1119585450923929672> User", value=f"{entry.user.mention}({entry.user})")
                    
                    await chan.send(embed=embed)
                    break

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        
                db = getMongoDataBase()
        
                try:
                    if before.bot:
                        return
                    result = await db["modlog"].find_one({"guildID": after.guild.id})
                    if result is None:
                        return
                    if result != None:
                        chan = await before.guild.fetch_channel(int(result["channelID"]))
                        if chan is None:
                            return
                        if len(before.roles) > len(after.roles):
                            role = next(role for role in before.roles if role not in after.roles)

                            async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_role_update, limit=1):

                                embed = discord.Embed(title="Mitglied wurde geändert", description=f"{entry.user.mention} hat eine Rolle von einem Mitglied entzogen.",
                                                    colour=discord.Colour.orange(), timestamp=discord.utils.utcnow())
                                
                                fields = [("<:v_user:1119585450923929672> Betroffenes Mitglied", before.mention, True),
                                        ("<:v_levelup:1119581140240576612> Entzogende Rolle", role.mention, True)]

                                for name, value, inline in fields:
                                    embed.add_field(name=name, value=value, inline=inline)
                                await chan.send(embed=embed)

                    if len(after.roles) > len(before.roles):
                        role = next(role for role in after.roles if role not in before.roles)
                        async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_role_update, limit=1):

                            embed = discord.Embed(title="Mitglied wurde geändert", description=f"{entry.user.mention} hat eine Rolle zu einem Mitglied hinzugefügt.",
                                                colour=discord.Colour.orange(), timestamp=discord.utils.utcnow())
                            
                            fields = [("<:v_user:1119585450923929672> Betroffenes Mitglied", before.mention, True),
                                    ("<:v_levelup:1119581140240576612> Hinzugefügte Rolle", role.mention, True)]

                            for name, value, inline in fields:
                                embed.add_field(name=name, value=value, inline=inline)
                            await chan.send(embed=embed)
                        else:
                            if before.nick != after.nick:
                                if after.nick is None:
                                    embed = discord.Embed(description=f"**Nickname**\n{before} hat seinen Spitznamen zurückgesetzt.", color=discord.Color.orange(), timestamp=datetime.now())
                                    
                                    await chan.send(embed=embed)
                                else:
                                    embed = discord.Embed(description=f"**Nickname**\n{before} hat seinen Nicknamen zu {after.nick} geändert.", color=discord.Color.orange(), timestamp=datetime.now())
                                    
                                    await chan.send(embed=embed)
                except:
                    pass

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def ticketlog(self, interaction: discord.Interaction,  modus: typing.Literal["An","Aus"], kanal: discord.TextChannel):
        """Setze den Ticketlog."""
        
        await interaction.response.defer()
        
        #premium_status = await haspremium_forserver(self, interaction.guild)
        #if premium_status == False:
        #    return await interaction.followup.send("**<:v_kreuz:1119580775411621908> Du kannst dies nicht tun, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")

        db = getMongoDataBase()

        if modus == "An":
            result = await db["ticketlog"].find_one({"guildID": interaction.guild.id})
            
            if result is None:
                await db["ticketlog"].insert_one({"guildID": interaction.guild.id, "channelID": kanal.id})                

                embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Ticketlog", description=f"Der Ticketlog ist nun aktiv in {kanal.mention}.")
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                
                await interaction.followup.send(embed=embed)
                return
            if result != None:
                await db["ticketlog"].update_one({"guildID": interaction.guild.id}, {"$set": {"channelID": kanal.id}})                

                embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Ticketlog", description=f"Der Ticketlog ist nun aktiv in {kanal.mention}.")
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                
                await interaction.followup.send(embed=embed)
                return
                
        if modus == "Aus":
            result = await db["ticketlog"].find_one({"guildID": interaction.guild.id})
            if result is None:
                embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Ticketlog", description=f"Der Ticketlog ist nicht aktiviert auf diesem Server.")
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)

                await interaction.followup.send(embed=embed)
                return
            if result != None:
                await db["ticketlog"].delete_one({"guildID": interaction.guild.id})


                embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Ticketlog deaktiviert", description=f"Der Ticketlog ist auf diesem Server nun deaktiviert.")
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        
                await interaction.followup.send(embed=embed)
                return
        
async def setup(bot):
    await bot.add_cog(logging(bot))