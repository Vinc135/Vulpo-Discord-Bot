from datetime import datetime
import discord
from discord.ext import commands
import typing
import aiohttp
import random
import asyncio
from info import get_syntax
##########

class meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "b490a86c0b800ef278846f71592953f4"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"

    @commands.command()
    async def invites(self, ctx, member: discord.User=None):
        """Finde heraus wieveiele Leute du schon eingeladen hast."""
        if member == None:
            member = ctx.author
        totalInvites = 0
        for invite in await ctx.guild.invites():
            if invite.inviter == member:
                totalInvites += invite.uses
        
        embed=discord.Embed(description=f"Das Mitglied {member.mention} hat insgesammt __**{totalInvites} Mitglied{'er' if totalInvites >= 2 else ''}**__ zum Server eingeladen!", color=discord.Color.orange())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        embed.set_footer(text="Diese Zahl basiert auf allen Invites, seitdem du auf dem Server bist.", icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")

        await ctx.send(embed=embed)

    @commands.command(usage="[user/ID]", aliases=["pb", "av"])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def avatar(self, ctx, user: discord.Member = None):
        """Zeigt das Profilbild eines Benutzers an."""
        if user is None:
            user = ctx.author
        embed = discord.Embed(colour=discord.Colour.green(), description=f"Profilbild von {user}")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        embed.set_image(url=user.avatar)
        await ctx.send(embed=embed)

    @commands.command(usage="<question>", aliases=['umfrage'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, *, question=None):
        """Zeigt deine Frage mit Reaktionen auf die Nachricht."""
        if question is None:
            await get_syntax(ctx)
            return
        else:
            author = ctx.author
            embed = discord.Embed(color=discord.Colour.green())
            embed.add_field(name=f'Umfrage von {author}', value=f'{question}', inline=False)

            await ctx.message.delete()
            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")

    @commands.command(usage="[channel/ID]", aliases=["ci", ])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def channelinfo(self, ctx, *, channels: typing.Union[discord.TextChannel, discord.VoiceChannel] = None):
        """Zeigt viele Informationen von einem Kanal an."""
        if channels is None:
            channels = ctx.channel
        if isinstance(channels, discord.TextChannel):
            channel = channels
            embed = discord.Embed(colour=discord.Color.green())
            embed.add_field(name=f"🆔 ID", value=f"{channel.id}", inline=False)
            embed.add_field(name="⚙️ Erstellt", value=f"{channel.created_at.__format__('am %d.%m.%Y at %X')}",
                            inline=False)
            embed.add_field(name="🗂 Kategorie",
                            value=f"{channel.category.name if channel.category.name else 'Keine Kategorie'}",
                            inline=False)
            embed.add_field(name="🖌 Beschreibung", value=f"{channel.topic if channel.topic else 'keine Beschreibung'}",
                            inline=False)
            embed.add_field(name="🔢 Position", value=f"{channel.position}",
                            inline=False)
            embed.set_author(name=f"Kanal info {channel.name}", icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        if isinstance(channels, discord.VoiceChannel):
            channel = channels
            embed = discord.Embed(colour=discord.Color.green())
            embed.add_field(name=f"🆔 ID", value=f"{channel.id}", inline=False)
            embed.add_field(name="⏱️ Erstellt", value=f"{channel.created_at.__format__('am %d.%m.%Y %X')}", inline=False)
            embed.add_field(name="🗂 Kategorie",
                            value=f"{channel.category.name if channel.category.name else 'Keine Kategorie'}",
                            inline=False)
            embed.add_field(name=f"📊 Limit", value=f"{channel.user_limit}", inline=False)
            embed.add_field(name=f"🔊 Bitrate", value=f"{channel.bitrate/1000} kbps", inline=False)
            embed.set_author(name=f"Kanal info {channel.name}", icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
    
    @commands.command(usage="[user/ID]", aliases=["ui", "whois"])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def userinfo(self, ctx, user: discord.Member = None):
        """Zeigt viele Informationen von einem Benutzer an."""
        if user is None:
            user = ctx.author

        embed = discord.Embed(colour=user.color, timestamp=datetime.utcnow())
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="📰 Profil", value=f"{user.display_name}", inline=False)
        embed.add_field(name="🆔 ID", value=f"{user.id}", inline=False)
        embed.add_field(name="⏱ Erstellt", value=f"{user.created_at.__format__('am %d.%m.%Y %X')}", inline=False)
        embed.add_field(name="➡️ Beigetreten am", value=f"{user.joined_at.__format__('am %d.%m.%Y %X')}", inline=False)
        embed.add_field(name="👑 Höchte Rolle", value=f"{user.top_role}", inline=False)
        embed.add_field(name="🤖 Bot", value=f"{user.bot if user.bot else 'Kein Bot'}", inline=False)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
    
    @commands.command(liases=["si", "server"])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def serverinfo(self, ctx):
        """Zeigt viele Informationen von einem Server an."""
        guild = ctx.author.guild
        embed = discord.Embed(colour=discord.Colour.green(), timestamp=datetime.utcnow())
        embed.add_field(name="🆔 ID", value=f"{guild.id}", inline=False)
        embed.add_field(name="⏱ Erstellt", value=f"{guild.created_at.__format__('am %d.%m.%Y %X')}", inline=False)
        embed.add_field(name="👑 Owner", value=f"{guild.owner}", inline=False)
        embed.add_field(name="💜 Boost status", value=f"Level: {guild.premium_tier}\nBooster: {guild.premium_subscription_count if guild.premium_subscription_count else 'Keine Booster'}", inline=False)
        embed.add_field(name=f"👥 Mitglieder",
                        value=f"Alle: {guild.member_count}\nOnline: {len([i for i in guild.members if str(i.status) == 'online'])}\nAbwesend: {len([i for i in guild.members if str(i.status) == 'idle'])}\nDnD: {len([i for i in guild.members if str(i.status) == 'dnd'])}\nOffline: {len([i for i in guild.members if str(i.status) == 'offline'])}", inline=False)
        embed.set_thumbnail(url=guild.icon)
        embed.set_author(name=f"Serverinfo {guild.name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command(aliases=["guildicon"])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def servericon(self, ctx):
        """Zeigt das Profilbild vom Server an."""
        guild = ctx.author.guild
        embed = discord.Embed(colour=discord.Colour.green(), description=f"Serverbild von {guild.name}")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        embed.set_image(url=guild.icon)
        await ctx.send(embed=embed)
     
    @commands.command(usage="<role/ID>", aliases=['ri'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def roleinfo(self, ctx, *, role: discord.Role = None):
        """Sendet eine Rolleninfo."""
        if role is None:
            await get_syntax(ctx)
            return
        else:
            guild = ctx.guild
            embed = discord.Embed(color=role.color, description=f"ℹ️ Rollen info für {role.name}",timestamp=datetime.utcnow())
            embed.add_field(name=f"🆔 ID", value=f"{role.id}", inline=False)
            embed.add_field(name="⏱ Erstellt", value=f"{role.created_at.__format__('am %d.%m.%Y %X')}",inline=False)
            a = role.color.value
            embed.add_field(name="🖌 Farbcode (HEX)", value=f'{a:x}', inline=False)
            embed.add_field(name="👥 Benutzer mit der Rolle",
                            value=f"{len(role.members)} von {guild.member_count} Mitgliedern", inline=False)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

    @commands.command(usage="<city>", aliases=['wetter'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def weather(self, ctx, *, city=None):
        """Zeigt das Wetter einer Stadt an."""
        if city is None:
            await get_syntax(ctx)
            return
        else:
            try:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(
                            f"https://api.openweathermap.org/data/2.5/weather?appid=bf254c2299576dc022583728cfaf7971&q=" + city.replace(
                                " ", "+")) as r:
                        data = await r.json()
                        icon = data['weather'][0]['icon']
                        embed = discord.Embed(colour=discord.Colour.green(), title=f"Weather",
                                              description=f"Mal gucken...")
                        embed.add_field(name=f"🗽 Location", value=f"{data['name']}")
                        embed.add_field(name=f"☁️ Wetter", value=f"{data['weather'][0]['main']} - {data['weather'][0]['description']}", inline=False)
                        embed.add_field(name=f"🔥 Temperatur", value=f"{int((float(data['main']['temp']))) - 273}°C")
                        embed.add_field(name=f"👆 Fühlt sich an wie", value=f"{int((float(data['main']['feels_like']))) - 273}°C")
                        embed.add_field(name=f"💧 Luftfeuchtigkeit", value=f"{int((float(data['main']['humidity'])))}%", inline=False)
                        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                        embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{icon}@2x.png")
                        await ctx.send(embed=embed)
            except:
                embed = discord.Embed(colour=discord.Colour.red(),
                                      description=f"Stadt **{city}** nicht gefunden")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
                return

    @commands.command(usage="", aliases=["perms","permission"])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def permissions(self, ctx, user: discord.Member=None):
        """Listet alle Berechtigungen von jemandem auf."""
        if user is None:
            permissions = ctx.channel.permissions_for(ctx.author)
            user = ctx.author
        permissions = ctx.channel.permissions_for(user)
        embed = discord.Embed(title=f':customs:  Berechtigungen von {user}', color=discord.Color.blue())
        embed.add_field(name='Server', value=ctx.guild)
        embed.add_field(name='Kanal', value=ctx.channel, inline=False)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

        for item, valueBool in permissions:
            if valueBool == True:
                value = ':white_check_mark:'
            else:
                value = ':x:'
            embed.add_field(name=item, value=value)

        await ctx.send(embed=embed)

    @commands.command(aliases=['geturl'], usage="<emoji>")
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def emojiurl(self, ctx, emoji: discord.PartialEmoji=None):
        """Gibt den Link für ein Emoji."""
        if emoji is None:
            await get_syntax(ctx)
            return
        else:
            embed = discord.Embed(colour=discord.Colour.green(),
                                  description=f"Hier der Link: {emoji.url}")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            embed.set_image(url=f"{emoji.url}")
            await ctx.send(embed=embed)

    @commands.command(aliases=['se'], usage="<emoji> <name>")
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def stealemoji(self, ctx, emoji: discord.PartialEmoji=None, *, name=None):
        """Erstelle das selbe Emoji, wie es ein anderer Server hat, für deinen Server."""
        if emoji == None or name == None:
            await get_syntax(ctx)
            return
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(emoji.url) as response:
                    image_bytes = await response.read()
                    emo = await ctx.guild.create_custom_emoji(name=name, image=image_bytes, reason="stealemoji command")
            embed = discord.Embed(colour=discord.Colour.green(),
                                  description=f"**Der Emoji {emo} wurde erstellt.**\nName: {name}")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            embed.set_image(url=f"{emoji.url}")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx):
        """Etwas ankündigen."""
        questions = ["In welchem Kanal soll es angekündigt werden? (Schreibe cancel zum Abbrechen)", "Welche Rolle soll gepingt werden? (Sende die genaue __Rollen-ID__, sende 0 für keine Rolle)(Schreibe cancel zum Abbrechen)", "Sende den Inhalt der Ankündigung!(Schreibe cancel zum Abbrechen)"]

        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            msg11 = await ctx.send(i)

            try:
                msg = await self.bot.wait_for('message', timeout=180, check=check)
                if msg.content == "cancel":
                    await ctx.send("Erolgreich abgebrochen")
                    return
            except asyncio.TimeoutError:
                await ctx.send("❌ Du hast die Fragen nicht in der vorgegebenen Zeit beantwortet. Sei beim nächstem Mal schneller!")
                return
            else:
                await msg11.delete()
                await msg.delete()
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"❌ Du hast keinen Kanal erwähnt. Mach es beim nächstem Mal so wie: {ctx.channel.mention}")
            return
        try:
            if answers[1] == "0":
                text = "**Ankündigung**"
            else:
                r_id = int(answers[1])
                role = discord.utils.get(ctx.guild.roles, id=r_id)
                
                def function(role, roleid):
                    if role == "@everyone":
                        return("@everyone")
                    if role == "@@everyone":
                        return("@everyone")
                    if role == "everyone":
                        return("@everyone")
                    else:
                        return(f"<@&{roleid}>")
                
                text = f"**Ankündigung** {function(role.name, role.id)}"
        except:
            await ctx.send("❌ Rolle nicht gefunden.")
            return
        inhalt = answers[2]
        channel = self.bot.get_channel(c_id)

        try:
            embed = discord.Embed(title="**Ankündigung!**",description=inhalt,colour=discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))
            embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon)
            embed.set_thumbnail(url=ctx.guild.icon)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await channel.send(text, embed=embed)
            await ctx.send("✅")
        except:
            await ctx.send("❌")
            return

async def setup(bot):
    await bot.add_cog(meta(bot))