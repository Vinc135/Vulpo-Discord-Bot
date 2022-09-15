import discord
from discord.ext import commands
import math
from info import get_syntax

class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        async def send_error(title, description, url, channel, author, avatar):
            embed = discord.Embed(colour=discord.Colour.red(), title=title, description=description)
            embed.set_author(name=author, icon_url=avatar)
            try:
                await channel.send(embed=embed)
            except:
                try:
                    await channel.send("❌ Mir fehlt die Berechtigung 'embed messages'.")
                except:
                    await ctx.message.add_reaction("❌")
        if isinstance(error,commands.MissingPermissions):
            await send_error("Fehlende Berechtigungen", "❌ Du hast nicht die Rechte, diesen Command auszuführen.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.MissingRequiredArgument):
            await get_syntax(ctx)
            return
        if isinstance(error,commands.CommandInvokeError):
            pass
        if isinstance(error,commands.TooManyArguments):
            await send_error("Zu viele Argumente", "❌ Du hast zu viele Argumente gegeben.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.DisabledCommand):
            await send_error("Deaktivierter Command", "❌ Dieser Command ist zurzeit deaktiviert", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.MissingAnyRole):
            await send_error("Fehlende Berechtigungen", "❌ Du brauchst eine bestimmte Rolle um dies zu tun.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.MissingRole):
            await send_error("Fehlende Berechtigungen", "❌ Du brauchst eine bestimmte Rolle um dies zu tun.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error, commands.CommandOnCooldown):

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
                await send_error("Auf Cooldown", f"❌ Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(seconds)}** Sekunden erneut.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
                return
            if math.ceil(error.retry_after) <= 3600:  # minutes
                await send_error("Auf Cooldown", f"❌ Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(minutes)}** Minuten and **{math.ceil(seconds)}** Sekunden.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
                return
            if math.ceil(error.retry_after) <= 86400:  # hours
                await send_error("Auf Cooldown", f"❌ Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(hours)}** Stunden, **{math.ceil(minutes)}** Minuten and **{math.ceil(seconds)}** Sekunden.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
                return
            if math.ceil(error.retry_after) >= 86400:  # days
                await send_error("Auf Cooldown", f"❌ Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(days)}** Tagen, **{math.ceil(hours)}** Stunden, **{math.ceil(minutes)}** Minuten and **{math.ceil(seconds)}** Sekunden.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
                return

        if isinstance(error,commands.BadArgument):
            pass
        if isinstance(error,commands.MessageNotFound):
            await send_error("Nicht gefunden", "❌ Die Nachricht wurde nicht gefunden.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.MemberNotFound):
            await send_error("Nicht gefunden", "❌ Der Member wurde nicht gefunden.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.UserNotFound):
            await send_error("Nicht gefunden", "❌ Der User wurde nicht gefunden.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.ChannelNotFound):
            await send_error("Nicht gefunden", "❌ Der Kanal wurde nicht gefunden.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.ChannelNotReadable):
            await send_error("Missing Access", "❌ Ich kann keine Nachrichten in dem Kanal ansehen.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.BadColourArgument):
            await send_error("Nicht gefunden", "❌ Die Farbe wurde nicht gefunden.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.RoleNotFound):
            await send_error("Nicht gefunden", "❌ Die Rolle wurde nicht gefunden.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.BotMissingPermissions):
            await send_error("Fehlende Berechtigungen", "❌ Ich habe keine Berechtigungen um das zu tun.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.BadInviteArgument):
            pass
        if isinstance(error,commands.EmojiNotFound):
            await send_error("Nicht gefunden", "❌ Ich konnte das Emoji nicht finden oder teile kein Server mit dem Emoji.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.CommandNotFound):
            pass
            return
        if isinstance(error,commands.PrivateMessageOnly):
            await send_error("Kein Zugang", "❌ Dieser Command funktioniert nur in Direktnachrichten.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.NoPrivateMessage):
            await send_error("Kein Zugang", "❌ Dieser Command funktioniert nur in Servern.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.NSFWChannelRequired):
            await send_error("Kein Zugang", "❌ Du kannst diesen Command nur in einem NSFW-Kanal nutzen.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.NotOwner):
            await send_error("Fehlende Berechtigungen", "❌ Nur der Besitzer von Vulpo kann diesen Command ausführen.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        if isinstance(error,commands.BotMissingAnyRole):
            await send_error("Fehlende Berechtigungen", "❌ The Vulpo bot needs a specific role for this.", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            return
        else:
            async def send_error(title, description, url, channel, author, avatar):
                embed = discord.Embed(colour=discord.Colour.red(), title=title, description=description)
                embed.set_author(name=author, icon_url=avatar)
                try:
                    await channel.send(embed=embed)
                except:
                    try:
                        await channel.send("❌ Mir fehlt die Berechtigung 'embed messages'.")
                    except:
                        await error.message.add_reaction("❌")
            await send_error("Unbekannt", "❌ Ein unbekannter Fehler ist aufgetreten.\nBitte öffne ein Ticket im [Supportserver](https://discord.gg/49jD3VXksp)", ctx.me.avatar, ctx.channel, ctx.author, ctx.author.avatar)
            try:
                guilds = self.bot.get_guild(925729625580113951)
                channels = guilds.get_channel(925732898634600458)

                embed = discord.Embed(colour=discord.Colour.red(), title="Unbekannt", description=ctx.message.content)
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                embed.add_field(name="Error", value=f"```py\n{error}```", inline=False)
                embed.set_author(name=f"{ctx.author} | {ctx.author.id}", icon_url=ctx.author.avatar)
                embed.set_footer(text=f"{ctx.guild.name} | {ctx.guild.id}", icon_url=ctx.guild.icon)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/811730903822368833/823531509461942294/2000px-Dialog-error-round.svg.png")

                await channels.send(embed=embed)
                return
            except:
                pass

async def setup(bot):
    await bot.add_cog(error(bot))