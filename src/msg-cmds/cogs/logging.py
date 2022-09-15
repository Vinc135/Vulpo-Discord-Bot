import discord
from discord.ext import commands

import mysql.connector
from info import get_syntax
from datetime import datetime

class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #messagelog

    @commands.command(usage="<enable <#channel> /disable>", aliases=["mel"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(ban_members=True)
    async def messagelog(self, ctx, endis=None, channel: discord.TextChannel=None):
        """Setze den Nachrichtenlog."""
        if endis == None:
            await get_syntax(ctx)
            return
        if endis == "enable":
            if channel == None:
                await get_syntax(ctx)
                return
            else:
                mydb = mysql.connector.connect(
                    host="54.37.204.19",
                    user="u60388_adFMo8yi8w",
                    password="dNPaL8=W2qapSVrwv=Q9Me8I",
                    database="s60388_Vulpo"
                )
                cursor = mydb.cursor(buffered=True)
                cursor.execute(f"SELECT channelid FROM messagelog WHERE guildid = {ctx.guild.id}")
                result = cursor.fetchone()
                if result is None:
                    cursor.execute("INSERT INTO messagelog(guildid, channelid) VALUES(%s, %s)", (ctx.guild.id, channel.id))
                    mydb.commit()
                    mydb.close()

                    embed = discord.Embed(colour=discord.Colour.orange(), title="Nachrichtenlog", description=f"Der Nachrichtenlog ist nun aktiv in {channel.mention}.")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await ctx.send(embed=embed)
                    return
                if result != None:
                    cursor.execute(f"UPDATE messagelog SET channelid = {channel.id} WHERE guildid = {ctx.guild.id}")
                    mydb.commit()
                    mydb.close()

                    embed = discord.Embed(colour=discord.Colour.orange(), title="Nachrichtenlog", description=f"Der Nachrichtenlog ist nun aktiv in {channel.mention}.")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await ctx.send(embed=embed)
                    return
        
        if endis == "disable":
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT channelid FROM messagelog WHERE guildid = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                embed = discord.Embed(colour=discord.Colour.red(), title="Messagelog", description=f"Der Nachrichtenlog ist nicht aktiviert auf diesem Server.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                mydb.close()
                return
            if result != None:
                cursor.execute(f"DELETE FROM messagelog WHERE guildid = {ctx.guild.id}")
                mydb.commit()
                mydb.close()

                embed = discord.Embed(colour=discord.Colour.red(), title="Messagelog deaktiviert", description=f"Der Nachrichtenlog ist nun deaktiviert auf diesem Server.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

        else:
            await get_syntax(ctx)
            return

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild == None:
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        try:
            try:
                cursor = mydb.cursor(buffered=True)
                cursor.execute(f"SELECT channelid FROM messagelog WHERE guildid = {message.guild.id}")
                result = cursor.fetchone()
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
        except:
            pass
        mydb.close()

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        for message in messages:
            cursor.execute(f"SELECT channelid FROM messagelog WHERE guildid = {message.guild.id}")
            break
        result = cursor.fetchone()
        if result is None:
            return
        if result != None:
            channel = message.guild.get_channel(int(result[0]))
            if channel is None:
                return
            else:
                embed = discord.Embed(description=f"**{len(messages)} Nachrichten in {message.channel.mention} gelöscht**", color=discord.Color.red(), timestamp=datetime.utcnow())

                await channel.send(embed=embed)
        mydb.close()

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.guild == None:
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        try:
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT channelid FROM messagelog WHERE guildid = {after.guild.id}")
            result = cursor.fetchone()
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
        mydb.close()

    #modlog

    @commands.command(usage="<enable <#channel> /disable>", aliases=["mol"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(ban_members=True)
    async def modlog(self, ctx, endis=None, channel: discord.TextChannel=None):
        """Setze den Modlog."""
        if endis == None:
            await get_syntax(ctx)
            return
        if endis == "enable":
            if channel == None:
                await get_syntax(ctx)
                return
            else:
                mydb = mysql.connector.connect(
                    host="54.37.204.19",
                    user="u60388_adFMo8yi8w",
                    password="dNPaL8=W2qapSVrwv=Q9Me8I",
                    database="s60388_Vulpo"
                )
                cursor = mydb.cursor(buffered=True)
                cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {ctx.guild.id}")
                result = cursor.fetchone()
                if result is None:
                    cursor.execute("INSERT INTO modlog(guildid, channelid) VALUES(%s, %s)", (ctx.guild.id, channel.id))
                    mydb.commit()
                    mydb.close()

                    embed = discord.Embed(colour=discord.Colour.orange(), title="Modlog", description=f"Der Modlog ist nun aktiv in {channel.mention}.")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await ctx.send(embed=embed)
                    return
                if result != None:
                    cursor.execute(f"UPDATE modlog SET channelid = {channel.id} WHERE guildid = {ctx.guild.id}")
                    mydb.commit()
                    mydb.close()

                    embed = discord.Embed(colour=discord.Colour.orange(), title="Modlog", description=f"Der Modlog ist nun aktiv in {channel.mention}.")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await ctx.send(embed=embed)
                    return
        
        if endis == "disable":
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                embed = discord.Embed(colour=discord.Colour.red(), title="Modlog", description=f"Der Modlog ist nicht aktiviert auf diesem Server.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return
            if result != None:
                cursor.execute(f"DELETE FROM modlog WHERE guildid = {ctx.guild.id}")
                mydb.commit()
                mydb.close()

                embed = discord.Embed(colour=discord.Colour.red(), title="Modlog deaktiviert", description=f"Der Modlog ist auf diesem Server nun deaktiviert.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

        else:
            await get_syntax(ctx)
            return
        mydb.close()

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {guild.id}")
        result = cursor.fetchone()
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
        mydb.close()
    
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {guild.id}")
        result = cursor.fetchone()
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
        mydb.close()

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {channel.guild.id}")
        result = cursor.fetchone()
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
        mydb.close()

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        try:
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {after.guild.id}")
            result = cursor.fetchone()
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
        mydb.close()


    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {channel.guild.id}")
        result = cursor.fetchone()
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
        mydb.close()

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {role.guild.id}")
        result = cursor.fetchone()
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
        mydb.close()

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {role.guild.id}")
        result = cursor.fetchone()
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
        mydb.close()

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if before.bot:
                return
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT channelid FROM modlog WHERE guildid = {before.guild.id}")
            result = cursor.fetchone()
            if result is None:
                return
            if result != None:
                chan = before.guild.get_channel(int(result[0]))
                if chan is None:
                    return
                else:
                    if before.nick != after.nick:
                        if after.nick is None:
                            embed = discord.Embed(description=f"**Nickname**\n{before} hat seinen Spitznamen zurückgesetzt.", color=discord.Color.green(), timestamp=datetime.utcnow())

                            await chan.send(embed=embed)
                            return
                        else:
                            embed = discord.Embed(description=f"**Nickname**\n{before} hat seinen Nicknamen zu {after.nick} geändert.", color=discord.Color.gold(), timestamp=datetime.utcnow())

                            await chan.send(embed=embed)
            mydb.close()
        except:
            pass

    @commands.command(usage="<enable <#channel> /disable>", aliases=["til"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(ban_members=True)
    async def ticketlog(self, ctx, endis=None, channel: discord.TextChannel=None):
        """Setze den Ticketlog."""
        if endis == None:
            await get_syntax(ctx)
            return
        if endis == "enable":
            if channel == None:
                await get_syntax(ctx)
                return
            else:
                mydb = mysql.connector.connect(
                    host="54.37.204.19",
                    user="u60388_adFMo8yi8w",
                    password="dNPaL8=W2qapSVrwv=Q9Me8I",
                    database="s60388_Vulpo"
                )
                cursor = mydb.cursor(buffered=True)
                cursor.execute(f"SELECT channelid FROM ticketlog WHERE guildid = {ctx.guild.id}")
                result = cursor.fetchone()
                if result is None:
                    cursor.execute("INSERT INTO ticketlog(guildid, channelid) VALUES(%s, %s)", (ctx.guild.id, channel.id))
                    mydb.commit()
                    mydb.close()

                    embed = discord.Embed(colour=discord.Colour.orange(), title="Ticketlog", description=f"Der Ticketlog ist nun aktiv in {channel.mention}.")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await ctx.send(embed=embed)
                    return
                if result != None:
                    cursor.execute(f"UPDATE ticketlog SET channelid = {channel.id} WHERE guildid = {ctx.guild.id}")
                    mydb.commit()
                    mydb.close()

                    embed = discord.Embed(colour=discord.Colour.orange(), title="Ticketlog", description=f"Der Ticketlog ist nun aktiv in {channel.mention}.")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await ctx.send(embed=embed)
                    return
        
        if endis == "disable":
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT channelid FROM ticketlog WHERE guildid = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                embed = discord.Embed(colour=discord.Colour.red(), title="Ticketlog", description=f"Der Ticketlog ist nicht aktiviert auf diesem Server.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return
            if result != None:
                cursor.execute(f"DELETE FROM ticketlog WHERE guildid = {ctx.guild.id}")
                mydb.commit()
                mydb.close()

                embed = discord.Embed(colour=discord.Colour.red(), title="Ticketlog deaktiviert", description=f"Der Ticketlog ist auf diesem Server nun deaktiviert.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

        else:
            await get_syntax(ctx)
            return
        mydb.close()
        
async def setup(bot):
    await bot.add_cog(logging(bot))