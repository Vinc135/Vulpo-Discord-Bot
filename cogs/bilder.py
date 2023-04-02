import os
import requests
import io
import aiohttp
import discord
from discord.ext import commands
import aiohttp
from PIL import Image
from io import BytesIO
from discord import app_commands
from info import getcolour

class bilder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def wanted(self, interaction, member: discord.Member=None):
        """Erstellt ein 'Gesucht' Plakat mit dem Profilbild eines Members."""
        if member == None:
            member = interaction.user
        if member != None:
            wanted = Image.open("wanted.jpg")
            asset = member.avatar
            data = BytesIO(await asset.read())
            pfp = Image.open(data)
            pfp = pfp.resize((640,640))
            wanted.paste(pfp, (335, 565))
            wanted.save("profile.jpg")
            embed = discord.Embed(title=" ", description=f"**{member} wird gesucht!**", colour=await getcolour(self, interaction.user))
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            file = discord.File("profile.jpg", filename="profile.jpg")
            embed.set_image(url="attachment://profile.jpg")
            await interaction.response.send_message(file=file, embed=embed)
            os.remove("profile.jpg")
    
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def pix(self, interaction, member: discord.Member=None):
        """Verpixelt das Profilbild eines Nutzers."""
        if member == None:
            member = interaction.user
        if member != None:
            url = str(member.avatar)
            url = url.replace("gif", "png")
            img = Image.open(requests.get(url, stream=True).raw)
            old = img.size
            img = img.resize((16, 16))
            img = img.resize(old)
            img.save('pix.png')
            embed = discord.Embed(title=" ", description=f"**{member} wurde verpixelt!**", colour=await getcolour(self, interaction.user))
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            file = discord.File("pix.png", filename="pix.png")
            embed.set_image(url="attachment://pix.png")
            await interaction.response.send_message(file=file, embed=embed)
            os.remove("pix.png")

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def wasted(self, interaction, *, member: discord.Member = None):
        """Sendet ein Bild deines Avatars mit Effekten."""
        if member is None:
            member = interaction.user
        async with interaction.channel.typing():
            session = aiohttp.ClientSession()
            async with session.get(
                f"https://some-random-api.ml/canvas/wasted?avatar={member.avatar}") as r:
                if r.status != 200:
                    return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Fehler beim Laden es Bildes. Versuche es später erneut!**", ephemeral=True)
                else:
                    data = io.BytesIO(await r.read())
                    file = discord.File(data, 'triggered.gif')
                    embed = discord.Embed(title=" ", description="**Geliefert!**", colour=await getcolour(self, interaction.user))
                    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
                    embed.set_image(url="attachment://triggered.gif")
                    await interaction.response.send_message(file=file, embed=embed)
                    await session.close()

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def cat(self, interaction):
        """Ein zufälliges Bild einer Katze."""
        try:
            async with interaction.channel.typing():
                async with aiohttp.ClientSession() as cs:
                    async with cs.get("http://aws.random.cat/meow") as r:
                        data = await r.json()

                        embed = discord.Embed(title="Miau", color=await getcolour(self, interaction.user))
                        embed.set_image(url=data['file'])
                        embed.set_footer(text="http://random.cat/")

                        await interaction.response.send_message(embed=embed)
        except:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Fehler beim Laden es Bildes. Versuche es später erneut!**", ephemeral=True)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def triggered(self, interaction, *, member: discord.Member=None):
        """Sendet ein Bild deines Avatars mit Effekten."""
        if member is None:
            member = interaction.user
        async with interaction.channel.typing():
            session = aiohttp.ClientSession()
            async with session.get(
                f"https://some-random-api.ml/canvas/triggered?avatar={member.avatar}") as r:
                if r.status != 200:
                    return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Fehler beim Laden es Bildes. Versuche es später erneut!**", ephemeral=True)
                else:
                    data = io.BytesIO(await r.read())
                    file=discord.File(data, 'triggered.gif')
                    embed = discord.Embed(title=" ", description="**Genervt!!!**", colour=await getcolour(self, interaction.user))
                    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
                    embed.set_image(url="attachment://triggered.gif")
                    await interaction.response.send_message(file=file, embed=embed)
                    await session.close()

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def color(self, interaction, hexcode: str):
        """Gib einen HEX-Code ein und die dazugehörige Farbe wird erscheinen."""
        try:
            link =f'https://some-random-api.ml/canvas/colorviewer?hex={hexcode}'

            embed = discord.Embed(color=await getcolour(self, interaction.user), title=f"**Hier die Farbe** **#{hexcode}**")
            embed.set_image(url=link)
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            embed.set_footer(text="HEX Code: (a-f, 1-9) up to 6 characters")

            await interaction.response.send_message(embed=embed)
        except:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Fehler beim Laden es Bildes. Versuche es später erneut!**", ephemeral=True)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def regenbogen(self, interaction, member: discord.Member=None):
        """Sendet ein Bild deines Avatars mit Effekten."""
        if member is None:
            member = interaction.user

        async with interaction.channel.typing():
            session = aiohttp.ClientSession()
            async with session.get(
                    f"https://some-random-api.ml/canvas/gay?avatar={member.avatar}") as r:
                if r.status != 200:
                    return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Fehler beim Laden es Bildes. Versuche es später erneut!**", ephemeral=True)
                else:
                    data = io.BytesIO(await r.read())
                    file=discord.File(data, 'triggered.gif')
                    embed = discord.Embed(title=" ", description="**Schwul**!", colour=await getcolour(self, interaction.user))
                    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
                    embed.set_image(url="attachment://triggered.gif")
                    await interaction.response.send_message(file=file, embed=embed)
                    await session.close()
                    
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def meme(self, interaction):
        """Sendet ein Meme."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/memes/random/.json') as r:
                res = await r.json()

                image = res[0]['data']['children'][0]['data']['url']
                permalink = res[0]['data']['children'][0]['data']['permalink']
                url = f'https://reddit.com{permalink}'
                title = res[0]['data']['children'][0]['data']['title']
                ups = res[0]['data']['children'][0]['data']['ups']
                downs = res[0]['data']['children'][0]['data']['downs']
                comments = res[0]['data']['children'][0]['data']['num_comments']

                embed = discord.Embed(colour=await getcolour(self, interaction.user), title=title, url=url)
                embed.set_image(url=image)
                embed.set_footer(text=f"🔺 {ups} | 🔻 {downs} | 💬 {comments} ")
                await interaction.response.send_message(embed=embed, content=None)

async def setup(bot):
    await bot.add_cog(bilder(bot))