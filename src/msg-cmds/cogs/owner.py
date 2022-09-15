import discord
from discord.ext import commands
import asyncio
import sys
from info import get_syntax
import mysql.connector

setstatus_aliases = ["s", ]
online_aliase = ["o", ]
idle_aliase = ["i", ]
dnd_aliase = ["dnd", ]

playing_aliases = ["p", ]
listening_aliases = ["l", ]
watching_aliases = ["w", ]

class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def get_user(self, ctx, user: discord.User):
        await ctx.send(user.created_at.__format__('am %d.%m.%Y %X'))

    @commands.group(invoke_without_command=True, name="status", aliases=setstatus_aliases)
    @commands.is_owner()
    async def _status(self, ctx):
        """Ändere den Status."""
        pass

    ### Online ###
    @_status.group(invoke_without_command=True, name="online", aliases=online_aliase)
    @commands.is_owner()
    async def _status_online(self, ctx):
        """Stelle den Status auf Online."""
        await self.bot.change_presence(status=discord.Status.online, activity=None)
        embed = discord.Embed(color=discord.Color.red(),
                              description=f"__**Bot Status**__\n🟢Online")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return
    
    @_status_online.command(name="playing", aliases=playing_aliases, usage="<text>")
    @commands.is_owner()
    async def _status_online_playing(self, ctx, *, Text: str=None):
        """Stelle den Status zu Online: Spielt..."""
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(type=discord.ActivityType.playing, name=Text))
        embed = discord.Embed(color=discord.Color.red(),
                              description=f"__**Bot Status**__\n🟢Online\n\n__**Text:**__\n**Spielt** {Text}")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return
    
    @_status_online.command(name="listening", aliases=listening_aliases, usage="<text>")
    @commands.is_owner()
    async def _status_online_listening(self, ctx, *, Text: str=None):
        """Stelle den Status zu Online: Hört ... zu."""
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(type=discord.ActivityType.listening, name=Text))
        embed = discord.Embed(color=discord.Color.red(),
                              description=f"__**Bot Status**__\n🟢Online\n\n__**Text:**__\n**Hört** {Text} **zu**.")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return
    
    @_status_online.command(name="watching", aliases=watching_aliases, usage="<text>")
    @commands.is_owner()
    async def _status_online_watching(self, ctx, *, Text: str=None):
        """Stelle den Status zu Online: Schaut ..."""
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(type=discord.ActivityType.watching, name=Text))
        embed = discord.Embed(color=discord.Color.red(),
                              description=f"__**Bot Status**__\n🟢Online\n\n__**Text:**__\n**Schaut** {Text}")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return

    ### Idle ###
    @_status.group(invoke_without_command=True, name="idle", aliases=["i"], usage="")
    @commands.is_owner()
    async def _status_idle(self, ctx):
        """Setzt den Status auf Abwesend."""
        await self.bot.change_presence(status=discord.Status.idle, activity=None)
        embed = discord.Embed(color=discord.Color.red(),
                              description=f"__**Bot Status**__\n🌙Abwesend")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return
    
    @_status_idle.command(name="playing", aliases=playing_aliases, usage="<text>")
    @commands.is_owner()
    async def _status_idle_playing(self, ctx, *, Text: str=None):
        """Setzt den Status auf Abwesend: Spielt..."""
        await self.bot.change_presence(status=discord.Status.idle,
                                       activity=discord.Activity(type=discord.ActivityType.playing, name=Text))
        embed = discord.Embed(color=discord.Color.red(),
                              description=f"__**Bot Status**__\n🌙Abwesend\n\n__**Text:**__\n**Spielt** {Text}")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return
    
    @_status_idle.command(name="listening", aliases=listening_aliases, usage="<text>")
    @commands.is_owner()
    async def _status_idle_listening(self, ctx, *, Text: str=None):
        """Setze den Status auf Abwesend: Hört... zu."""
        await self.bot.change_presence(status=discord.Status.idle,
                                       activity=discord.Activity(type=discord.ActivityType.listening, name=Text))
        embed = discord.Embed(color=discord.Color.red(),
                              description=f"__**Bot Status**__\n🌙Abwesend\n\n__**Text:**__\n**Hört** {Text} **zu**.")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return
    
    @_status_idle.command(name="watching", aliases=watching_aliases, usage="<text>")
    @commands.is_owner()
    async def _status_idle_looking(self, ctx, *, Text: str=None):
        """Setze den Status auf Abwesend: Schaut ..."""
        await self.bot.change_presence(status=discord.Status.idle,
                                       activity=discord.Activity(type=discord.ActivityType.watching, name=Text))
        embed = discord.Embed(color=discord.Color.red(),
                              description=f"__**Bot Status**__\n🌙Abwesend\n\n__**Text:**__\n**Schaut** {Text}")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return

    ### DnD ###
    @_status.group(invoke_without_command=True, name="dnd", aliases=["d"])
    @commands.is_owner()
    async def _status_dnd(self, ctx):
        """Den Status auf Nicht stören setzen."""
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=None)
        embed = discord.Embed(color=discord.Color.red(),
                              description=f"__**Bot Status**__\n⛔️Nicht stören")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return
    
    @_status_dnd.command(name="playing", aliases=playing_aliases, usage="<text>")
    @commands.is_owner()
    async def _status_dnd_playing(self, ctx, *, Text: str=None):
        """Setzt den Status auf Nicht stören: Spielt..."""
        await self.bot.change_presence(status=discord.Status.do_not_disturb,
                                       activity=discord.Activity(type=discord.ActivityType.playing, name=Text))
        embed = discord.Embed(color=discord.Color.red(),
                              description=f"__**Bot Status**__\n⛔️Nicht stören\n\n__**Text:**__\n**Spielt** {Text}")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return

    @_status_dnd.command(name="listening", aliases=listening_aliases, usage="<text>")
    @commands.is_owner()
    async def _status_dnd_listening(self, ctx, *, Text: str=None):
        """Setzt den Status auf Nicht stören: Hört... zu."""
        await self.bot.change_presence(status=discord.Status.do_not_disturb,
                                       activity=discord.Activity(type=discord.ActivityType.listening, name=Text))
        embed = discord.Embed(color=discord.Color.red(),
                              description=f"__**Bot Status**__\n⛔️Nicht stören\n\n__**Text:**__\n**Hört** {Text} **zu**.")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return
    
    @_status_dnd.command(name="watching", aliases=watching_aliases, usage="<text>")
    @commands.is_owner()
    async def _status_dnd_watching(self, ctx, *, Text: str=None):
        """Setzt den Status auf Nicht stören: Schaut..."""
        await self.bot.change_presence(status=discord.Status.do_not_disturb,
                                       activity=discord.Activity(type=discord.ActivityType.watching, name=Text))
        embed = discord.Embed(color=discord.Color.red(),
                              description=f"__**Bot Status**__\n⛔️Nicht stören\n\n__**Text:**__\n**Schaut** {Text}")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return
    
    @commands.command(usage="<Benutzer/ID> <Nachricht>")
    @commands.is_owner()
    @commands.guild_only()
    async def dm(self, ctx, user: discord.User=None, *, message=None):
        """Sendet eine Nachricht an den DM eines Benutzers."""
        if user is None or message is None:
            await get_syntax(ctx)
            return
        try:
            dm = discord.Embed(color=discord.Color.orange(), title="Hey!",description=f"Eine neue Nachricht von **{ctx.guild}**")
            dm.add_field(name=f"Nachricht", value=f"{message}", inline=False)
            dm.set_footer(text=f"Keine Antwort möglich!")

            embed = discord.Embed(color=discord.Color.orange(), description=f"Ich habe **{message}** an {user.mention} geschickt.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await user.send(embed=dm)
            await ctx.send(embed=embed)
            return
        except:
            embed2 = discord.Embed(description=f"❌ Die Nachricht konnte nicht an {user} zugestellt werden. Dies geschieht in der Regel, weil der Bot keinen gemeinsamen Server mit dem Empfänger hat, Direktnachrichten auf diesem Server deaktiviert sind oder der Empfänger nur Direktnachrichten von Freunden annimmt. ",
                                  color=discord.Color.red())
            embed2.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed2)
            return

    @commands.command(usage="<serverId>")
    @commands.is_owner()
    @commands.guild_only()
    async def gleave(self, ctx, id=None):
        """Verlässt einen bestimmten Server."""
        if id is None:
            await get_syntax(ctx)
            return
        else:
            try:
                guild = self.bot.get_guild(int(id))
                embed = discord.Embed(
                    description=f"Soll ich wirklich den Server {guild.name} mit {guild.member_count} Mitgliedern verlassen?",
                    color=discord.Color.orange())
                embed.set_author(name=ctx.author, icon_url=ctx.me.avatar)
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return str(reaction.emoji) in ['✅', '❌'] and user == ctx.message.author

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=10)
                    if str(reaction.emoji) == '✅':
                        await message.clear_reactions()
                        embed1 = discord.Embed(description=f"Ich habe den Server {guild.name} verlassen.",
                                              color=discord.Color.orange())
                        embed1.set_author(name=ctx.author, icon_url=ctx.me.avatar)
                        Gilde = self.bot.get_guild(int(id))
                        await Gilde.verlassen()
                        await message.edit(embed=embed1)

                    if str(reaction.emoji) == '❌':
                        await message.clear_reactions()
                        embed2 = discord.Embed(description=f"Ich habe den Server {guild.name} nicht verlassen.",
                                              color=discord.Color.orange())
                        embed2.set_author(name=ctx.author, icon_url=ctx.me.avatar)
                        await message.edit(embed=embed2)

                except asyncio.TimeoutError:
                    await message.clear_reactions()
                    embed3 = discord.Embed(description=f"Ich habe den Server {guild.name} nicht verlassen, weil du nicht antwortest.",
                                          color=discord.Color.orange())
                    embed3.set_author(name=ctx.author, icon_url=ctx.me.avatar)
                    await message.edit(embed=embed3)
            except:
                embed = discord.Embed(
                    description=f"Ich konnte keinen Server mit der ID {id} finden.",
                    color=discord.Color.orange())
                embed.set_author(name=ctx.author, icon_url=ctx.me.avatar)
                await ctx.send(embed=embed)
                return
            
    @commands.command(aliases=["servers"])
    @commands.is_owner()
    @commands.guild_only()
    async def serverlist(self, ctx):
        activeservers = self.bot.guilds
        i = 1
        test = "\n".join(f"**{i + 1}** {guild.name}({guild.member_count}) — {guild.id}" for i, guild in enumerate(activeservers))
        try:
            for chunk in [test[i : i + 2000] for i in range(0, len(test), 2000)]:
                embed = discord.Embed(title="Liste von Servern, wo der Bot drin ist", description=chunk, color=0x3498db)
                embed.set_author(name=ctx.author, icon_url=ctx.me.avatar)
                await ctx.send("**Nummer** **Servername(Member) — Serverid**", embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(title="Liste von Servern, wo der Bot drin ist", description=chunk, color=0x3498db)
            embed.set_author(name=ctx.author, icon_url=ctx.me.avatar)
            await ctx.send(embed=embed)
            
    @commands.command(usage="[command]", aliases=["disabled"])
    @commands.is_owner()
    @commands.guild_only()
    async def disable(self, ctx, *, command=None):
        """Deaktiviere einen Command oder lass dir über alle eine Liste senden."""
        if command is None:
            liste = "Alle deaktivierten Commands:"
            i = 0
            for cmd in self.bot.commands:
                if not cmd.enabled:
                    i += 1
                    liste += f"\n**{i}**. {cmd.name}"
            if i == 0:
                liste = "Keine Commands sind zurzeit deaktiviert."
            await ctx.send(liste)
            return

        elif ctx.command == command:
            command = self.bot.get_command(command)
            embed = discord.Embed(colour=discord.Colour.red(), title="❌ Wrong argument",
                                    description=f"Ich konnte den Command **{command}** nicht deaktivieren.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        else:
            command = self.bot.get_command(command)
            command.enabled = not command.enabled
            x = 'aktiviert' if command.enabled else 'deaktiviert'
            embed = discord.Embed(colour=discord.Colour.green(), title="Erfolg",
                                    description=f"Ich habe den Command **{command}** **{x}**!")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
            
    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def ownerhelp(self, ctx):
        embed = discord.Embed(colour=discord.Colour.orange(),
                              description="Benutze ****help [command]**** für eine detaillierte Beschreibung eines Commands.")
        embed.add_field(name="__Status__", value="**status**, **status online**, **status online playing**, **status online watching**, **status online listening**, **status idle playing**, **status idle watching**, **status idle listening**, **status dnd playing**, **status dnd watching**, **status dnd listening**", inline=False)
        embed.add_field(name="__Extensions__",
                        value="**cog load**, **cog reload**, **cog unload**",
                        inline=False)
        embed.add_field(name="__Anderes__",
                        value="**dm**, **gleave**, **serverlist**, **disable**, **ownerhelp**, **shutdown**, **get_user**",
                        inline=False)
        embed.set_footer(text=f"Benutze {ctx.prefix} vor jedem Command")
        embed.set_author(name="Command Menü", icon_url=ctx.me.avatar)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def shutdown(self, ctx):
        """Takes me off."""
        await ctx.send('**:ok:** Tschüss!')
        await self.bot.logout()
        sys.exit(0)

async def setup(bot):
    await bot.add_cog(owner(bot))