import asyncio
import discord
from discord.ext import commands
from datetime import datetime
import random
import os
from info import get_syntax
import aiomysql

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipe_message_author = {}
        self.snipe_message_content = {}
        self.snipe_message_channel = {}

    @commands.command(usage="<user/ID> <reason>", aliases=["k", ])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member = None, *, reason: str = None):
        """Lässt einen Benutzer kicken. Wenn möglich."""
        if user is None or reason is None:
            await get_syntax(ctx)
            return
        elif user.guild_permissions.kick_members:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f"{user.mention} kann nicht gekickt werden, da er das Recht hat, Mitglieder zu kicken.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(colour=discord.Colour.orange(),
                                  description=f"Der Benutzer {user} (**{user.id}**) wurde gekickt.")
            embed.add_field(name=f"🎛️ Server:", value=f"{ctx.guild.name}", inline=False)
            embed.add_field(name=f"👮 Moderator:", value=f"{ctx.author} (**{ctx.author.id}**)", inline=False)
            embed.add_field(name=f"📄 Grund:", value=f"{reason}", inline=False)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

            dm = discord.Embed(colour=discord.Colour.orange(),
                               description=f"Hey {user.mention}! \nDu wurdest auf dem Server **{ctx.guild.name}** gekickt! Genauere Informationen hier:")
            dm.add_field(name=f"🎛️ Server:", value=f"{ctx.guild.name}", inline=False)
            dm.add_field(name=f"👮 Moderator:", value=f"{ctx.author.mention}", inline=False)
            dm.add_field(name=f"📄 Grund:", value=f"{reason}", inline=False)
            dm.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            try:
                await user.send(embed=dm)
                await user.kick(reason=reason)
                await ctx.send(embed=embed)
            except:
                await user.kick(reason=reason)
                await ctx.send(embed=embed)
                await ctx.send("Ich konnte die Nachricht nicht an den Benutzer senden.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, amount=None):
        if amount is None:
            await get_syntax(ctx)
            return
        try:
            amount = int(amount)
        except:
            await get_syntax(ctx)
            return
        await ctx.channel.edit(reason='Bot Slowmode Befehl', slowmode_delay=int(amount))
        embed = discord.Embed(title="⏰ Slowmode setzen",
                              description=f"Der Slowmode wurde auf **{amount}** Sekunden gesetzt.",
                              colour=discord.Colour.blue())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command(usage="<user/ID> <reason>", aliases=["b", ])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member = None, *, reason: str = None):
        """Sperrt einen Benutzer. Wenn möglich."""
        if user is None or reason is None:
            await get_syntax(ctx)
            return
        elif user.guild_permissions.ban_members:
            embed = discord.Embed(colour=discord.Color.red(),
                                  description=f"{user.mention} kann nicht gebannt werden, da er die Rechte 'Mitglieder bannen' hat.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f"Der Benutzer {user} (**{user.id}**) wurde gebannt.")
            embed.add_field(name=f"🎛️ Server:", value=f"{ctx.guild.name}", inline=False)
            embed.add_field(name=f"👮 Moderator:", value=f"{ctx.author} (**{ctx.author.id}**)", inline=False)
            embed.add_field(name=f"📄 Grund:", value=f"{reason}", inline=False)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

            dm = discord.Embed(colour=discord.Colour.red(),
                               description=f"Hey {user.mention}! \nDu wurdest auf dem Server **{ctx.guild.name}** gebannt! Genauere Informationen hier:")
            dm.add_field(name=f"🎛️ Server:", value=f"{ctx.guild.name}", inline=False)
            dm.add_field(name=f"👮 Moderator:", value=f"{ctx.author.mention}", inline=False)
            dm.add_field(name=f"📄 Grund:", value=f"{reason}", inline=False)
            dm.set_author(name=ctx.author, icon_url=ctx.author.avatar)

            try:
                await user.send(embed=dm)
                await user.ban(reason=reason)
                await ctx.send(embed=embed)
            except:
                await user.ban(reason=reason)
                await ctx.send(embed=embed)
                await ctx.send("Ich konnte die Nachricht nicht an den Benutzer senden.")

    @commands.command(usage="<ID> <reason>", aliases=["gb"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(ban_members=True)
    async def ghostban(self, ctx, ids: int, *, reason: str = None):
        """Sperrt einen Benutzer. Wenn möglich."""
        if ids is None or reason is None:
            await get_syntax(ctx)
            return
        else:
            ban_user = discord.Object(ids)
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f"Der Benutzer mit der ID {ids} wurde gebannt.")
            embed.add_field(name=f"🎛️ Server:", value=f"{ctx.guild.name}", inline=False)
            embed.add_field(name=f"👮 Moderator:", value=f"{ctx.author} (**{ctx.author.id}**)", inline=False)
            embed.add_field(name=f"📄 Grund:", value=f"{reason}", inline=False)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            try:
                await ctx.guild.ban(ban_user, reason=reason)
                await ctx.send(embed=embed)
            except:
                await ctx.guild.ban(embed, reason=reason)
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member=None):
        """Entbanne einen Member."""
        if member is None:
            await get_syntax(ctx)
            return
        else:
            banned_user = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_user:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f"User {member} wurde entbannt")
                    return
            await ctx.send("Der Benutzer wurde nicht in der Sperrliste gefunden.")

    @commands.group(usage="", aliases=["bans"])
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(ban_members=True)
    async def banlist(self, ctx):
        """Listet alle gesperrten Benutzer auf diesem Server auf."""
        a = 0
        users = [ban async for ban in ctx.guild.bans()]
        if len(users) > 0:
            msg1 = f'__**Username**__ — __**Grund**__\n'
            for entry in users:
                userName = str(entry.user)
                if entry.user.bot:
                    userName = '🤖 ' + userName
                reason = str(entry.reason)
                msg1 += f'{userName} — {reason}\n'
                a += 1
            try:
                for chunk in [msg1[i:i + 2000] for i in range(0, len(msg1), 2000)]:
                    embed = discord.Embed(title="Banlist", description=f"{msg1}", color=discord.Color.red())
                    embed.set_thumbnail(url=ctx.guild.icon)
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    embed.set_footer(text=f"{a} gesperrte Benutzer in dieser Server.")
                    await ctx.send(embed=embed)
            except discord.HTTPException:
                embed2 = discord.Embed(title="Banlist", description=f"{msg1}", color=discord.Color.red())
                embed2.set_thumbnail(url=ctx.guild.icon)
                embed2.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                embed.set_footer(text=f"{a} gesperrte Benutzer in dieser Server.")
                await ctx.send(embed=embed2)
        else:
            await ctx.send('No banned users on this server!')

    @commands.command(usage="<user/ID> <reason>", aliases=["shortban"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, user: discord.Member = None, *, reason=None):
        """Kickt einen User aus dem Discord Server und löscht seine Nachrichten der letzten 7 Tage. Der Nutzer wird hierüber nach Möglichkeit per DM informiert."""
        if user is None or reason is None:
            await get_syntax(ctx)
            return
        elif user.guild_permissions.ban_members:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f"{user.mention} kann nicht softbannt werden, da er die Rechte **Mitglieder sperren** hat.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f"Der Benutzer {user} (**{user.id}**) wurde softbannt.")
            embed.add_field(name=f"🎛️ Server:", value=f"{ctx.guild.name}", inline=False)
            embed.add_field(name=f"👮 Moderator:", value=f"{ctx.author} (**{ctx.author.id}**)", inline=False)
            embed.add_field(name=f"📄 Grund:", value=f"{reason}", inline=False)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

            dm = discord.Embed(colour=discord.Colour.red(),
                               description=f"Hey {user.mention}! \nDu wurdest auf dem Server ** {ctx.guild.name} ** gesperrt! Genauere Informationen hier:")
            dm.add_field(name=f"🎛️ Server:", value=f"{ctx.guild.name}", inline=False)
            dm.add_field(name=f"👮 Moderator:", value=f"{ctx.author.mention}", inline=False)
            dm.add_field(name=f"📄 Grund:", value=f"{reason}", inline=False)
            dm.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            try:
                await user.send(embed=dm)
                await ctx.guild.ban(user=user, reason=reason, delete_message_days=7)
                await ctx.guild.unban(user=user)
                await ctx.send(embed=embed)
            except:
                await ctx.guild.ban(user=user, reason=reason, delete_message_days=7)
                await ctx.guild.unban(user=user)
                await ctx.send(embed=embed)
                await ctx.send("Ich konnte die Nachricht nicht an den Benutzer senden.")

    @commands.command(usage="<number>", aliases=["purge"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = None):
        """Löscht eine bestimmte Anzahl von Nachrichten."""
        if amount is None:
            await get_syntax(ctx)
            return
        else:
            if int(amount) < 300:
                deleted = await ctx.message.channel.purge(limit=amount + 1)
                embed = discord.Embed(colour=discord.Colour.green(),
                                      description=f"{len(deleted) - 1} Nachricht/en gelöscht.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

                await ctx.send(embed=embed, delete_after=3)

            if int(amount) >= 300:
                embed = discord.Embed(colour=discord.Colour.red(),
                                      description="❌ Deine Nummer darf nicht größer als 300 sein.",
                                      timestamp=datetime.utcnow())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(colour=discord.Colour.red(), title="❌ Wrong Syntax",
                                  description=f"Dein Betrag muss eine Zahl sein. Beispiel: **{ctx.prefix}clear {random.randint(1, 300)}**")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return

    @commands.command(usage="<title> [description]")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(manage_messages=True)
    async def embedfy(self, ctx, title=None, *, description=None):
        """Der Bot zeigt deine Nachricht in einer Einbettung an."""
        if title is None:
            await get_syntax(ctx)
            return
        else:
            await ctx.message.delete()
            embed = discord.Embed(colour=discord.Colour.green(), title=f"{title}",
                                  description=f"{description if description else 'Kein Text angegeben'}")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            embed.set_thumbnail(url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return

    @commands.command(usage="<role> <user/ID>")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, role: discord.Role = None, user: discord.Member = None):
        """Auf diese Weise können Sie Rollen zu einem Benutzer hinzufügen und entfernen."""
        if role is None or user is None:
            await get_syntax(ctx)
            return
        if role not in user.roles:
            try:
                embed = discord.Embed(colour=discord.Colour.green(),
                                      description=f"{role.mention} wurde hinzugefügt {user.mention}.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await user.add_roles(role)
                await ctx.send(embed=embed)
                return
            except:
                embed = discord.Embed(colour=discord.Colour.red(),
                                      description=f"Leider habe ich dazu keine Berechtigung.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

        if role in user.roles:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f"{role.mention} wurde entfernt von {user.mention}.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await user.remove_roles(role)
            await ctx.send(embed=embed)
            return

    @commands.command(usage="<user/ID> <reason>")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def mute(self, ctx, user: discord.Member = None, *, reason=None):
        """Schaltet einen Benutzer stumm, bis die Stummschaltung aufgehoben wird."""
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="Muted")

        if user is None or reason is None:
            await get_syntax(ctx)
            return
        elif user.guild_permissions.manage_roles:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f"{user.mention} kann nicht stumm geschaltet werden, da er die Rechte **Rollen verwalten** hat.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return

        if not role:
            role = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=False,
                                              read_messages=False)

        if role in user.roles:
            embed = discord.Embed(colour=discord.Colour.red(), description=f"{user.mention} ist bereits gestummt.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return

        if role not in user.roles:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f"Der Benutzer {user.mention} (**{user.id}**) wurde gestummt.")
            embed.add_field(name=f"🎛️ Server:", value=f"{ctx.guild.name}", inline=False)
            embed.add_field(name=f"👮 Moderator:", value=f"{ctx.author} (**{ctx.author.id}**)", inline=False)
            embed.add_field(name=f"📄 Grund:", value=f"{reason}", inline=False)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

            dm = discord.Embed(colour=discord.Colour.red(),
                               description=f"Hey {user.mention}! \nDu wurdest auf dem Server **{ctx.guild.name}** stummgeschaltet! Genauere Informationen hier:")
            dm.add_field(name=f"🎛️ Server:", value=f"{ctx.guild.name}", inline=False)
            dm.add_field(name=f"👮 Moderator:", value=f"{ctx.author.mention}", inline=False)
            dm.add_field(name=f"📄 Grund:", value=f"{reason}", inline=False)
            dm.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            for channel in guild.channels:
                await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=False)
            try:
                await user.send(embed=dm)
                await user.add_roles(role, reason=reason)
                await ctx.send(embed=embed)
            except:
                try:
                    await user.add_roles(role, reason=reason)
                    await ctx.send(embed=embed)
                    await ctx.send("Ich konnte die Nachricht nicht an den Benutzer senden.")
                except:
                    embedr = discord.Embed(colour=discord.Colour.red(),
                                           description=f"Leider habe ich dazu keine Berechtigung. Die stumme Rolle muss unter der **Vulpo**-Rolle liegen.")
                    embedr.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    await ctx.send(embed=embedr)
                    return

    @commands.command(usage="<user/ID>")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def unmute(self, ctx, user: discord.Member = None):
        """Die Stummschaltung eines stummgeschalteten Benutzers wird aufgehoben."""
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild
        if user is None:
            await get_syntax(ctx)
            return
        if not role:
            role = await guild.create_role(name="Muted", send_messages=False, read_message_history=False)
            for channel in guild.channels:
                await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=False)

        if role not in user.roles:
            embed = discord.Embed(colour=discord.Colour.red(), description=f"{user.mention} ist überhaupt nicht stummgeschaltet.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        if role in user.roles:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f"Der Benutzer {user.mention} (**{user.id}**) wurde entstummt.")
            embed.add_field(name=f"🎛️ Server:", value=f"{ctx.guild.name}", inline=False)
            embed.add_field(name=f"👮 Moderator:", value=f"{ctx.author} (**{ctx.author.id}**)", inline=False)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

            dm = discord.Embed(colour=discord.Colour.red(),
                               description=f"Hey {user.mention}! \nDu wurdest auf dem Server **{ctx.guild.name}** entstummt! Genauere Informationen hier:")
            dm.add_field(name=f"🎛️ Server:", value=f"{ctx.guild.name}", inline=False)
            dm.add_field(name=f"👮 Moderator:", value=f"{ctx.author.mention}", inline=False)
            dm.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            try:
                await user.remove_roles(role)
                await user.send(embed=dm)
                embed = discord.Embed(colour=discord.Colour.green(), description=f"{user.mention} wurde entstummt.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return
            except:
                embed = discord.Embed(colour=discord.Colour.red(),
                                      description=f"Leider habe ich dazu keine Berechtigung. Die stumme Rolle muss unter meiner Rolle liegen.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

    @commands.command(usage="<user/ID> <reason>", aliases=['w'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def warn(self, ctx, user: discord.User = None, *, reason: str = None):
        """Warnt einen Benutzer. Wenn möglich."""
        if user is None or reason is None:
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
            cursor.execute("SELECT warnID FROM warns WHERE userID = (%s) AND guildID = (%s)", (user.id, ctx.guild.id))
            result = cursor.fetchall()
            if result is None:
                cursor.execute("INSERT INTO warns(guildID, userID, grund, warnID) VALUES(%s, %s, %s, %s)", (ctx.guild.id, user.id, reason + f"\n`Verwarnung erstellt am {discord.utils.utcnow().__format__('%d.%m.%Y')}`", 1))
            if result != None:
                warnID = 1
                for warn in result:
                    warnID += 1
                await asyncio.sleep(1)
                cursor.execute("INSERT INTO warns(guildID, userID, grund, warnID) VALUES(%s, %s, %s, %s)", (ctx.guild.id, user.id, reason + f"\n`Verwarnung erstellt am {discord.utils.utcnow().__format__('%d.%m.%Y')}`", warnID))
            embed = discord.Embed(colour=discord.Colour.gold(),
                                  description=f"Der Benutzer {user} (**{user.id}**) wurde verwarnt.")
            embed.add_field(name=f"🎛 Server:", value=f"{ctx.guild.name}", inline=False)
            embed.add_field(name=f"👮 Moderator:", value=f"{ctx.author} (**{ctx.author.id}**)", inline=False)
            embed.add_field(name=f"📄 Grund:", value=f"{reason}", inline=False)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

            dm = discord.Embed(colour=discord.Colour.gold(),
                               description=f"Hey {user.mention}! \nDu wurdest auf dem Server **{ctx.guild.name}** verwarnt! Genauere Informationen hier:")
            dm.add_field(name=f"🎛 Server:", value=f"{ctx.guild.name}", inline=False)
            dm.add_field(name=f"👮 Moderator:", value=f"{ctx.author.mention}", inline=False)
            dm.add_field(name=f"📄 Grund:", value=f"{reason}", inline=False)
            dm.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            try:
                await user.send(embed=dm)
                await ctx.send(embed=embed)
            except:
                await ctx.send(embed=embed)
                await ctx.send("Ich konnte die Nachricht nicht an den Benutzer senden.")
        mydb.commit()
        mydb.close()

    @commands.command(usage="<user/ID> <warnID>", aliases=['uw'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def unwarn(self, ctx, user: discord.User = None, warnID: str = None):
        """Entwarnt einen Benutzer. Wenn möglich."""
        if user is None or warnID is None:
            await get_syntax(ctx)
            return

        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT grund FROM warns WHERE guildID = (%s) AND userID = (%s) AND warnID = (%s)", (ctx.guild.id, user.id, warnID))
        result = cursor.fetchone()
        if result is None:
            await ctx.send(f"Die Verwarnung mit der ID {warnID} von {user} wurde nicht gefunden.")
            return
        cursor.execute("DELETE FROM warns WHERE userID = (%s) AND guildID = (%s) AND warnID = (%s)", (user.id, ctx.guild.id, warnID))
        embed = discord.Embed(colour=discord.Colour.gold(),
                                description=f"Die Verwarnung mit der ID {warnID} von {user} (**{user.id}**) wurde entfernt.")
        embed.add_field(name=f"🎛️ Server:", value=f"{ctx.guild.name}", inline=False)
        embed.add_field(name=f"👮 Moderator:", value=f"{ctx.author} (**{ctx.author.id}**)", inline=False)
        embed.add_field(name=f"📄 Verwarnung:", value=f"{result[0]}", inline=False)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        mydb.commit()
        mydb.close()

    @commands.command(usage="<user/ID>", aliases=['lw'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def listwarns(self, ctx, user: discord.User = None):
        """Bekomme eine Liste an Warns eines bestimmten Benutzers."""
        if user is None:
            await get_syntax(ctx)
            return

        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT grund, warnID FROM warns WHERE guildID = (%s) AND userID = (%s)", (ctx.guild.id, user.id))
        result = cursor.fetchall()
        if result is None:
            await ctx.send(f"Der User {user} hat keine Verwarnungen hier.")
            return
        warnembed = discord.Embed(colour=discord.Colour.gold(), description=f"Alle Verwarnungen von {user} (**{user.id}**).")
        warnembed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        a = 0
        for warn in result:
            a += 1
            warnembed.add_field(name=f"Verwarnung {warn[1]}", value=f"{warn[0]}", inline=False)
        if a != 0:
            await ctx.send(embed=warnembed)
        if a == 0:
            await ctx.send(f"Der User {user} hat keine Verwarnungen hier.")
        mydb.commit()
        mydb.close()

    @commands.command(usage="[channel/ID]")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        """Sperrt einen Kanal, damit nicht jeder Nachrichten senden kann."""
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        f = discord.Embed(colour=discord.Color.red(),
                          description="Dieser Kanal wurde gesperrt. **Du bist jetzt stummgeschaltet!**")
        f.set_author(name="Kanal gesperrt", icon_url=ctx.author.avatar)
        f.set_footer(text=f"Gesperrt von {ctx.author}")
        await channel.send(embed=f)

    @commands.command(usage="[channel/ID]")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        """Schaltet einen Kanal frei, damit jeder Nachrichten senden kann."""
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        f = discord.Embed(colour=discord.Color.green(),
                          description="Dieser Kanal wurde freigeschaltet. **Du bist jetzt nicht stummgeschaltet!**")
        f.set_author(name="Kanal freigeschaltet", icon_url=ctx.author.avatar)
        f.set_footer(text=f"Freigeschaltet von {ctx.author}")
        await channel.send(embed=f)

    @commands.command(aliases=['archive'], usage="<messages>")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.channel)
    async def log(self, ctx, *limit: int):
        """Erstellt eine Datei über einen Textchat."""
        if not limit:
            limit = 10
        else:
            limit = limit[0]
        logFile = f'{ctx.channel}.log'
        counter = 0
        with open(logFile, 'w', encoding='UTF-8') as f:
            f.write(
                f'Nachrichten vom Kanal: {ctx.channel} um {ctx.message.created_at.strftime("%d.%m.%Y %H:%M:%S")}\n')
            async for message in ctx.channel.history(limit=limit, before=ctx.message):
                try:
                    attachment = '[File:: {}]'.format(message.attachments[0].url)
                except IndexError:
                    attachment = ''
                f.write(
                    '{} {!s:20s}: {} {}\r\n'.format(message.created_at.strftime('%d.%m.%Y %H:%M:%S'), message.author,
                                                    message.clean_content, attachment))
                counter += 1
        msg = f':ok: {counter} Nachrichten wurden gespeichert!'
        f = discord.File(logFile)
        await ctx.send(file=f, content=msg)
        os.remove(logFile)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        
        self.snipe_message_author[message.guild.id] = message.author
        self.snipe_message_content[message.guild.id] = message.content
        self.snipe_message_channel[message.guild.id] = message.channel

    @commands.command(aliases=['snip'])
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.channel)
    async def snipe(self, ctx):
        """Zeigt die letzte gelöschte Nachricht vom Server an."""
        try:
            channels = self.snipe_message_channel[ctx.guild.id]
            em = discord.Embed(color=discord.Color.dark_green(), title=f"Gelöschte Nachricht",
                               description=f"Kanal: *#{channels.name}*\nAuthor: *{self.snipe_message_author[ctx.guild.id]}*")
            em.add_field(name=f"Nachricht", value=f"**{self.snipe_message_content[ctx.guild.id]}**")
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=em)
        except:
            em = discord.Embed(color=discord.Color.dark_green(),
                               description=f"Es sind keine kürzlich gelöschten Nachrichten vorhanden.")
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=em)
            return


async def setup(bot):
    await bot.add_cog(moderation(bot))