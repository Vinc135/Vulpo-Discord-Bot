import os
import typing
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
import asyncio
import random

def get_pic_from_pixabay(q, category):
    url = "https://pixabay.com/api/"
    api_key = "38012586-0dbb65610fcbf43f53d7ff81c"

    params = {
        "key": api_key,
        "q": q,
        "image_type": "photo",
        "category": category,
        "per_page": 50
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "hits" in data:

            random_pic = random.choice(data["hits"])

            image_url = random_pic["webformatURL"]
            return image_url
        else:
            return "Keine Ergebnisse gefunden."
    except requests.RequestException as e:
        return "Fehler bei der Anfrage:", str(e)


class bilder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def wanted(self, interaction, member: discord.Member=None):
        """Erstellt ein 'Gesucht' Plakat mit dem Profilbild eines Members."""
        if member is None:
            member = interaction.user
        if member is not None:
            wanted = Image.open("wanted.jpg")
            asset = member.avatar
            data = BytesIO(await asset.read())
            pfp = Image.open(data)
            pfp = pfp.resize((640,640))
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, wanted.paste, pfp, (335, 565))
            with BytesIO() as image_binary:
                wanted.save(image_binary, 'JPEG')
                image_binary.seek(0)
                file = discord.File(fp=image_binary, filename='profile.jpg')
            embed = discord.Embed(title=" ", description=f"**{member} wird gesucht!**", colour=await getcolour(self, interaction.user))
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            embed.set_image(url="attachment://profile.jpg")
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(file=file, embed=embed)
    
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
            embed.set_footer(text="Premium jetzt veröffentlicht! www.vulpo-bot.de/premium")
            await interaction.response.send_message(file=file, embed=embed)
            os.remove("pix.png")

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def animal(self, interaction, tier: typing.Literal["Hund", "Katze", "Pferd", "Vogel", "Kaninchen", "Meerschweinchen", "Hamster", "Fisch", "Schildkröte", "Wellensittich", "Hase", "Schlange", "Frettchen", "Maus", "Kanarienvogel"]):
        """Ein zufälliges Bild eines Tieres."""
        try:
            url = get_pic_from_pixabay(tier, "animals")
            embed = discord.Embed(title=" ", description=f"**{tier}**", colour=await getcolour(self, interaction.user))
            embed.set_image(url=url)

            await interaction.response.send_message(embed=embed)
        except:
            return await interaction.response.send_message("**<:v_kreuz:1119580775411621908> Fehler beim Laden es Bildes. Versuche es später erneut!**", ephemeral=True)
          
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