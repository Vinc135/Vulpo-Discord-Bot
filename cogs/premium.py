import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from utils.utils import getcolour
from utils.MongoDB import getMongoDataBase
import re
from io import BytesIO
from PIL import Image
import datetime

class buttons(discord.ui.View):
    def __init__(self, bot=None, farbe=None):
        super().__init__(timeout=None)
        self.bot = bot
        self.farbe = farbe

    @discord.ui.button(label='Ja', style=discord.ButtonStyle.green, custom_id="fhweouchiorbvl", emoji="✅")
    async def ja(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        db = getMongoDataBase()
        
        result = db["embedfarben"].find_one({"userID": interaction.user.id})
        
        if result == None:
            db["embedfarben"].insert_one({"userID": interaction.user.id, "farbe": self.farbe})
            return await interaction.response.send_message(f"**✅ Alles klar, die Farbe wurde geändert zu {self.farbe}. Du kannst jederzeit diesen Befehl erneut ausführen, um die Farbe aller Embeds zu ändern.**", ephemeral=True)
        
        db["embedfarben"].update_one({"userID": interaction.user.id}, {"$set": {"farbe": self.farbe}})
        await interaction.response.edit_message(embed=None, view=None, content=f"**✅ Alles klar, die Farbe wurde geändert zu {self.farbe}. Du kannst jederzeit diesen Befehl erneut ausführen, um die Farbe aller Embeds zu ändern.**")

    @discord.ui.button(label='Nein', style=discord.ButtonStyle.red, custom_id="wehrfuzgweofouhb", emoji="<:v_x:1264270921452224562>")
    async def nein(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=None, view=None, content="**<:v_x:1264270921452224562> Alles klar, die Farbe wurde nicht geändert. Du kannst jederzeit diesen Befehl erneut ausführen, um die Farbe aller Embeds zu ändern.**")

async def remove_expired_users(self):
    current_timestamp = datetime.datetime.now().timestamp()
    
    db = getMongoDataBase()
    
    result = db["premium"].find()
    
    for user in result:
        if user["endtime"] == None:
            continue
        
        if user["endtime"] < current_timestamp:
            db["premium"].delete_one({"userID": user["userID"]})

class premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_load(self):
        self.check.start()

    def cog_unload(self):
        self.check.cancel()


    @tasks.loop(seconds=60)
    async def check(self):
        await remove_expired_users(self)

    premium = app_commands.Group(name='premium', description='Verwalte dein Premium Abo.', guild_only=True)

    @premium.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def embedfarbe(self, interaction: discord.Interaction, neuefarbe: str=None):
        """Ändere die Farbe aller Embeds, die dir gesendet werden von Vulpo."""
        
        db = getMongoDataBase()
        
        status = db["premium"].find_one({"userID": interaction.user.id})
        
        if status == None:
            return await interaction.response.send_message("<:v_x:1264270921452224562> **Du hast kein Premium. Premium ist heiß begehrt. Du kannst es bekommen, indem du ein Abonnement wirst: https://vulpo-bot.de/premium.**", ephemeral=True)
        
        if status["status"] == 0:
            return await interaction.response.send_message("<:v_x:1264270921452224562> **Du hast kein Premium. Premium ist heiß begehrt. Du kannst es bekommen, indem du ein Abonnement wirst: https://vulpo-bot.de/premium.**", ephemeral=True)
        
        if neuefarbe is None:
            embed = discord.Embed(title="Farbe", description="Dies ist deine aktuelle Farbe, sie wird bei allen Embeds, die für dich bestimmt sind, verwendet.", color=await getcolour(self, interaction.user))
            return await interaction.response.send_message(embed=embed, ephemeral=True)
            
        if not re.match(r'^[0-9a-fA-F]+$', neuefarbe):
            return await interaction.response.send_message(f"<:v_x:1264270921452224562> **Ungültiger Hexcode: {neuefarbe}. [Hier kannst du Farben mit dem entsprechenden HEX-Code finden](https://encycolorpedia.de).**", ephemeral=True)
        
        embed = discord.Embed(color=discord.Colour(int(neuefarbe, 16)),title=f"Soll diese Farbe die neue Farbe aller Embeds sein?")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_footer(text="HEX Code: (a-f, 1-9) bis zu 6 Ziffern")
        
        await interaction.response.send_message(embed=embed, ephemeral=True, view=buttons(self.bot, neuefarbe))

    @premium.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def rangkarte(self, interaction: discord.Interaction, bild: discord.Attachment):
        """Ändere das Bild deiner Rangkarte."""
        if not bild.content_type.startswith("image/"):
            return await interaction.response.send_message("<:v_x:1264270921452224562> **Das Attachment ist kein Bild.**", ephemeral=True)

        image = Image.open(BytesIO(await bild.read()))
        if image.width != 1000 or image.height != 250:
            return await interaction.response.send_message("<:v_x:1264270921452224562> **Das Bild muss die Maße 1000x250 haben.**", ephemeral=True)
        if image.format != "PNG":
            return await interaction.response.send_message("<:v_x:1264270921452224562> **Das Bild muss im PNG-Format vorliegen.**", ephemeral=True)
        
        db = getMongoDataBase()
        
        status = db["premium"].find_one({"userID": interaction.user.id})
        
        if status == None:
            return await interaction.response.send_message("<:v_x:1264270921452224562> **Du hast kein Premium. Premium ist heiß begehrt. Du kannst es bekommen, indem du ein Abonnement wirst: https://vulpo-bot.de/premium.**", ephemeral=True)
        
        if status["status"] == 0:
            return await interaction.response.send_message("<:v_x:1264270921452224562> **Du hast kein Premium. Premium ist heiß begehrt. Du kannst es bekommen, indem du ein Abonnement wirst: https://vulpo-bot.de/premium.**", ephemeral=True)
        
        bild.save(f"Rank_Bilder/{interaction.user.id}.png")
        fullpath = os.path.join("Rank_Bilder/", f"{interaction.user.id}.png")
        image.save(fullpath)
        await interaction.response.send_message("✅ **Das Bild wurde gesetzt. Teste es doch gleich mal mit `/rang`.**", ephemeral=True)

async def setup(bot):
    await bot.add_cog(premium(bot)) 