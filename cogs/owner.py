import discord
from discord.ext import commands
import asyncio
import sys
from utils.utils import getcolour

class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def cog(self, ctx, arg, name):
        if ctx.author.id == 835782971235368960 or ctx.author.id == 824378909985341451:
            try:
                if arg == "load":
                    cogname = f"cogs.{name}"
                    await self.bot.load_extension(cogname)
                    await ctx.send(f"📥 cogs.{name}")
                if arg == "reload":
                    cogname = f"cogs.{name}"
                    await self.bot.reload_extension(cogname)
                    await ctx.send(f"🔄 cogs.{name}")
                if arg == "unload":
                    cogname = f"cogs.{name}"
                    await self.bot.unload_extension(cogname)
                    await ctx.send(f"📤 cogs.{name}")
            except Exception as e:
                await ctx.send(f"```py\n{e}\n```")

    @commands.command(usage="<Benutzer/ID> <Nachricht>")
    @commands.is_owner()
    @commands.guild_only()
    async def dm(self, ctx, user: discord.User=None, *, message: str):
        """Sendet eine Nachricht an den DM eines Benutzers."""
        try:
            dm = discord.Embed(color=discord.Color.orange(), title="Nachricht aus dem Supportserver!",description=f"Eine neue Nachricht vom Owner des Vulpo Bots.", url="https://discord.gg/49jD3VXksp")
            dm.add_field(name=f"Nachricht", value=f"{message}", inline=False)
            dm.set_footer(text=f"Keine Antwort möglich!")
            await user.send(embed=dm)
            await ctx.send("**<:v_haken:1119579684057907251> Die Nachricht wurde versendet.**")
            return
        except:
            embed2 = discord.Embed(description=f"<:v_kreuz:1119580775411621908> Die Nachricht konnte nicht an {user} zugestellt werden. Dies geschieht in der Regel, weil der Bot keinen gemeinsamen Server mit dem Empfänger hat, Direktnachrichten auf diesem Server deaktiviert sind oder der Empfänger nur Direktnachrichten von Freunden annimmt. ",
                                  color=discord.Color.red())
            embed2.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed2)
            return

    @commands.command(usage="<serverId>")
    @commands.is_owner()
    @commands.guild_only()
    async def gleave(self, ctx, id: int):
        """Verlässt einen bestimmten Server."""
        try:
            guild = self.bot.get_guild(int(id))
            embed = discord.Embed(
                description=f"Soll ich wirklich den Server {guild.name} mit {guild.member_count} Mitgliedern verlassen?",
                color=discord.Color.orange())
            embed.set_author(name=ctx.author, icon_url=ctx.me.avatar)
            message = await ctx.send(embed=embed)
            await message.add_reaction('<:v_haken:1119579684057907251>')
            await message.add_reaction('<:v_kreuz:1119580775411621908>')

            def check(reaction, user):
                return str(reaction.emoji) in ['<:v_haken:1119579684057907251>', '<:v_kreuz:1119580775411621908>'] and user == ctx.message.author

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=10)
                if str(reaction.emoji) == '<:v_haken:1119579684057907251>':
                    await message.clear_reactions()
                    embed1 = discord.Embed(description=f"Ich habe den Server {guild.name} verlassen.",
                                            color=discord.Color.orange())
                    embed1.set_author(name=ctx.author, icon_url=ctx.me.avatar)
                    guild = self.bot.get_guild(int(id))
                    await guild.leave()
                    await message.edit(embed=embed1)

                if str(reaction.emoji) == '<:v_kreuz:1119580775411621908>':
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
            await message.edit(embed=embed)
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
                embed = discord.Embed(title="Liste von Servern, in denen der Bot drin ist", description=chunk, color=0x3498db)
                embed.set_author(name=ctx.author, icon_url=ctx.me.avatar)
                await ctx.send("**Nummer** **Servername(Member) — Serverid**", embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(title="Liste von Servern, in denen der Bot drin ist", description=chunk, color=0x3498db)
            embed.set_author(name=ctx.author, icon_url=ctx.me.avatar)
            await ctx.send(embed=embed)
            
    @commands.command(usage="[command]", aliases=["disabled"])
    @commands.is_owner()
    @commands.guild_only()
    async def disable(self, ctx, *, command: str=None):
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
            embed = discord.Embed(colour=discord.Colour.red(), title="<:v_kreuz:1119580775411621908> Wrong argument",
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
    async def shutdown(self, ctx):
        """Takes me off."""
        await ctx.send('**:ok:** Tschüss!')
        await self.bot.logout()
        sys.exit(0)
        
    @commands.command()
    @commands.is_owner()
    async def servershare(self, ctx, user: discord.User):
        s = "Ich teile folgende Server mit dem Benutzer:"
        for server in self.bot.guilds:
            member = server.get_member(user.id)
            if member:
                s += f"\n{server.name} - {server.id}"
        await ctx.send(s)
        

async def setup(bot):
    await bot.add_cog(owner(bot))