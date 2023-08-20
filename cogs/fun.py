import asyncio
import asyncio
import random
import discord
from discord.ext import commands
from discord import app_commands
from info import getcolour

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def lostrate(self, interaction: discord.Interaction, user: discord.Member=None):
        """Berechnet mit einem hochkomplexen Prozess wie Lost der Benutzer ist."""
        if user is None:
            user = interaction.user
        x = random.randint(1, 100)
        embed = discord.Embed(colour=await getcolour(self, interaction.user), description=f"{user.mention} ist LOST zu {x}%.")
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def iq(self, interaction: discord.Interaction, member: discord.Member=None):
        """Finde heraus, wie hoch der IQ von dir oder einem Benutzer ist."""
        if member is None:
            member = interaction.user
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
        embed = discord.Embed(colour=await getcolour(self, interaction.user), description=f"Mit einem IQ von {x} ist {member.mention} {iq}")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def ask(self, interaction: discord.Interaction, frage: str):
        """Lass bekannte Leute deine Frage beantworten."""
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
        gif = random.choice(all_gifs)
        await interaction.response.send_message(f"**{frage}**\n\n{gif}")

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def love(self, interaction: discord.Interaction, member: discord.Member, user: discord.Member):
        """Finde heraus, wie verliebt 2 Benutzer oder du und ein anderer Benutzer sind!"""
        await interaction.response.send_message("**Mal sehen ob ihr verliebt seid 👀**")
        love_per = random.randint(1, 100)

        # erstes Einbetten
        embed = discord.Embed(color=await getcolour(self, interaction.user),
                              description=f"Mal sehen, wie sehr sich {member.mention} und {user.mention} lieben ... <3")
        embed.add_field(name="❤️ Loverator", value="💌 Ich berechne Liebe ...")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        message = await interaction.channel.send(embed=embed)
        await asyncio.sleep(3)

        # 2. embed
        embed2 = discord.Embed(color=await getcolour(self, interaction.user),
                               description=f"Mal sehen, wie sehr sich {member.mention} und {user.mention} lieben ... <3")
        embed2.add_field(name="❤️ Loverator",
                         value=f"{member.mention} und {user.mention} lieben sich zu **{love_per}%**.")
        embed2.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed2.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        await message.edit(embed=embed2)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def los(self, interaction: discord.Interaction):
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
        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="Rubbellos",
                              description=f"{ergebnis1} {ergebnis2} {ergebnis3}\n"
                                          f"{ergebnis4} {ergebnis5} {ergebnis6}\n"
                                          f"{ergebnis7} {ergebnis8} {ergebnis9}\n")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_footer(text="3 von 🔵 in vertikal, horizontal oder diagonal")
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def games(self, interaction: discord.Interaction):
        """Zeigt alle Spiele an, die auf dem aktuellen Server gespielt werden."""
        description = ""
        for member in interaction.guild.members:
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
        embed = discord.Embed(title="Aktuell gespielte Spiele auf diesem Server", description=description, color=await getcolour(self, interaction.user))
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def password(self, interaction: discord.Interaction):
        """Generiert ein zufälliges Passwort für dich!"""
        user = interaction.user
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

        embed = discord.Embed(colour=await getcolour(self, interaction.user), title="🔐 Passwort", description=f"**Nicht anderen Personen zeigen, falls du dieses Passwort verwenden solltest!**")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.add_field(name="Vorgschlagenes Passwort:", value=result)
        embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
        await user.send(embed=embed)
        await interaction.response.send_message(f"{user.mention}, ich habe dir ein zufällig generiertes Passwort in deine Dm's geschickt!")
        return
        
async def setup(bot):
    await bot.add_cog(fun(bot))