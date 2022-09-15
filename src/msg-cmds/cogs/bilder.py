import os
import requests
import io
import aiohttp
import discord
from discord.ext import commands
import aiohttp
from PIL import Image
from io import BytesIO
from info import get_syntax


class bilder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="[Member]")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wanted(self, interaction, member: discord.Member=None):
        """Erstellt ein 'Gesucht' Plakat mit dem Profilbild eines Members."""
        if member == None:
            member = interaction.user
        if member != None:
            wanted = Image.open("wanted.jpg")
            asset = member.avatar
            data = BytesIO(await asset.read())
            pfp = Image.open(data)
            pfp = pfp.resize((240,240))
            wanted.paste(pfp, (128, 215))
            wanted.save("profile.jpg")
            embed = discord.Embed(title=" ", description=f"**{member} wird gesucht!**", colour=discord.Colour.blue())
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            file = discord.File("profile.jpg", filename="profile.jpg")
            embed.set_image(url="attachment://profile.jpg")
            await interaction.send(file=file, embed=embed)
            os.remove("profile.jpg")
    
    @commands.command(usage="[Member]")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
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
            embed = discord.Embed(title=" ", description=f"**{member} wurde verpixelt!**", colour=discord.Colour.blue())
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            file = discord.File("pix.png", filename="pix.png")
            embed.set_image(url="attachment://pix.png")
            await interaction.send(file=file, embed=embed)
            os.remove("pix.png")

    @commands.command(usage="[user/ID]")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def wasted(self, interaction, *, user: discord.Member = None):
        """Sendet ein Bild deines Avatars mit Effekten."""
        if user is None:
            user = interaction.user
        async with interaction.channel.typing():
            session = aiohttp.ClientSession()
            async with session.get(
                f"https://some-random-api.ml/canvas/wasted?avatar={user.avatar}") as r:
                if r.status != 200:
                    return await interaction.send("Fehler beim Laden es Bildes.")
                else:
                    data = io.BytesIO(await r.read())
                    file = discord.File(data, 'triggered.gif')
                    embed = discord.Embed(title=" ", description="**Geliefert!**", colour=discord.Colour.blue())
                    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
                    embed.set_image(url="attachment://triggered.gif")
                    await interaction.send(file=file, embed=embed)
                    await session.close()

    @commands.command(usage="")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cat(self, interaction):
        """Ein zufälliges Bild einer Katze."""
        try:
            async with interaction.channel.typing():
                async with aiohttp.ClientSession() as cs:
                    async with cs.get("http://aws.random.cat/meow") as r:
                        data = await r.json()

                        embed = discord.Embed(title="Miau")
                        embed.set_image(url=data['file'])
                        embed.set_footer(text="http://random.cat/")

                        await interaction.send(embed=embed)
        except:
            return await interaction.send("Fehler beim Laden es Bildes.") 

    @commands.command(usage="[user/ID]")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def triggered(self, interaction, *, user: discord.Member = None):
        """Sendet ein Bild deines Avatars mit Effekten."""
        if user is None:
            user = interaction.user
        async with interaction.channel.typing():
            session = aiohttp.ClientSession()
            async with session.get(
                f"https://some-random-api.ml/canvas/triggered?avatar={user.avatar}") as r:
                if r.status != 200:
                    return await interaction.send("Fehler beim Laden es Bildes.") 
                else:
                    data = io.BytesIO(await r.read())
                    file=discord.File(data, 'triggered.gif')
                    embed = discord.Embed(title=" ", description="**Genervt!!!**", colour=discord.Colour.blue())
                    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
                    embed.set_image(url="attachment://triggered.gif")
                    await interaction.send(file=file, embed=embed)
                    await session.close()

    @commands.command(usage="<HEX code>")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def color(self, interaction, arg=None):
        """Gib einen HEX-Code ein und die dazugehörige Farbe wird erscheinen."""
        if arg is None:
            await get_syntax(interaction)
            return
        else:
            try:
                link =f'https://some-random-api.ml/canvas/colorviewer?hex={arg}'

                embed = discord.Embed(color=discord.Color.light_gray(),title=f"**Hier die Farbe** **#{arg}**")
                embed.set_image(url=link)
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                embed.set_footer(text="HEX Code: (a-f, 1-9) up to 6 characters")

                await interaction.send(embed=embed)
            except:
                return await interaction.send("Fehler beim Laden es Bildes.")
    
    @commands.command(usage="[user/ID]")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gay(self, interaction, *, user: discord.Member = None):
        """Sendet ein Bild deines Avatars mit Effekten."""
        if user is None:
            user = interaction.user

        async with interaction.channel.typing():
            session = aiohttp.ClientSession()
            async with session.get(
                    f"https://some-random-api.ml/canvas/gay?avatar={user.avatar}") as r:
                if r.status != 200:
                    return await interaction.send("Fehler beim Laden es Bildes.")
                else:
                    data = io.BytesIO(await r.read())
                    file=discord.File(data, 'triggered.gif')
                    embed = discord.Embed(title=" ", description="**Schwul**!", colour=discord.Colour.blue())
                    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
                    embed.set_image(url="attachment://triggered.gif")
                    await interaction.send(file=file, embed=embed)
                    await session.close()
                    
    @commands.command(aliases=["mem"])
    @commands.is_nsfw()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def meme(self, interaction):
        """Sendet ein Meme."""
        if interaction.user.bot:
            return
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

                embed = discord.Embed(colour=discord.Colour.blue(), title=title, url=url)
                embed.set_image(url=image)
                embed.set_footer(text=f"🔺 {ups} | 🔻 {downs} | 💬 {comments} ")
                await interaction.send(embed=embed, content=None)

async def setup(bot):
    await bot.add_cog(bilder(bot))