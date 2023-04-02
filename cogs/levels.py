import os
import discord
from discord import File
from discord.ext import commands, tasks
import random
import asyncio
from info import levelup_role_check, limit_characters
import math
from discord import app_commands
import typing
from easy_pil import Editor, Canvas, load_image_async, Font
from info import getcolour

async def checkstatus(self, guild):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT enabled FROM levelstatus WHERE guild_id = (%s)", (guild.id))
            enabled = await cursor.fetchone()
            if enabled == None:
                await cursor.execute("INSERT INTO levelstatus (guild_id, enabled) VALUES (%s, %s)", (guild.id, 0))
                return False
            if enabled[0] == 1:
                return True
            if enabled[0] == 0:
                return False

class levelsystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1.0, 5.0, commands.BucketType.user)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot:
            return
        bucket = self._cd.get_bucket(msg)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await checkstatus(self, msg.guild) == False:
                    return
                
                await cursor.execute(f"SELECT role_id FROM lb_rollen WHERE guild_id = {msg.guild.id}")
                lb_rollen = await cursor.fetchall()
                for r_id in lb_rollen:
                    rolle = msg.guild.get_role(int(r_id[0]))
                    if rolle:
                        if rolle in msg.author.roles:
                            return
                
                await cursor.execute(f"SELECT channel_id FROM lb_channel WHERE guild_id = {msg.guild.id}")
                lb_channel = await cursor.fetchall()
                for c_id in lb_channel:
                    if int(c_id[0]) == int(msg.channel.id):
                        return

                await cursor.execute("SELECT user_xp, user_level FROM levelsystem WHERE client_id = (%s) AND guild_id = (%s)", (msg.author.id, msg.guild.id))
                userdata = await cursor.fetchone()
                if userdata == None:
                    await cursor.execute("INSERT INTO levelsystem (client_id, user_xp, user_level, guild_id) VALUES (%s, %s, %s, %s)", (msg.author.id, 2, 0, msg.guild.id))
                    return

                xp_start = int(userdata[0])
                lvl_start = int(userdata[1])
                xp_end = 5 * (math.pow(lvl_start , 2)) + (50 * lvl_start) + 100
                newxp = random.randint(15, 30)
                #################################################################################################### XP BOOST
                
                await cursor.execute("SELECT status FROM xpboost WHERE guildID = (%s)", (msg.guild.id))
                xpboost = await cursor.fetchone()
                if xpboost == None:
                    pass
                if xpboost != None:
                    if xpboost[0] == 1:
                        newxp += newxp * 2
                    if xpboost[0] == 0:
                        pass
                
                #################################################################################################### XP BOOST
                await cursor.execute("UPDATE levelsystem SET user_xp = (%s) WHERE client_id = (%s) AND guild_id = (%s)", (int(userdata[0]) + newxp, msg.author.id, msg.guild.id))
                
                if xp_end < (xp_start + newxp):
                    await cursor.execute("UPDATE levelsystem SET user_level = (%s) WHERE client_id = (%s) AND guild_id = (%s)", (int(lvl_start) + 1, msg.author.id, msg.guild.id))
                    await cursor.execute("UPDATE levelsystem SET user_xp = (%s) WHERE client_id = (%s) AND guild_id = (%s)", (0 + 1, msg.author.id, msg.guild.id))

                    await cursor.execute(f"SELECT channel_id, message FROM levelup WHERE guild_id = {msg.guild.id}")
                    result = await cursor.fetchone()
                    nachricht = ""
                    neue_levelrolle = await levelup_role_check(self.bot, msg.guild, msg.author, int(lvl_start) + 1)
                    if result:
                        if result[1] != None:
                            nachricht += result[1].replace("%member", str(msg.author.mention)).replace("%level", str(int(lvl_start) + 1))
                        if result[1] == None or result[1] == "Normal":
                            if neue_levelrolle == None:
                                nachricht += f"🎉 Glückwunsch {msg.author.mention}! Du hast Level {int (lvl_start) + 1} erreicht."
                            else:
                                nachricht += f"🎉 Glückwunsch {msg.author.mention}! Du hast Level {int (lvl_start) + 1} erreicht.\nViel Spaß mit deiner neuen Levelrolle **{neue_levelrolle.name}**."
                        if result[0] == "Privat":
                            return await msg.author.send(nachricht)
                        if result[0] == None or result[0] == "Normal":
                            kanal = msg.channel
                        if result[0] != None and result[0] != "Normal":
                            channel_objct = msg.guild.get_channel(int(result[0]))
                            if channel_objct:
                                kanal = channel_objct
                            if channel_objct is None:
                                kanal = msg.channel
                        await kanal.send(nachricht)
                    if result == None:
                        if neue_levelrolle == None:
                            await msg.channel.send(f"🎉 Glückwunsch {msg.author.mention}! Du hast Level {int (lvl_start) + 1} erreicht.")
                            return
                        await msg.channel.send(f"🎉 Glückwunsch {msg.author.mention}! Du hast Level {int (lvl_start) + 1} erreicht.\nViel Spaß mit deiner neuen Levelrolle **{neue_levelrolle.name}**.")

    levelsystem = app_commands.Group(name='levelsystem', description='Nehme Einstellungen am Levelsystem vor.', guild_only=True)
    role = app_commands.Group(name='role', description='Nehme Einstellungen an Levelrollen vor oder lass sie dir alle anzeigen.', parent=levelsystem, guild_only=True)
    block = app_commands.Group(name='block', description='Entferne Rollen und Kanäle vom Levelsystem.', parent=levelsystem, guild_only=True)

    @role.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def add(self, interaction: discord.Interaction, level: int, role: discord.Role):
        """Setze eine neue Levelrolle."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await checkstatus(self, interaction.guild) == False:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
                    return
                if not int(level) > 0 or not int(level) < 101:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Die Stufe muss eine Zahl zwischen 1 und 100 sein.**", ephemeral=True)
                    return
                await cursor.execute("SELECT guild_id FROM levelroles WHERE level = (%s) AND roleid = (%s)", (level, role.id))
                r = await cursor.fetchone()
                if r is not None:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Für dieses Level wird bereits eine Rolle vergeben. Bitte wähle ein anderes Level.**", ephemeral=True)
                    return
                await cursor.execute("INSERT INTO levelroles(guild_id, roleid, level) VALUES (%s, %s, %s)", (interaction.guild.id, role.id, level))
                
                await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Die Rolle {role} wird nun beim Erreichen von Level {level} vergeben.**")

    @role.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def delete(self, interaction: discord.Interaction, role: discord.Role, level: int):
        """Entferne eine Levelrolle."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await checkstatus(self, interaction.guild) == False:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
                    return
                await cursor.execute("SELECT roleid FROM levelroles WHERE roleid = (%s) AND level = (%s) AND guild_id = (%s)", (role.id, level, interaction.guild.id))
                r = await cursor.fetchone()
                if r is None:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Diese Levelrolle existiert nicht.**", ephemeral=True)
                    return
                await cursor.execute("DELETE FROM levelroles WHERE guild_id = (%s) AND roleid = (%s) AND level = (%s)", (interaction.guild.id, role.id, level))
                
                await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Die Rolle {role} wird nun nicht mehr beim Erreichen von Level {level} vergeben.**")
    
    @role.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def list(self, interaction: discord.Interaction):
        """Liste von allen Levelrollen in diesem Server."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await checkstatus(self, interaction.guild) == False:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
                    return
                try:
                    await cursor.execute(f"SELECT roleid FROM levelroles WHERE guild_id = {interaction.guild.id}")
                    r = await cursor.fetchall()
                    if r is None:
                        return await interaction.response.send_message("<:v_kreuz:1049388811353858069> Ich habe auf diesem Server keine Levelrolle gefunden.", ephemeral=True)
                except:
                    return await interaction.response.send_message("<:v_kreuz:1049388811353858069> Ich habe auf diesem Server keine Levelrolle gefunden.", ephemeral=True)

                await cursor.execute(f"SELECT roleid, level FROM levelroles WHERE guild_id = {interaction.guild.id}")
                result = await cursor.fetchall()
                embed = discord.Embed(title="Alle Levelrollen", description="Hier kannst du alle Levelrollen auf diesem Server sehen.", color=await getcolour(self, interaction.user))
                a = 0
                for i in result:
                    t = ""
                    role = interaction.guild.get_role(int(i[0]))
                    level = i[1]
                    if role:
                        t += f"{role.mention}"
                    if role is None:
                        t = "Gelöschte Rolle"
                    role = interaction.guild.get_role(int(i[0]))
                    level = i[1]
                    a += 1

                    embed.add_field(name=f"Level {level}", value=f"Jeder, der Level {level} erreicht, erhält die Rolle {t}.")
                await asyncio.sleep(1)
                if a >= 1:
                    await interaction.response.send_message(embed=embed)
                if a < 1:
                    return await interaction.response.send_message("<:v_kreuz:1049388811353858069> Ich habe auf diesem Server keine Levelrolle gefunden.", ephemeral=True)
    
    @levelsystem.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def levelupmessage(self, interaction: discord.Interaction, modus: typing.Literal["Custom Nachricht", "Deaktivieren"], nachricht: str=None):
        """Nutze %level für das neue Level und %member für den Member."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await checkstatus(self, interaction.guild) == False:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
                    return
                if nachricht:
                    if len(nachricht) > 1000:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Deine Nachricht darf nicht größer als 1000 Charaktere sein.**", ephemeral=True)
                        return
                if modus == "Deaktivieren":
                    await cursor.execute("UPDATE levelup SET message = (%s) WHERE guild_id = (%s)", ("Normal", interaction.guild.id))
                    
                    return await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Levelupnachricht wurde erfolgreich zurückgesetzt.**")
                if nachricht == None:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du musst auch eine Nachricht angeben.**", ephemeral=True)
                    return
                await cursor.execute(f"SELECT message FROM levelup WHERE guild_id = {interaction.guild.id}")
                message = await cursor.fetchone()
                if message == None:
                    await cursor.execute("INSERT INTO levelup (guild_id, message) VALUES (%s, %s)", (interaction.guild.id, nachricht))
                    
                await cursor.execute("UPDATE levelup SET message = (%s) WHERE guild_id = (%s)", (nachricht, interaction.guild.id))
                
                await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Levelupnachricht wurde erfolgreich geändert.**")

    @levelsystem.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def levelupkanal(self, interaction: discord.Interaction, modus: typing.Literal["Kanal des Levelups","Private Nachricht","Deaktivieren","Spezieller Kanal (Kanalangabe benötigt)"], kanal: discord.TextChannel=None):
        """Lege einen Levelup-Kanal fest."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await checkstatus(self, interaction.guild) == False:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
                    return
                await cursor.execute(f"SELECT channel_id FROM levelup WHERE guild_id = {interaction.guild.id}")
                channel = await cursor.fetchone()

                if modus == "Deaktivieren":
                    if channel == None:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Hier ist kein Levelupkanal eingerichtet.", ephemeral=True)
                        return
                    await cursor.execute("UPDATE levelup SET channel_id = (%s) WHERE guild_id = (%s)", ("Normal", interaction.guild.id))
                    
                    return await interaction.response.send_message("**<:v_haken:1048677657040134195> Der Levelupkanal wurde erfolgreich zurückgesetzt.**")

                if modus == "Kanal des Levelups":
                    if channel == None:
                        await cursor.execute("INSERT INTO levelup (guild_id, channel_id) VALUES (%s, %s)", (interaction.guild.id, "Normal"))
                        
                    await cursor.execute("UPDATE levelup SET channel_id = (%s) WHERE guild_id = (%s)", ("Normal", interaction.guild.id))
                    return await interaction.response.send_message("**<:v_haken:1048677657040134195> Der Levelupkanal wurde erfolgreich geändert.**")
                 
                if modus == "Private Nachricht":
                    if channel == None:
                        await cursor.execute("INSERT INTO levelup (guild_id, channel_id) VALUES (%s, %s)", (interaction.guild.id, "Privat"))
                        
                    await cursor.execute("UPDATE levelup SET channel_id = (%s) WHERE guild_id = (%s)", ("Privat", interaction.guild.id))
                    return await interaction.response.send_message("**<:v_haken:1048677657040134195> Der Levelupkanal wurde erfolgreich geändert.**")

                if modus == "Spezieller Kanal (Kanalangabe benötigt)":
                    if kanal == None:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du musst auch einen Kanal angeben.**", ephemeral=True)
                        return
                    if channel == None:
                        await cursor.execute("INSERT INTO levelup (guild_id, channel_id) VALUES (%s, %s)", (interaction.guild.id, kanal.id))
                        
                    await cursor.execute("UPDATE levelup SET channel_id = (%s) WHERE guild_id = (%s)", (kanal.id, interaction.guild.id))
                    
                    return await interaction.response.send_message("**<:v_haken:1048677657040134195> Der Levelupkanal wurde erfolgreich geändert.**")

    @block.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def channel(self, interaction: discord.Interaction, modus: typing.Literal["Der Blacklist hinzufügen","Von der Blacklist entfernen"], kanal: discord.abc.GuildChannel):
        """Entferne einen Kanal vom Levelsystem."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await checkstatus(self, interaction.guild) == False:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
                    return
                await cursor.execute("SELECT channel_id FROM lb_channel WHERE guild_id = (%s) AND channel_id = (%s)", (interaction.guild.id, kanal.id))
                channel = await cursor.fetchone()

                if modus == "Der Blacklist hinzufügen":
                    if channel:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Der Kanal ist bereits auf der Blacklist.**", ephemeral=True)
                        return
                    await cursor.execute("INSERT INTO lb_channel (channel_id, guild_id) VALUES (%s,%s)", (kanal.id, interaction.guild.id))
                    
                    await interaction.response.send_message("**<:v_haken:1048677657040134195> Der Kanal ist nun auf der Blacklist.**")

                if modus == "Von der Blacklist entfernen":
                    if channel == None:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Der Kanal ist nicht auf der Blacklist.**", ephemeral=True)
                        return
                    await cursor.execute("DELETE FROM lb_channel WHERE channel_id = (%s) AND guild_id = (%s)", (kanal.id, interaction.guild.id))
                    
                    await interaction.response.send_message("**<:v_haken:1048677657040134195> Der Kanal ist nun nicht mehr auf der Blacklist.**")

    @block.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def rolle(self, interaction: discord.Interaction, modus: typing.Literal["Der Blacklist hinzufügen","Von der Blacklist entfernen"], rolle: discord.Role):
        """Entferne eine Rolle vom Levelsystem."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await checkstatus(self, interaction.guild) == False:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
                    return
                await cursor.execute("SELECT role_id FROM lb_rollen WHERE guild_id = (%s) AND role_id = (%s)", (interaction.guild.id, rolle.id))
                r = await cursor.fetchone()

                if modus == "Der Blacklist hinzufügen":
                    if r:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Die Rolle ist bereits auf der Blacklist.**", ephemeral=True)
                        return
                    await cursor.execute("INSERT INTO lb_rollen (role_id, guild_id) VALUES (%s,%s)", (rolle.id, interaction.guild.id))
                    await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Rolle ist nun auf der Blacklist.**")

                if modus == "Von der Blacklist entfernen":
                    if r == None:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Die Rolle ist nicht auf der Blacklist.**", ephemeral=True)
                        return
                    await cursor.execute("DELETE FROM lb_rollen WHERE role_id = (%s) AND guild_id = (%s)", (rolle.id, interaction.guild.id))
                    await interaction.response.send_message("**<:v_haken:1048677657040134195> Die Rolle ist nun nicht mehr auf der Blacklist.**")
    
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def rank(self, interaction: discord.Interaction, member: discord.Member=None):
        """Dieser Befehl zeigt dein Level und deine Erfahrungspunkte."""
        if await checkstatus(self, interaction.guild) == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
        await interaction.response.defer(thinking=True)
        if member == None:
            member = interaction.user

        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT user_xp, user_level FROM levelsystem WHERE client_id = (%s) AND guild_id = (%s)", (member.id, interaction.guild.id))
                result = await cursor.fetchone()
                if result == None or result == False:
                    if member == None:
                        return await interaction.followup.send(f"**<:v_kreuz:1049388811353858069> Du bist noch nicht eingestuft. Sende erst noch ein paar Nachrichten.**", ephemeral=True)
                    return await interaction.followup.send(f"**<:v_kreuz:1049388811353858069> {member} ist noch nicht eingestuft. Er/Sie muss erst noch ein paar Nachrichten.**", ephemeral=True)
                try:
                    xp_start = result[0]
                    lvl_start = result[1]
                    xp_end = round(5 * (math.pow(lvl_start , 2)) + (50 * lvl_start) + 100)
                    multiplication = 100 / xp_end
                    prozent = round(xp_start) * multiplication
                except:
                    if member == None:
                        return await interaction.followup.send(f"**<:v_kreuz:1049388811353858069> Du bist noch nicht eingestuft. Sende erst noch ein paar Nachrichten.**", ephemeral=True)
                    return await interaction.followup.send(f"**<:v_kreuz:1049388811353858069> {member} ist noch nicht eingestuft. Er/Sie muss erst noch ein paar Nachrichten.**", ephemeral=True)
                await cursor.execute(f"SELECT client_id FROM levelsystem WHERE guild_id = {interaction.guild.id} ORDER BY user_level DESC")
                result = await cursor.fetchall()
                a = 0
                for u in result:
                    a += 1
                    if str(member.id) == str(u[0]):
                        break

                user = interaction.guild.get_member(member.id)
                await cursor.execute("SELECT status FROM premium WHERE userID = (%s)", (user.id))
                status = await cursor.fetchone()
                if status == None:
                    user = interaction.guild.get_member(member.id)
                    ## Rank card
                    if prozent > 0:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_0%.png")
                    if prozent > 10:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_10%.png")
                    if prozent > 20:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_20%.png")
                    if prozent > 30:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_30%.png")
                    if prozent > 40:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_40%.png")
                    if prozent > 50:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_50%.png")
                    if prozent > 60:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_60%.png")
                    if prozent > 70:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_70%.png")
                    if prozent > 80:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_80%.png")
                    if prozent > 90:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_90%.png")
                    if prozent >= 100:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_100%.png")
                    profile = await load_image_async(str(member.avatar))

                    profile = Editor(profile).resize((125, 125)).circle_image()
                    square = Canvas((300, 300), "#06FFBF")
                    square = Editor(square)
                    square.rotate(30, expand=True)
                    background.paste(profile.image, (32, 43))
                    poppins = Font.poppins("bold", size=40)
                    poppins_small = Font.poppins("bold", size=30)
                    background.text((165, 65), limit_characters(str(member), 13), color="white", font=poppins)
                    background.text((770, 195), f"{xp_start}/{round(xp_end)}", color="white", font=poppins_small)
                    background.text((830, 61), f"{lvl_start}", color="white", font=poppins_small)
                    background.text((300, 123), f"{a}", color="white", font=poppins)
                    file = File(fp=background.image_bytes, filename="rang.png")
                    return await interaction.followup.send(file=file)
                if status[0] == 0:
                    user = interaction.guild.get_member(member.id)
                    ## Rank card
                    if prozent > 0:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_0%.png")
                    if prozent > 10:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_10%.png")
                    if prozent > 20:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_20%.png")
                    if prozent > 30:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_30%.png")
                    if prozent > 40:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_40%.png")
                    if prozent > 50:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_50%.png")
                    if prozent > 60:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_60%.png")
                    if prozent > 70:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_70%.png")
                    if prozent > 80:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_80%.png")
                    if prozent > 90:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_90%.png")
                    if prozent >= 100:
                        background = Editor("Rank_Bilder/Rank_Image_Entwurf_100%.png")
                    profile = await load_image_async(str(member.avatar))

                    profile = Editor(profile).resize((125, 125)).circle_image()
                    square = Canvas((300, 300), "#06FFBF")
                    square = Editor(square)
                    square.rotate(30, expand=True)
                    background.paste(profile.image, (32, 43))
                    poppins = Font.poppins("bold", size=40)
                    poppins_small = Font.poppins("bold", size=30)
                    background.text((165, 65), limit_characters(str(member), 13), color="white", font=poppins)
                    background.text((770, 195), f"{xp_start}/{round(xp_end)}", color="white", font=poppins_small)
                    background.text((830, 61), f"{lvl_start}", color="white", font=poppins_small)
                    background.text((300, 123), f"{a}", color="white", font=poppins)
                    file = File(fp=background.image_bytes, filename="rang.png")
                    return await interaction.followup.send(file=file)
                if status[0] == 1:
                    if os.path.exists(f"Rank_Bilder/{member.id}.png"):
                        background = Editor(f"Rank_Bilder/{member.id}.png")
                        profile = await load_image_async(str(member.avatar))

                        profile = Editor(profile).resize((125, 125)).circle_image()
                        square = Canvas((300, 300), "#FFFFFF")
                        square = Editor(square)
                        square.rotate(30, expand=True)
                        background.paste(profile.image, (32, 43))

                        # Progress-Bar Parameter
                        xp_progress = xp_start
                        xp_needed = xp_end
                        progress_bar_width = 800
                        progress_bar_height = 40
                        progress_bar_x = 100
                        progress_bar_y = 190

                        # Zeichnen des Fortschrittsbalkens, der proportional zum XP-Fortschritt gefüllt ist
                        await cursor.execute("SELECT farbe FROM embedfarben WHERE userID = (%s)", (user.id))
                        farbe = await cursor.fetchone()
                        if farbe == None:
                            f = "orange"
                        else:
                            f = f"#{farbe[0]}"
                        progress_bar_fill_width = int(progress_bar_width * xp_progress / xp_needed)
                        background.rectangle(position=(progress_bar_x, progress_bar_y), outline="white", width=progress_bar_width, height=progress_bar_height)
                        background.rectangle(position=(progress_bar_x, progress_bar_y), fill=f, outline=None, width=progress_bar_fill_width, height=40)

                        poppins = Font.poppins("bold", size=40)
                        poppins_small = Font.poppins("bold", size=30)

                        # Texte
                        background.text((165, 65), limit_characters(str(member), 13), color="white", font=poppins)
                        background.text((750, 61), f"Level {lvl_start}", color="white", font=poppins_small)
                        background.text((180, 123), f"Rang {a}", color="white", font=poppins)
                        background.text((750, 95), f"{xp_start}/{xp_end}", color="white", font=poppins_small)

                        file = File(fp=background.image_bytes, filename="rang.png")
                        return await interaction.followup.send(file=file)
                    else:
                        user = interaction.guild.get_member(member.id)
                        ## Rank card
                        if prozent > 0:
                            background = Editor("Rank_Bilder/Rank_Image_Entwurf_0%.png")
                        if prozent > 10:
                            background = Editor("Rank_Bilder/Rank_Image_Entwurf_10%.png")
                        if prozent > 20:
                            background = Editor("Rank_Bilder/Rank_Image_Entwurf_20%.png")
                        if prozent > 30:
                            background = Editor("Rank_Bilder/Rank_Image_Entwurf_30%.png")
                        if prozent > 40:
                            background = Editor("Rank_Bilder/Rank_Image_Entwurf_40%.png")
                        if prozent > 50:
                            background = Editor("Rank_Bilder/Rank_Image_Entwurf_50%.png")
                        if prozent > 60:
                            background = Editor("Rank_Bilder/Rank_Image_Entwurf_60%.png")
                        if prozent > 70:
                            background = Editor("Rank_Bilder/Rank_Image_Entwurf_70%.png")
                        if prozent > 80:
                            background = Editor("Rank_Bilder/Rank_Image_Entwurf_80%.png")
                        if prozent > 90:
                            background = Editor("Rank_Bilder/Rank_Image_Entwurf_90%.png")
                        if prozent >= 100:
                            background = Editor("Rank_Bilder/Rank_Image_Entwurf_100%.png")
                        profile = await load_image_async(str(member.avatar))

                        profile = Editor(profile).resize((125, 125)).circle_image()
                        square = Canvas((300, 300), "#06FFBF")
                        square = Editor(square)
                        square.rotate(30, expand=True)
                        background.paste(profile.image, (32, 43))
                        poppins = Font.poppins("bold", size=40)
                        poppins_small = Font.poppins("bold", size=30)
                        background.text((165, 65), limit_characters(str(member), 13), color="white", font=poppins)
                        background.text((770, 195), f"{xp_start}/{round(xp_end)}", color="white", font=poppins_small)
                        background.text((830, 61), f"{lvl_start}", color="white", font=poppins_small)
                        background.text((300, 123), f"{a}", color="white", font=poppins)
                        file = File(fp=background.image_bytes, filename="rang.png")
                        return await interaction.followup.send(file=file)
              
    @levelsystem.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def status(self, interaction: discord.Interaction, modus: typing.Literal["An","Aus"]):
        """Aktiviert/Deaktiviert das Levelsystem auf deinem Server."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if modus == "An":
                    await cursor.execute(f"SELECT enabled FROM levelstatus WHERE guild_id = {interaction.guild.id}")
                    enabled = await cursor.fetchone()
                    if enabled == None:
                        await cursor.execute(f"UPDATE levelstatus SET enabled = 1 WHERE guild_id = {interaction.guild.id}")
                        
                        await interaction.response.send_message("**<:v_haken:1048677657040134195> Das Levelsystem ist jetzt auf diesem Server aktiviert.**")
                        return
                    if enabled[0] == 1:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Levelsystem ist hier bereits aktiviert.**", ephemeral=True)
                        return
                    if enabled[0] == 0:
                        await cursor.execute(f"UPDATE levelstatus SET enabled = 1 WHERE guild_id = {interaction.guild.id}")
                        
                        await interaction.response.send_message("**<:v_haken:1048677657040134195> Das Levelsystem ist jetzt auf diesem Server aktiviert.**")
                        return
                if modus == "Aus":
                    await cursor.execute(f"SELECT enabled FROM levelstatus WHERE guild_id = {interaction.guild.id}")
                    enabled = await cursor.fetchone()
                    if enabled == None:
                        await cursor.execute(f"UPDATE levelstatus SET enabled = 0 WHERE guild_id = {interaction.guild.id}")
                        
                        await interaction.response.send_message("**<:v_haken:1048677657040134195> Das Levelsystem ist jetzt auf diesem Server deaktiviert.**")
                        return
                    if enabled[0] == 1:
                        await cursor.execute(f"UPDATE levelstatus SET enabled = 0 WHERE guild_id = {interaction.guild.id}")
                        
                        await interaction.response.send_message("**<:v_haken:1048677657040134195> Das Levelsystem ist jetzt auf diesem Server deaktiviert.**")
                        return
                    if enabled[0] == 0:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Levelsystem ist hier bereits deaktiviert.**", ephemeral=True)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def setlevel(self, interaction: discord.Interaction, member: discord.Member, level: int):
        """Bearbeite das Level eines Nutzers."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await checkstatus(self, interaction.guild) == False:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
                    return
                await cursor.execute("SELECT user_xp, user_level FROM levelsystem WHERE guild_id = (%s) AND client_id = (%s)", (interaction.guild.id, member.id))
                result = await cursor.fetchone()
                if result is None:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Der Nutzer hat bisher noch keinen Rang. Er muss erst ein paar Nachrichten schreiben.**", ephemeral=True)
                    return
                await cursor.execute("UPDATE levelsystem SET user_level = (%s) WHERE guild_id = (%s) AND client_id = (%s)", (level, interaction.guild.id, member.id))
                await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Der Benutzer {member.mention} ist nun Level {level}.**")

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def xpboost(self, interaction: discord.Interaction, status: typing.Literal["Anschalten (2x)", "Ausschalten (1x)"]):
        """Starte einen XP Boost auf deinem Server."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await checkstatus(self, interaction.guild) == False:
                    await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
                    return
                
                await cursor.execute("SELECT status FROM xpboost WHERE guildID = (%s)", (interaction.guild.id))
                result = await cursor.fetchone()
                if result == None:
                    if status == "Anschalten (2x)":
                        await cursor.execute("INSERT INTO xpboost (status, guildID) VALUES (%s, %s)", (1, interaction.guild.id))
                        return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Der XP Boost wurde auf diesem Server aktiviert.**")
                    if status == "Ausschalten (1x)":
                        return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Hier ist kein XP Boost aktiviert.**", ephemeral=True)
                if result != None:
                    if status == "Anschalten (2x)":
                        if result[0] == 1:
                            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Hier ist der XP Boost bereits aktiviert.**", ephemeral=True)
                        await cursor.execute("UPDATE xpboost SET status = (%s) WHERE guildID = (%s)", (1, interaction.guild.id))
                        return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Der XP Boost wurde auf diesem Server aktiviert.**")
                    if status == "Ausschalten (1x)":
                        if result[0] == 0:
                            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Hier ist der XP Boost bereits deaktiviert.**", ephemeral=True)
                        await cursor.execute("UPDATE xpboost SET status = (%s) WHERE guildID = (%s)", (0, interaction.guild.id))
                        return await interaction.response.send_message(f"**<:v_haken:1048677657040134195> Der XP Boost wurde auf diesem Server deaktiviert.**")
                
async def setup(bot):
    await bot.add_cog(levelsystem(bot))