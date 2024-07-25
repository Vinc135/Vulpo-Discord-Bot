import typing
import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import getcolour
from PIL import Image
from io import BytesIO
from cogs.economy import open_acc, update_account
from utils.MongoDB import getMongoDataBase

class buttons(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Nächste Flagge', style=discord.ButtonStyle.grey, custom_id="FlaggenQuizNext", emoji="⏩")
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=False, ephemeral=True)
        acc = await open_acc(self, interaction.user)
        rucksack = int(acc["rucksack"])
        if 20 > int(rucksack):
            return await interaction.followup.send(f"<:v_x:1264270921452224562> Du hast nicht **20 Coins** in deinem Rucksack. Es fehlen dir **{20 - rucksack} Coins**. Entweder überweise dir die Cookies von deiner Bank in dein Rucksack oder gehe zuerst arbeiten oder betteln. Alle Commands siehst du mit `/help`.", ephemeral=True)

        await update_account(self, interaction.user, "rucksack", 0, 20)
        
        await interaction.channel.send(f"{interaction.user.mention} hat die Flagge übersprungen. (-20 Coins)")
        db = getMongoDataBase()
        fq_flaggen = db["fq_flaggen"]
        fqcurrent = db["fqcurrent"]

        db_entry = None
        file = False
        while not file:
            result = await fq_flaggen.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
            db_entry = result[0]
            file = await getFile(db_entry["filename"])
        
        embed = discord.Embed(color=await getcolour(self, interaction.user), title="Flaggenquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
        embed.set_footer(text=f"Das letzte Flaggenquiz wurde übersprungen von {interaction.user}.", icon_url=interaction.user.avatar)
        embed.set_image(url="attachment://Flagge.png")       
        m2 = await interaction.channel.send(embed=embed, file=file, view=buttons(self.bot))
        
        await fqcurrent.update_one(
            {"guildID": str(interaction.guild.id)},
            {"$set": {"lösung": db_entry["lösung"], "msgID": str(m2.id)}},
            upsert=True
        )

    @discord.ui.button(label='Anfangsbuchstabe', style=discord.ButtonStyle.grey, custom_id="FirstLetterFlaggenQuiz", emoji="💡")
    async def letter(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        db = getMongoDataBase()
        fqcurrent = db["fqcurrent"]
        
        result = await fqcurrent.find_one({"guildID": str(interaction.guild.id)})
        if result:
            return await interaction.followup.send(f"💡 Der erste Buchstabe der gesuchten Flagge ist __**{result['lösung'][0]}**__.", ephemeral=True)
        await interaction.followup.send(f"<:v_x:1264270921452224562> Es gibt aktuell keine Lösung", ephemeral=True)

async def updateLeaderbord(bot, userid):
    db = getMongoDataBase()
    fq_leaderboard = db["fq_leaderboard"]
    
    r = await fq_leaderboard.find_one({"userID": userid})
    if r:
        await fq_leaderboard.update_one(
            {"userID": userid},
            {"$inc": {"anzahl": 1}}
        )
    else:
        await fq_leaderboard.insert_one({"userID": userid, "anzahl": 1})

async def check_channel(self, msg):
    db = getMongoDataBase()
    fq = db["fq"]
    
    result = await fq.find_one({"guildID": str(msg.guild.id)})
    if result:
        return int(result["channelID"]) == int(msg.channel.id)
    
    return False

async def check_word(self, msg: discord.Message):
    db = getMongoDataBase()
    fqcurrent = db["fqcurrent"]
    
    result = await fqcurrent.find_one({"guildID": str(msg.guild.id)})
    if result and result["lösung"].lower() == msg.content.lower():
        await fqcurrent.delete_one({"guildID": str(msg.guild.id)})
        return True
    return False

async def answer_correct(self, msg):
    await msg.channel.send(f"{msg.author.mention} hat den gesuchten Begriff erraten. (+10 Coins)")
    await update_account(self, msg.author, "rucksack", 10, 0)
    
    db = getMongoDataBase()
    fq_flaggen = db["fq_flaggen"]
    fqcurrent = db["fqcurrent"]
    
    db_entry = None
    file = False
    
    while not file:
        result = await fq_flaggen.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
        db_entry = result[0]
    
        file = await getFile(db_entry["filename"])
    
    embed = discord.Embed(color=await getcolour(self, msg.author), title="Flaggenquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
    embed.set_image(url="attachment://Flagge.png")
    embed.set_footer(text=f"Das letzte Flaggenquiz wurde gelöst von {msg.author}.", icon_url=msg.author.avatar)
    m2 = await msg.channel.send(embed=embed, file=file, view=buttons(self.bot))
    
    await fqcurrent.insert_one({"guildID": msg.guild.id, "lösung": db_entry["lösung"], "msgID": str(m2.id)})
    await updateLeaderbord(self.bot, msg.author.id)

async def answer_incorrect(self, msg):
    try:
        await msg.add_reaction("<:v_x:1264270921452224562>")
    except: 
        pass

async def getFile(filename):
    img = None
    
    img = Image.open(f"./flaggenquiz/{filename}")
    with BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        file = discord.File(fp=image_binary, filename='Flagge.png')
        return file

class flaggenquiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=buttons(self.bot))
        
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if(msg.guild is None or msg.author.bot):
            return
        
        tf1 = await check_channel(self, msg)
        
        if not tf1:
            return
        
        if not msg.guild or msg.author.bot:
            return
        
        tf2 = await check_word(self, msg)
        
        if tf2:
            await answer_correct(self, msg)
        else:
            await answer_incorrect(self, msg)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.default_permissions(manage_guild=True)
    async def flaggenquiz(self, interaction: discord.Interaction, modus: typing.Literal["Anschalten", "Ausschalten"], kanal: typing.Union[discord.TextChannel, discord.ForumChannel, discord.Thread]):
        """Verwalte das Flaggenquiz deines Servers."""
        await interaction.response.defer()

        server = interaction.guild
        db = getMongoDataBase()
        fq = db["fq"]
        fq_flaggen = db["fq_flaggen"]
        fqcurrent = db["fqcurrent"]

        if modus == "Anschalten":
            flag = await fq.find_one({"guildID": str(server.id)})
            
            if not flag:
                await fq.insert_one({"guildID": str(server.id), "channelID": str(kanal.id)})
            else:
                await fqcurrent.delete_one({"guildID": str(server.id)})
                await fq.update_one({"guildID": str(server.id)}, {"$set": {"channelID": str(kanal.id)}})

            flag = None
            file = None
            fileFound = False
            while not fileFound:
                flag = await fq_flaggen.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
                flag = flag[0]
                
                file = await getFile(flag["filename"])
                
                
                if(file is not None and file is not False):
                    fileFound = True
            
            embed = discord.Embed(color=discord.Colour.orange(), title="Flaggenquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
            embed.set_image(url="attachment://Flagge.png")       
            m = await kanal.send(embed=embed, file=file, view=buttons(self.bot))
            
            await fqcurrent.insert_one({"guildID": str(interaction.guild.id), "lösung": flag["lösung"], "msgID": str(m.id)})
            return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Das Flaggenquiz wurde {'neu ' if flag else ''} gestartet in {kanal.mention}.**", ephemeral=True)
        
        if modus == "Ausschalten":
            flag = await fq.find_one({"guildID": str(server.id)})
            if not flag:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Das Flaggenquiz ist in diesem Server nicht aktiviert.**", ephemeral=True)
            
            await fq.delete_one({"guildID": str(server.id)})
            return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Das Flaggenquiz wurde in diesem Server ausgeschaltet.**", ephemeral=True)

async def setup(bot):
    await bot.add_cog(flaggenquiz(bot))