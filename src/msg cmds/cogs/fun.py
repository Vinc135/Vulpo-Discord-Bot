import os
import asyncio
import requests
import io
import aiohttp
import asyncio
import random
import discord
from discord.ext import commands
from datetime import datetime
import aiohttp
from PIL import Image, ImageFilter
from io import BytesIO
from info import get_syntax

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="[user]", aliases=["lr", ])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    async def lostrate(self, ctx, user: discord.Member = None):
        """Berechnet mit einem hochkomplexen Prozess wie Lost der Benutzer ist."""
        if user is None:
            user = ctx.author
        x = random.randint(1, 100)
        embed = discord.Embed(colour=discord.Color.gold(), description=f"{user.mention} is LOST zu {x}%.")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command(usage="[user]")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    async def iq(self, ctx, user: discord.Member = None):
        """Finde heraus, wie hoch der IQ von dir oder einem Benutzer ist."""
        if user is None:
            user = ctx.author
        x = random.randint(14, 230)
        if x < 40:
            iq = "ein ziemlicher Idiot."
        elif x < 80:
            iq = "nicht der Beste in Mathe."
        elif x < 150:
            iq = "ziemlich durchschnittlich."
        elif x < 200:
            iq = "ziemlich schlau."
        else:
            iq = "ein **SUPERBRAIN**!"
        embed = discord.Embed(colour=discord.Color.gold(), description=f"Mit einem IQ von {x} ist {user.mention} {iq}")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command(usage="<frage>")
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ask(self, ctx, *, frage: str = None):
        """Lass bekannte Leute deine Frage beantworten."""
        if frage is None:
            await get_syntax(ctx)
            return

        all_gifs = ['https://tenor.com/view/shrek-of-course-sarcasm-sarcastic-really-gif-14499396',
                    'https://tenor.com/view/timon-lion-king-nope-no-shake-gif-3834543',
                    'https://tenor.com/view/yes-nod-old-spice-oh-yes-commercial-gif-15384634',
                    'https://tenor.com/view/agt-americas-got-talent-stop-buzzer-no-gif-4434972',
                    'https://tenor.com/view/yes-melb-agt-americas-got-talent-agtgifs-gif-4519427',
                    'https://tenor.com/view/egal-singing-ocean-sea-boat-ride-gif-16080257',
                    'https://tenor.com/view/thats-a-no-elmo-shaking-shaking-head-nope-gif-7663315',
                    'https://tenor.com/view/definitiv-nein-n%C3%B6-tv-total-raab-gif-11127197',
                    'https://tenor.com/view/shannon-sharpe-shay-nope-nah-nuhuh-gif-12298561',
                    'https://tenor.com/view/ja-jack-nicholson-fryslan-friesland-omrop-gif-12148366',
                    'https://tenor.com/view/ok-okay-awkward-smile-gif-5307535',
                    'https://tenor.com/view/elmo-shrug-gif-5094560',
                    'https://tenor.com/view/horrible-crying-noooo-no-gif-11951898',
                    'https://tenor.com/view/maaaayyybe-fallon-maybe-gif-5280420',
                    'https://tenor.com/view/idk-i-dont-know-sebastian-stan-lol-wtf-gif-5364867',
                    'https://tenor.com/view/yes-no-maybe-owl-funny-gif-13722109',
                    'https://tenor.com/view/yes-minions-movie-minions-gi-fs-minions-gif-5026357',
                    'https://tenor.com/view/steve-carell-no-please-no-gif-5026106',
                    'https://tenor.com/view/obama-wtf-why-president-wut-gif-12221156',
                    'https://tenor.com/view/trump-donald-trump-dance-thinking-idk-gif-5753267',
                    'https://tenor.com/view/inauguration-cnn2017-donald-trump-finger-wag-no-absolutely-not-gif-12953442',
                    'https://tenor.com/view/angela-merkel-keine-ahnung-no-clue-kanzlerin-deutschland-gif-11189427',
                    'https://tenor.com/view/merkel-n%C3%B6-n%C3%B6merkel-merkel-meme-gif-gif-16050778',
                    'https://tenor.com/view/angela-merkel-schmunzel-nicken-zufrieden-politik-gif-11862007']
        await ctx.send(f"**{frage}**\n\n{random.choice(all_gifs)}")

    @commands.command(usage="<user1> [user2]", aliases=["paar", ])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def love(self, ctx, u1: discord.Member = None, u2: discord.Member = None):
        """Finde heraus, wie verliebt 2 Benutzer oder du und ein anderer Benutzer sind!"""
        if u1 is None:
            await get_syntax(ctx)
            return

        if u2 is None and u1 is not None:
            u2 = ctx.message.author

        love_per = random.randint(1, 100)

        # erstes Einbetten
        embed = discord.Embed(color=discord.Color.orange(),
                              description=f"Mal sehen, wie sehr sich {u1.mention} und {u2.mention} lieben ... <3")
        embed.add_field(name="❤️ Loverator", value="💌 Ich berechne Liebe ...")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        message = await ctx.send(embed=embed)
        await asyncio.sleep(3)

        # 2. embed
        embed2 = discord.Embed(color=discord.Color.orange(),
                               description=f"Mal sehen, wie sehr sich {u1.mention} und {u2.mention} lieben ... <3")
        embed2.add_field(name="❤️ Loverator",
                         value=f"{u1.mention} und {u2.mention} lieben sich zu **{love_per}%**.")
        embed2.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await message.edit(embed=embed2)

    @commands.command(usage="[user]", aliases=["sr", ])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def susrate(self, ctx, user: discord.Member = None):
        """Ein hochkomplexes System berechnet wie SUS wird der Benutzer ist."""
        if user is None:
            user = ctx.author
        x = random.randint(1, 100)
        embed = discord.Embed(color=discord.Color.gold(), description=f"{user.mention} ist SUS zu {x}%. Jetzt abstimmen!")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command(usage="", aliases=["rubbellos", ])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def los(self, ctx):
        """Ziehe ein Ticket und reibe es auf, indem du auf die schwarzen Blöcke tippst."""
        choices1 = ["||⚪||", "||🔵||", "||⚪||", "||⚪||"]
        choices2 = ["||⚪||", "||🔵||", "||⚪||", "||⚪||"]
        choices3 = ["||⚪||", "||🔵||", "||⚪||", "||⚪||"]
        choices4 = ["||⚪||", "||🔵||", "||⚪||", "||⚪||"]
        choices5 = ["||⚪||", "||🔵||", "||⚪||", "||⚪||"]
        choices6 = ["||⚪||", "||🔵||", "||⚪||", "||⚪||"]
        choices7 = ["||⚪||", "||🔵||", "||⚪||", "||⚪||"]
        choices8 = ["||⚪||", "||🔵||", "||⚪||", "||⚪||"]
        choices9 = ["||⚪||", "||🔵||", "||⚪||", "||⚪||"]
        ergebnis1 = random.choice(choices1)
        ergebnis2 = random.choice(choices2)
        ergebnis3 = random.choice(choices3)
        ergebnis4 = random.choice(choices4)
        ergebnis5 = random.choice(choices5)
        ergebnis6 = random.choice(choices6)
        ergebnis7 = random.choice(choices7)
        ergebnis8 = random.choice(choices8)
        ergebnis9 = random.choice(choices9)
        embed = discord.Embed(colour=discord.Colour.dark_blue(), title="Rubbellos",
                              description=f"{ergebnis1} {ergebnis2} {ergebnis3}\n"
                                          f"{ergebnis4} {ergebnis5} {ergebnis6}\n"
                                          f"{ergebnis7} {ergebnis8} {ergebnis9}\n")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        embed.set_footer(text="3 von 🔵 in vertikal, horizontal oder diagonal")
        await ctx.send(embed=embed)

    @commands.command(aliases=['activities'], usage="")
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def games(self, ctx):
        """Zeigt alle Spiele an, die auf dem aktuellen Server gespielt werden."""
        description = ""
        for member in ctx.guild.members:
            if member.bot == False:
                for activity in member.activities:
                    if isinstance(activity, discord.Game):
                        description += f"**{activity}** - {member.mention}({member})\n"
                    elif isinstance(activity, discord.Activity):
                        description += f"**{activity.name}** - {member.mention}({member})\n"
            if member.bot:
                pass
        if description == "":
            description += "Sieht hier echt langweilig aus. Zurzeit spielt niemand ein Spiel."
        embed = discord.Embed(title="Aktuell gespielte Spiele auf diesem Server", description=description, color=discord.Color.green())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command(usage="<text>")
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def reverse(self, ctx, *, msg: str = None):
        """Dreht Text um."""
        if msg is None:
            await get_syntax(ctx)
            return
        else:
            embed = discord.Embed(colour=discord.Colour.green(), description=f"Umgekehrt!")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            embed.add_field(name="Vorher", value=f"{msg}")
            embed.add_field(name="Nachher", value=f"{msg[::-1]}")
            await ctx.send(embed=embed)
            return

    @commands.command(usage="")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def password(self, ctx):
        """Generiert ein zufälliges Passwort für dich!"""
        user = ctx.author
        letters = ["a","A","b","B","c","C","d","D","e","E","f","F","g","G","h","H","i","I","j","J","k","K","l","L","m","M","n","N","o","O","p","P","q","Q","r","R","s","S","t","T","u","U","v","V","w","W","x","X","y","Y","z","Z"]
        choices = [f"{random.choice(letters)}",f"{random.randint(1, 9)}",f"{random.choice(letters)}",f"{random.randint(1, 9)}",f"{random.choice(letters)}",f"{random.randint(1, 9)}",f"{random.choice(letters)}",f"{random.randint(1, 9)}",f"{random.choice(letters)}"]
        x1 = random.choice(choices)
        x2 = random.choice(choices)
        x3 = random.choice(choices)
        x4 = random.choice(choices)
        x5 = random.choice(choices)
        x6 = random.choice(choices)
        x7 = random.choice(choices)
        x8 = random.choice(choices)
        x9 = random.choice(choices)
        x10 = random.choice(choices)
        x11 = random.choice(choices)
        x12 = random.choice(choices)
        x13 = random.choice(choices)
        x14 = random.choice(choices)
        x15 = random.choice(choices)
        x16 = random.choice(choices)
        x17 = random.choice(choices)
        x18 = random.choice(choices)
        x19 = random.choice(choices)
        x20 = random.choice(choices)
        x21 = random.choice(choices)
        x22 = random.choice(choices)
        result = f"||{x1}{x2}{x3}{x4}{x5}{x6}{x7}{x8}{x9}{x10}{x11}{x12}{x13}{x14}{x15}{x16}{x17}{x18}{x19}{x20}{x21}{x22}||"

        embed = discord.Embed(colour=discord.Colour.green(), title="🔐 Passwort", description=f"**Nicht anderen Personen zeigen!**")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        embed.add_field(name="Vorgschlagenes Passwort:", value=result)
        await user.send(embed=embed)
        await ctx.send(f"{user.mention}, ich habe dir ein zufällig generiertes Passwort in deine Dm's geschickt!")
        return
        
async def setup(bot):
    await bot.add_cog(fun(bot))