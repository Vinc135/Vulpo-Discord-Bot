import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import typing
from info import getcolour

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
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if argument == "Ausschalten":
                    await cursor.execute(f"SELECT channelID FROM reportlog WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    if result == None:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Auf diesem Server ist kein Reportlog eingerichtet.**", ephemeral=True)
                    await cursor.execute("DELETE FROM reportlog WHERE guildID = (%s)", (interaction.guild.id))
                    return await interaction.response.send_message("**<:v_haken:1048677657040134195> Der Reportlog wurde ausgeschaltet.**")
                if argument == "Einrichten (Kanal muss mit angegeben werden)":
                    if kanal == None:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Beim Einrichten ist auch eine Kanal-Angabe erforderlich.**", ephemeral=True)

                    await cursor.execute(f"SELECT channelID FROM reportlog WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    if result:
                        await cursor.execute("UPDATE reportlog SET channelID = (%s) WHERE guildID = (%s)", (kanal.id, interaction.guild.id))
                    else:
                        await cursor.execute("INSERT INTO reportlog(guildID, channelID) VALUES(%s, %s)", (interaction.guild.id, kanal.id))
                    await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Der Reportlog ist nun aktiv in {kanal.mention}.**")
                if argument == "Anzeigen":
                    await cursor.execute(f"SELECT channelID FROM reportlog WHERE guildID = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    try:
                        channel = interaction.guild.get_channel(int(result[0]))
                    except:
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Der Kanal des Reportlogs existiert nicht mehr. Bitte deaktiviere den Reportlog und richte ihn erneut ein.**", ephemeral=True)

                    embed = discord.Embed(title="Reportlog", description=f"Der aktuelle Reportlog ist aktiv in {channel.mention}", color=await getcolour(self, interaction.user))
                    await interaction.response.send_message(embed=embed)
    #messagelog

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def messagelog(self, interaction: discord.Interaction, modus: typing.Literal["An","Aus"], kanal: discord.TextChannel):
        """Setze den Nachrichtenlog."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if modus == "An":
                    await cursor.execute(f"SELECT channelid FROM messagelog WHERE guildid = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    if result is None:
                        await cursor.execute("INSERT INTO messagelog(guildid, channelid) VALUES(%s, %s)", (interaction.guild.id, kanal.id))
                        

                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Nachrichtenlog", description=f"Der Nachrichtenlog ist nun aktiv in {kanal.mention}.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        await interaction.response.send_message(embed=embed)
                        return
                    if result != None:
                        await cursor.execute(f"UPDATE messagelog SET channelid = {kanal.id} WHERE guildid = {interaction.guild.id}")
                        
                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Nachrichtenlog", description=f"Der Nachrichtenlog ist nun aktiv in {kanal.mention}.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        await interaction.response.send_message(embed=embed)
                        return
            
                if modus == "Aus":
                    await cursor.execute(f"SELECT channelid FROM messagelog WHERE guildid = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    if result is None:
                        embed = discord.Embed(colour=discord.Colour.red(), title="Messagelog", description=f"Der Nachrichtenlog ist nicht aktiviert auf diesem Server.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        await interaction.response.send_message(embed=embed)
                        return
                    if result != None:
                        await cursor.execute(f"DELETE FROM messagelog WHERE guildid = {interaction.guild.id}")
                        

                        embed = discord.Embed(colour=discord.Colour.red(), title="Messagelog deaktiviert", description=f"Der Nachrichtenlog ist nun deaktiviert auf diesem Server.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        await interaction.response.send_message(embed=embed)
                        return
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild == None:
            return
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(f"SELECT channelid FROM messagelog WHERE guildid = {message.guild.id}")
                    result = await cursor.fetchone()
                    if result is None:
                        return
                    if result != None:
                        channel = message.guild.get_channel(int(result[0]))
                        if channel is None:
                            return
                        else:
                            embed = discord.Embed(title="Eine Nachricht wurde gelöscht", color=discord.Color.red(), timestamp=datetime.utcnow())
                            embed.add_field(name="Autor", value=message.author)
                            embed.add_field(name="Kanal", value=message.channel.mention)
                            embed.add_field(name="Nachricht", value=message.content)

                            await channel.send(embed=embed)
                except:
                    pass

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                for message in messages:
                    await cursor.execute(f"SELECT channelid FROM messagelog WHERE guildid = {message.guild.id}")
                    break
                result = await cursor.fetchone()
                if result is None:
                    return
                if result != None:
                    channel = message.guild.get_channel(int(result[0]))
                    if channel is None:
                        return
                    else:
                        embed = discord.Embed(description=f"**{len(messages)} Nachrichten in {message.channel.mention} gelöscht**", color=discord.Color.red(), timestamp=datetime.utcnow())

                        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.guild == None:
            return
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(f"SELECT channelid FROM messagelog WHERE guildid = {after.guild.id}")
                    result = await cursor.fetchone()
                    if result is None:
                        return
                    if result != None:
                        channel = after.guild.get_channel(int(result[0]))
                        if channel is None:
                            return
                        else:
                            if before.pinned == False and after.pinned == True:
                                embed = discord.Embed(description=f"**Die folgende Nachricht({after.id}) wurde in {after.channel.mention} angeheftet:**\n{after.content}", color=discord.Color.gold(), timestamp=datetime.utcnow())
                                embed.set_author(name=after.author, icon_url=after.author.avatar)
                                embed.set_footer(text=f"Autor-ID: {after.author.id}")

                                await channel.send(embed=embed)
                                return
                                
                            if before.pinned == True and after.pinned == False:
                                embed = discord.Embed(description=f"**Die folgende Nachricht({after.id}) wurde in {after.channel.mention} losgelöst:**\n{after.content}", color=discord.Color.gold(), timestamp=datetime.utcnow())
                                embed.set_author(name=after.author, icon_url=after.author.avatar)
                                embed.set_footer(text=f"Autor-ID: {after.author.id}")

                                await channel.send(embed=embed)
                                
                            if before.content != after.content:
                                if before.pinned == True and after.pinned == True:
                                    embed = discord.Embed(description=f"**Die folgende angeheftete Nachricht({after.id}) wurde in {after.channel.mention} bearbeitet:*", color=discord.Color.gold(), timestamp=datetime.utcnow())
                                    embed.add_field(name="Vorher", value=before.content, inline=False)
                                    embed.add_field(name="Nachher", value=after.content, inline=False)
                                    embed.set_author(name=after.author, icon_url=after.author.avatar)
                                    embed.set_footer(text=f"Autor-ID: {after.author.id}")

                                    await channel.send(embed=embed)
                                else:
                                    embed = discord.Embed(description=f"**Nachricht({after.id}) wurde in {after.channel.mention} bearbeitet**", color=discord.Color.gold(), timestamp=datetime.utcnow())
                                    embed.add_field(name="Vorher", value=before.content, inline=False)
                                    embed.add_field(name="Nachher", value=after.content, inline=False)
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
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if modus == "An":
                    await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    if result is None:
                        await cursor.execute("INSERT INTO modlog(guildid, channelid) VALUES(%s, %s)", (interaction.guild.id, kanal.id))
                        

                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Modlog", description=f"Der Modlog ist nun aktiv in {kanal.mention}.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        await interaction.response.send_message(embed=embed)
                        return
                    if result != None:
                        await cursor.execute(f"UPDATE modlog SET channelid = {kanal.id} WHERE guildid = {interaction.guild.id}")
                        

                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Modlog", description=f"Der Modlog ist nun aktiv in {kanal.mention}.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        await interaction.response.send_message(embed=embed)
                        return
                
                if modus == "Aus":
                    await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {interaction.guild.id}")
                    result = await cursor.fetchone()
                    if result is None:
                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Modlog", description=f"Der Modlog ist nicht aktiviert auf diesem Server.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        await interaction.response.send_message(embed=embed)
                        return
                    if result != None:
                        await cursor.execute(f"DELETE FROM modlog WHERE guildid = {interaction.guild.id}")
                        

                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Modlog deaktiviert", description=f"Der Modlog ist auf diesem Server nun deaktiviert.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        await interaction.response.send_message(embed=embed)
                        return

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {guild.id}")
                result = await cursor.fetchone()
                if result is None:
                    return
                if result != None:
                    channel = guild.get_channel(int(result[0]))
                    if channel is None:
                        return
                    else:
                        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                            embed = discord.Embed(title="Jemand wurde gebannt", color=discord.Color.red(), timestamp=datetime.utcnow())
                            embed.add_field(name="User", value=f"{entry.target.mention}({entry.target})")
                            embed.add_field(name="Moderator", value=f"{entry.user.mention}({entry.user})")
                            embed.add_field(name="Grund", value=entry.reason if entry.reason else 'Kein grund angegeben')

                            await channel.send(embed=embed)
                            break

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {guild.id}")
                result = await cursor.fetchone()
                if result is None:
                    return
                if result != None:
                    channel = guild.get_channel(int(result[0]))
                    if channel is None:
                        return
                    else:
                        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                            embed = discord.Embed(title="Jemand wurde entbannt", color=discord.Color.green(), timestamp=datetime.utcnow())
                            embed.add_field(name="User", value=f"{entry.target.mention}({entry.target})")
                            embed.add_field(name="Moderator", value=f"{entry.user.mention}({entry.user})")
                            embed.add_field(name="Grund", value=entry.reason if entry.reason else 'Kein grund angegeben')

                            await channel.send(embed=embed)
                            break

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {channel.guild.id}")
                result = await cursor.fetchone()
                if result is None:
                    return
                if result != None:
                    chan = channel.guild.get_channel(int(result[0]))
                    if chan is None:
                        return
                    else:
                        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
                            embed = discord.Embed(title=f"Ein {entry.target.type}kanal wurde erstellt", color=discord.Color.green(), timestamp=datetime.utcnow())
                            embed.add_field(name="Name", value=f"{entry.target.mention}({entry.target.name})")
                            embed.add_field(name="User", value=f"{entry.user.mention}({entry.user})")
                            embed.add_field(name="Kategory", value=entry.target.category)

                            await chan.send(embed=embed)
                            break

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {after.guild.id}")
                    result = await cursor.fetchone()
                    if result is None:
                        return
                    if result != None:
                        chan = after.guild.get_channel(int(result[0]))
                        if chan is None:
                            return
                        else:
                            async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update):
                                if before.name != after.name:
                                    embed = discord.Embed(title="Ein Kanal wurde umbenannt", color=discord.Color.green(), timestamp=datetime.utcnow())
                                    embed.add_field(name="Alt", value=before.name)
                                    embed.add_field(name="Neu", value=after.name)
                                    embed.add_field(name="User", value=f"{entry.user.mention}({entry.user})")

                                    await chan.send(embed=embed)
                                    break
                                if before.topic != after.topic:
                                    embed = discord.Embed(title="Eine Kanalbeschreibung wurde geändert", color=discord.Color.green(), timestamp=datetime.utcnow())
                                    embed.add_field(name="Alt", value=before.topic if before.topic else 'Keine Beschreibung')
                                    embed.add_field(name="Neu", value=after.topic if after.topic else 'Keine Beschreibung')
                                    embed.add_field(name="User", value=f"{entry.user.mention}({entry.user})")

                                    await chan.send(embed=embed)
                                    break
                except:
                    pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {channel.guild.id}")
                result = await cursor.fetchone()
                if result is None:
                    return
                if result != None:
                    chan = channel.guild.get_channel(int(result[0]))
                    if chan is None:
                        return
                    else:
                        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
                            embed = discord.Embed(title=f"Ein {channel.type}kanal wurde gelöscht", color=discord.Color.red(), timestamp=datetime.utcnow())
                            embed.add_field(name="Name", value=f"{channel.name}")
                            embed.add_field(name="User", value=f"{entry.user.mention}({entry.user})")

                            await chan.send(embed=embed)
                            break

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {role.guild.id}")
                result = await cursor.fetchone()
                if result is None:
                    return
                if result != None:
                    chan = role.guild.get_channel(int(result[0]))
                    if chan is None:
                        return
                    else:
                        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
                            embed = discord.Embed(title=f"Eine Rolle wurde erstellt", color=discord.Color.green(), timestamp=datetime.utcnow())
                            embed.add_field(name="Name", value=f"{role.name}")
                            embed.add_field(name="User", value=f"{entry.user.mention}({entry.user})")

                            await chan.send(embed=embed)
                            break

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {role.guild.id}")
                result = await cursor.fetchone()
                if result is None:
                    return
                if result != None:
                    chan = role.guild.get_channel(int(result[0]))
                    if chan is None:
                        return
                    else:
                        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
                            embed = discord.Embed(title=f"Eine Rolle wurde gelöscht", color=discord.Color.red(), timestamp=datetime.utcnow())
                            embed.add_field(name="Name", value=f"{role.name}")
                            embed.add_field(name="User", value=f"{entry.user.mention}({entry.user})")

                            await chan.send(embed=embed)
                            break

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    if before.bot:
                        return
                    await cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {before.guild.id}")
                    result = await cursor.fetchone()
                    if result is None:
                        return
                    if result != None:
                        chan = before.guild.get_channel(int(result[0]))
                        if chan is None:
                            return
                        if len(before.roles) > len(after.roles):
                            role = next(role for role in before.roles if role not in after.roles)

                            async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_role_update, limit=1):

                                embed = discord.Embed(title="Mitglied wurde geändert", description=f"{entry.user.mention} hat eine Rolle von einem Mitglied entzogen.",
                                                    colour=discord.Colour.orange(), timestamp=discord.utils.utcnow())

                                fields = [("Betroffenes Mitglied", before.mention, True),
                                        ("Entzogende Rolle", role.mention, True)]

                                for name, value, inline in fields:
                                    embed.add_field(name=name, value=value, inline=inline)
                                await chan.send(embed=embed)

                    if len(after.roles) > len(before.roles):
                        role = next(role for role in after.roles if role not in before.roles)
                        async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_role_update, limit=1):

                            embed = discord.Embed(title="Mitglied wurde geändert", description=f"{entry.user.mention} hat eine Rolle zu einem Mitglied hinzugefügt.",
                                                colour=discord.Colour.orange(), timestamp=discord.utils.utcnow())

                            fields = [("Betroffenes Mitglied", before.mention, True),
                                    ("Hinzugefügte Rolle", role.mention, True)]

                            for name, value, inline in fields:
                                embed.add_field(name=name, value=value, inline=inline)
                            await chan.send(embed=embed)
                        else:
                            if before.nick != after.nick:
                                if after.nick is None:
                                    embed = discord.Embed(description=f"**Nickname**\n{before} hat seinen Spitznamen zurückgesetzt.", color=discord.Color.green(), timestamp=datetime.utcnow())

                                    await chan.send(embed=embed)
                                else:
                                    embed = discord.Embed(description=f"**Nickname**\n{before} hat seinen Nicknamen zu {after.nick} geändert.", color=discord.Color.gold(), timestamp=datetime.utcnow())

                                    await chan.send(embed=embed)
                except:
                    pass

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def ticketlog(self, interaction: discord.Interaction,  modus: typing.Literal["An","Aus"], kanal: discord.TextChannel):
        """Setze den Ticketlog."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if modus == "An":
                    await cursor.execute("SELECT channelid FROM ticketlog WHERE guildid = (%s)", (interaction.guild.id))
                    result = await cursor.fetchone()
                    if result is None:
                        await cursor.execute("INSERT INTO ticketlog(guildid, channelid) VALUES(%s, %s)", (interaction.guild.id, kanal.id))
                        

                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Ticketlog", description=f"Der Ticketlog ist nun aktiv in {kanal.mention}.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        await interaction.response.send_message(embed=embed)
                        return
                    if result != None:
                        await cursor.execute("UPDATE ticketlog SET channelid = (%s) WHERE guildid = (%s)", (kanal.id, interaction.guild.id))
                        

                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Ticketlog", description=f"Der Ticketlog ist nun aktiv in {kanal.mention}.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        await interaction.response.send_message(embed=embed)
                        return
                
                if modus == "Aus":
                    await cursor.execute("SELECT channelid FROM ticketlog WHERE guildid = (%s)", (interaction.guild.id))
                    result = await cursor.fetchone()
                    if result is None:
                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Ticketlog", description=f"Der Ticketlog ist nicht aktiviert auf diesem Server.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        await interaction.response.send_message(embed=embed)
                        return
                    if result != None:
                        await cursor.execute("DELETE FROM ticketlog WHERE guildid = (%s)", (interaction.guild.id))
                        

                        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Ticketlog deaktiviert", description=f"Der Ticketlog ist auf diesem Server nun deaktiviert.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        await interaction.response.send_message(embed=embed)
                        return
        
async def setup(bot):
    await bot.add_cog(logging(bot))