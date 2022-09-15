import asyncio
import random
import typing
import discord
from discord.ext import commands
from discord import app_commands
from info import random_color

class Emojiquiz_Vorschlag_abgeben(discord.ui.Modal, title="Vorschlag für's Emojiquiz"):
    def __init__(self, bot=None):
        self.bot = bot
        super().__init__(custom_id="bldshcakjdbckhqbedcjbwhvil")
        self.add_item(discord.ui.TextInput(label="Gesuchter Begriff", style=discord.TextStyle.short, required=True, placeholder="minimal 2 Emojis"))
        self.add_item(discord.ui.TextInput(label="Tipp", style=discord.TextStyle.short, required=True, placeholder="Ein Tipp um es leichter herauszufinden."))
        self.add_item(discord.ui.TextInput(label="Lösung", style=discord.TextStyle.short, required=True, placeholder="Hier den gesuchten Begriff."))

    async def on_submit(self, interaction: discord.Interaction):
        if int(interaction.user.id) == 689386059326292008:
            return await interaction.response.send_message("**❌ Du kannst keine Vorschläge mehr abgeben, da du auf der Blacklist stehst. EInen Antrag auf Entbannung kannst du im [Supportserver](https://discord.gg/49jD3VXksp) stellen.**", ephemeral=True)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT lösung FROM eqdb")
                ergebnis = await cursor.fetchall()      
                a = 0
                for word in ergebnis:
                    if word[0].lower() == str(self.children[2]).lower():
                        a += 1
                if a == 1:
                    return await interaction.response.send_message("❌ Der Vorschlag wurde nicht eingereicht, da der Begriff bereits existiert.", ephemeral=True)
                ###
                await cursor.execute(f"SELECT rucksack, bank, job, stunden FROM economy WHERE userID = {interaction.user.id}")
                result = await cursor.fetchone()
                if result is None:
                    await cursor.execute("INSERT INTO economy(rucksack, bank, job, stunden, userID) VALUES(%s, %s, %s, %s, %s)",("0", "0", "Kein Job", "0", interaction.user.id))
                    bal = 0
                else:
                    bal = int(result[0])
                new = bal + 100
                await cursor.execute("UPDATE economy SET rucksack = (%s) WHERE userID = (%s)", (new, interaction.user.id))

                cembed = discord.Embed(title=f"Neue Einsendung", description="Dieser Vorschlag muss noch bearbeitet werden.", color=random_color())
                cembed.add_field(name="Gesuchter Begriff", value=self.children[0].value, inline=False)
                cembed.add_field(name="Tipp", value=self.children[1].value, inline=False)
                cembed.add_field(name="Lösung", value=self.children[2].value, inline=False)
                cembed.set_author(name=interaction.user, icon_url=interaction.user.avatar if interaction.user.avatar else "https://cdn.discordapp.com/avatars/925799559576322078/a2f839c85ee1dd3ef9a1b1fa511e332b.png?size=1024")
                guild = self.bot.get_guild(925729625580113951)
                channel = guild.get_channel(959846011545739374)
                await channel.send(embed=cembed, view=database(self.bot))
                await interaction.response.send_message("**Dankeschön für deine Einsendung**\n<:herz:941398727501955113> Als Dankeschön hast du 100 Coins in Vulpo's Economy System erhalten.", ephemeral=True)

class database(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Annehmen', style=discord.ButtonStyle.grey, custom_id="hdfkgqehvfkhgwevkhgvwekhgfvkhgvkj", emoji="✅")
    async def annehmen(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                message = await interaction.channel.fetch_message(interaction.message.id)
                embed = message.embeds[0]
                emojis = embed.fields[0].value
                tipp = embed.fields[1].value
                lösung = embed.fields[2].value
                
                await cursor.execute("SELECT lösung FROM eqdb")
                result = await cursor.fetchall()
                if result is None:
                    await cursor.execute("INSERT INTO eqdb(emojis, tipp, lösung) VALUES(%s, %s, %s)", (emojis, tipp, lösung))
                    await message.delete()
                    await interaction.response.send_message("✅ Der Vorschlag wurde mit in die Datenbank aufgenommen.", ephemeral=True)
                    
                    
                a = 0
                for word in result:
                    if word[0].lower() == lösung.lower():
                        a += 1
                    else:
                        pass
                if a == 1:
                    await interaction.message.delete()
                    return await interaction.response.send_message("❌ Der Vorschlag wurde nicht in die Datenbank mit aufgenommen, da er bereits existiert.", ephemeral=True)
                else:
                    await cursor.execute("INSERT INTO eqdb(emojis, tipp, lösung) VALUES(%s, %s, %s)", (emojis, tipp, lösung))
                    await message.delete()
                    await interaction.response.send_message("✅ Der Vorschlag wurde mit in die Datenbank aufgenommen.", ephemeral=True)
        
    @discord.ui.button(label='Ablehnen', style=discord.ButtonStyle.grey, custom_id="wkgedkuzqgewuzfdhwelic", emoji="❌")
    async def ablehnen(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message("❌ Der Vorschlag wurde nicht in die Datenbank mit aufgenommen.", ephemeral=True)
        
        
class buttons(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Nächstes Wort', style=discord.ButtonStyle.grey, custom_id="jqvefkghwkcvh", emoji="⏩")
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        acc = await open_acc(self, interaction.user)
        rucksack = int(acc[0])
        if 20 > int(rucksack):
            return await interaction.response.send_message(f"❌ Du hast nicht **20 🍪** in deinem Rucksack. Es fehlen dir **{20 - rucksack} 🍪**. Entweder überweise dir die Cookies von deiner Bank in dein Rucksack oder gehe zuerst arbeiten oder betteln. Alle Commands siehst du mit `/help`.", ephemeral=True)

        await update_acc(self, interaction.user, "rucksack", 0, 20)
        
        await interaction.response.defer(thinking=False, ephemeral=True)
        m = await interaction.channel.send(f"{interaction.user.mention} hat den Begriff übersprungen. (-20 🍪)")
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT emojis, lösung, tipp FROM eqdb")
                result = await cursor.fetchall()
                a = random.randint(1, int(len(result)))
                b = 0
                for quiz in result:
                    if a == b:
                        embed = discord.Embed(color=random_color(), title="Emojiquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                        embed.add_field(name="❓ Gesuchter Begriff", value=quiz[0])
                        embed.add_field(name="❗️ Tipp", value=quiz[2])
                        embed.set_footer(text=f"Das letzte Quiz wurde übersprungen von {interaction.user}.", icon_url=interaction.user.avatar)
                        await asyncio.sleep(2)
                        async for message in interaction.channel.history():
                            await message.delete()
                        m2 = await interaction.channel.send(embed=embed, view=buttons(self.bot))
                        await cursor.execute("DELETE FROM eqcurrent WHERE guildID = (%s)", (interaction.guild.id))
                        await cursor.execute("INSERT INTO eqcurrent(guildID, lösung, msgID) VALUES(%s, %s, %s)", (interaction.guild.id, quiz[1], m2.id))
                        b += 100000
                    else:
                        b += 1
    
    @discord.ui.button(label='Anfangsbuchstabe', style=discord.ButtonStyle.grey, custom_id="dvekzlfdigqwjvliz", emoji="💡")
    async def letter(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT lösung FROM eqcurrent WHERE guildID = (%s)", (interaction.guild.id))
                result = await cursor.fetchone()
                await interaction.response.send_message(f"💡 Der erste Buchstabe des gesuchten Wortes ist __**{result[0][0]}**__. Mehr Tipps gebe ich aber nicht.", ephemeral=True)
    
    @discord.ui.button(label='Neuen Begriff vorschlagen', style=discord.ButtonStyle.grey, custom_id="dgqeiufdzgfwjggjvekj", emoji="🙋‍♂️")
    async def vorschlag(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Emojiquiz_Vorschlag_abgeben(self.bot))

async def open_acc(self, user):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SELECT rucksack, bank, job, stunden FROM economy WHERE userID = {user.id}")
            result = await cursor.fetchone()
            if result is None:
                await cursor.execute("INSERT INTO economy(rucksack, bank, job, stunden, userID) VALUES(%s, %s, %s, %s, %s)",("0", "0", "Kein Job", "0", user.id))
                
                liste = ["0","0","Kein Job","0",user.id]
                return liste
            else:
                return result

async def update_acc(self, user, mode, sum, dif):
    acc = await open_acc(self, user)
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            if mode == "rucksack":
                bal = acc[0]
                new = int(bal) + int(sum) - int(dif)
                await cursor.execute("UPDATE economy SET rucksack = (%s) WHERE userID = (%s)", (new, user.id))
                
            if mode == "bank":
                bal = acc[1]
                new = int(bal) + int(sum) - int(dif)
                await cursor.execute("UPDATE economy SET bank = (%s) WHERE userID = (%s)", (new, user.id))


async def check_channel(self, msg):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT channelID FROM eq WHERE guildID = (%s)", (msg.guild.id))
            result = await cursor.fetchone()
            if result is None:
                return False
            else:
                if int(result[0]) == int(msg.channel.id):
                    return True
                else:
                    return False

async def check_word(self, msg: discord.Message):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT lösung FROM eqcurrent WHERE guildID = (%s)", (msg.guild.id))
            result = await cursor.fetchone()
            if result is None:
                return False
            if result[0].lower() == msg.content.lower():
                await cursor.execute("DELETE FROM eqcurrent WHERE guildID = (%s)", (msg.guild.id))
                return True
            elif result[0].lower() != msg.content.lower():
                return False
                
async def answer_correct(self, msg):
    await msg.channel.send(f"{msg.author.mention} hat den gesuchten Begriff erraten. (+10 🍪)")
    await update_acc(self, msg.author, "rucksack", 10, 0)
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT emojis, lösung, tipp FROM eqdb")
            result = await cursor.fetchall()
            a = random.randint(1, int(len(result)))
            b = 0
            for quiz in result:
                if a == b:
                    embed = discord.Embed(color=random_color(), title="Emojiquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                    embed.add_field(name="❓ Gesuchter Begriff", value=quiz[0])
                    embed.add_field(name="❗️ Tipp", value=quiz[2])
                    embed.set_footer(text=f"Das letzte Quiz wurde gelöst von {msg.author}.", icon_url=msg.author.avatar)
                    await asyncio.sleep(2)
                    async for message in msg.channel.history():
                        await message.delete()
                    m2 = await msg.channel.send(embed=embed, view=buttons(self.bot))
                    await cursor.execute("INSERT INTO eqcurrent(guildID, lösung, msgID) VALUES(%s, %s, %s)", (msg.guild.id, quiz[1], m2.id))
                    await cursor.execute("SELECT anzahl FROM eq_leaderboard WHERE userID = (%s)", (msg.author.id))
                    r = await cursor.fetchone()
                    if r != None:
                        await cursor.execute("UPDATE eq_leaderboard SET anzahl = (%s) WHERE userID = (%s)", (int(r[0]) + 1, msg.author.id))
                    if r == None:
                        await cursor.execute("INSERT INTO eq_leaderboard(userID, anzahl) VALUES(%s, %s)", (msg.author.id, 1))
                    b += 100000
                else:
                    b += 1

async def answer_incorrect(self, msg):
    await msg.add_reaction("❌")
            
class Emojiquiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=buttons(self.bot))
        self.bot.add_view(view=database(self.bot))
        
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.guild == None:
            return
        if msg.author.bot:
            return
        tf1 = await check_channel(self, msg)
        if tf1 == False:
            return
        else:
            tf2 = await check_word(self, msg)
            if tf2 == True:
                await answer_correct(self, msg)
            else:
                await answer_incorrect(self, msg)
    
    @app_commands.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def emojiquiz(self, interaction: discord.Interaction, modus: typing.Literal["Anschalten", "Ausschalten"], kanal: discord.TextChannel):
        """Verwalte das Enojiquiz deines Servers."""
        if modus == "Anschalten":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelID FROM eq WHERE guildID = (%s)", (interaction.guild.id))
                    result = await cursor.fetchone()
                    if result is None:
                        await cursor.execute("INSERT INTO eq(guildID, channelID) VALUES(%s, %s)", (interaction.guild.id, kanal.id))
                        await cursor.execute("SELECT emojis, lösung, tipp FROM eqdb")
                        result2 = await cursor.fetchall()
                        a = random.randint(1, int(len(result2)))
                        b = 0
                        for quiz in result2:
                            if a == b:
                                embed = discord.Embed(color=random_color(), title="Emojiquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                                embed.add_field(name="❓ Gesuchter Begriff", value=quiz[0])
                                embed.add_field(name="❗️ Tipp", value=quiz[2])
                                m2 = await kanal.send(embed=embed, view=buttons(self.bot))
                                await cursor.execute("INSERT INTO eqcurrent(guildID, lösung, msgID) VALUES(%s, %s, %s)", (interaction.guild.id, quiz[1], m2.id))
                                b += 100000
                                return await interaction.response.send_message(f"**✅ Das Emojiquiz wurde gestartet in {kanal.mention}.**", ephemeral=True)
                            else:
                                b += 1
                    if result is not None:
                        await cursor.execute("UPDATE eq SET channelID = (%s) WHERE guildID = (%s)", (kanal.id, interaction.guild.id))
                        await cursor.execute("SELECT emojis, lösung, tipp FROM eqdb")
                        result2 = await cursor.fetchall()
                        a = random.randint(1, int(len(result2)))
                        b = 0
                        for quiz in result2:
                            if a == b:
                                embed = discord.Embed(color=random_color(), title="Emojiquiz", description="Solltest du Probleme beim Lösen haben, kannst du die Buttons dieser Nachricht benutzen.")
                                embed.add_field(name="❓ Gesuchter Begriff", value=quiz[0])
                                embed.add_field(name="❗️ Tipp", value=quiz[2])
                                m2 = await kanal.send(embed=embed, view=buttons(self.bot))
                                await cursor.execute("INSERT INTO eqcurrent(guildID, lösung, msgID) VALUES(%s, %s, %s)", (interaction.guild.id, quiz[1], m2.id))
                                b += 100000
                                return await interaction.response.send_message(f"**✅ Das Emojiquiz wurde neu gestartet in {kanal.mention}.**", ephemeral=True)
                            else:
                                b += 1
        if modus == "Ausschalten":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT channelID FROM eq WHERE guildID = (%s)", (interaction.guild.id))
                    result = await cursor.fetchone()
                    if result is None:
                        return await interaction.response.send_message("**❌ Das Emojiquiz ist nicht in diesem Server aktiviert.**", ephemeral=True)
                    await cursor.execute("DELETE FROM eq WHERE guildID = (%s)", (interaction.guild.id))
                    return await interaction.response.send_message(f"**✅ Das Emojiquiz wurde in diesem Server ausgeschalten.**", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Emojiquiz(bot))