import os
import discord
from discord import File
from discord.ext import commands, tasks
import random
import asyncio
from utils.utils import levelup_role_check, limit_characters
import math
from discord import app_commands
import typing
from easy_pil import Editor, Canvas, load_image_async, Font
from utils.utils import getcolour, haspremium_forserver, haspremium
from utils.MongoDB import getMongoDataBase

async def checkstatus(self, guild):
    db = getMongoDataBase()
    enabled = await db['levelstatus'].find_one({"guildID": str(guild.id)})
    
    if enabled == None:
        await db['levelstatus'].insert_one({"guildID": str(guild.id), "status": "0"})
        return False
    
    return enabled['status'] == "1"

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
        
        if await checkstatus(self, msg.guild) == False:
            return 
        
        db = getMongoDataBase()
        
        lb_rollen = await db['lb_rollen'].find({"guild_id": str(msg.guild.id)}).to_list(length=None)
        for r_id in lb_rollen:
            rolle = msg.guild.get_role(int(r_id["role_id"]))
            if rolle:
                if rolle in msg.author.roles:
                    return
                
        lb_channel = await db['lb_channel'].find({"guild_id": str(msg.guild.id)}).to_list(length=None)
        
        for c_id in lb_channel:
            if int(c_id["channel_id"]) == int(msg.channel.id):
                return
        userdata = await db['levelsystem'].find_one({"client_id": str(msg.author.id), "guild_id": str(msg.guild.id)})
        
        if userdata == None:
            await db['levelsystem'].insert_one({"client_id": str(msg.author.id), "guild_id": str(msg.guild.id), "user_xp": 0, "user_level": 0})
            return

        xp_start = int(userdata["user_xp"])
        lvl_start = int(userdata["user_level"])
        xp_end = 5 * (math.pow(lvl_start , 2)) + (50 * lvl_start) + 100
        newxp = random.randint(15, 30)
        #################################################################################################### XP BOOST
        
        xpboost = await db['xpboost'].find_one({"guild_id": str(msg.guild.id)})
        if xpboost == None:
            pass
        if xpboost != None:
            if xpboost["status"] == 1:
                newxp += newxp * 2
                
        #################################################################################################### XP BOOST
        await db['levelsystem'].update_one({"client_id": str(msg.author.id), "guild_id": str(msg.guild.id)}, {"$set": {"user_xp": xp_start + newxp}})
        
        if xp_end < (xp_start + newxp):
            await db['levelsystem'].update_one({"client_id": str(msg.author.id), "guild_id": str(msg.guild.id)}, {"$set": {"user_level": lvl_start + 1}})
            await db['levelsystem'].update_one({"client_id": str(msg.author.id), "guild_id": str(msg.guild.id)}, {"$set": {"user_xp": 1}})
            result = await db["levelup"].find_one({"guild_id": str(msg.guild.id)})

            nachricht = ""
            neue_levelrolle = await levelup_role_check(self.bot, msg.guild, msg.author, int(lvl_start) + 1)
            
            if result["channel_id"] == None or result["channel_id"] == "":
                if neue_levelrolle == None:
                    return await msg.channel.send(f"🎉 Glückwunsch {msg.author.mention}! Du hast Level {int (lvl_start) + 1} erreicht.")
                return await msg.channel.send(f"🎉 Glückwunsch {msg.author.mention}! Du hast Level {int (lvl_start) + 1} erreicht.\nViel Spaß mit deiner neuen Levelrolle **{neue_levelrolle.name}**")
            
            if 'message' in result and result['message'] != "":
                nachricht = result["message"].replace("%member", str(msg.author.mention)).replace("%level", str(int(lvl_start) + 1))
            else:
                if neue_levelrolle == None:
                    nachricht = f"🎉 Glückwunsch {msg.author.mention}! Du hast Level {int (lvl_start) + 1} erreicht."
                else:
                    nachricht = f"🎉 Glückwunsch {msg.author.mention}! Du hast Level {int (lvl_start) + 1} erreicht.\nViel Spaß mit deiner neuen Levelrolle **{neue_levelrolle.name}**."
            
            if result["channel_id"] == "Privat":
                return await msg.author.send(nachricht)
            
            if result["channel_id"] == None or result["channel_id"] == "Normal":
                kanal = msg.channel
            else:
                kanal = await msg.guild.fetch_channel(int(result["channel_id"]))
                
                if kanal == None:
                    kanal = msg.channel
                    
            await kanal.send(nachricht)

    levelsystem = app_commands.Group(name='levelsystem', description='Nehme Einstellungen am Levelsystem vor.', guild_only=True)
    role = app_commands.Group(name='role', description='Nehme Einstellungen an Levelrollen vor oder lass sie dir alle anzeigen.', parent=levelsystem, guild_only=True)
    block = app_commands.Group(name='block', description='Entferne Rollen und Kanäle vom Levelsystem.', parent=levelsystem, guild_only=True)

    @role.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def add(self, interaction: discord.Interaction, level: int, role: discord.Role):
        """Setze eine neue Levelrolle."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        existing = await db['levelroles'].count_documents({"guild_id": str(str(interaction.guild.id))})

        if await checkstatus(self, interaction.guild) == False:
            await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
            return
        
        premium_status = await haspremium_forserver(self, interaction.guild)
        
        
        if not premium_status and existing >= 5:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Du kannst keine weiteren Levelrollen erstellen, da du das Limit erreicht hast**")
        
        if not int(level) > 0 or not int(level) < 101:
            await interaction.followup.send("**<:v_x:1264270921452224562> Die Stufe muss eine Zahl zwischen 1 und 100 sein.**", ephemeral=True)
            return
        
        r = await db['levelroles'].find_one({"guild_id": str(str(interaction.guild.id)), "level": level})
        
        if r is not None:
            await interaction.followup.send("**<:v_x:1264270921452224562> Für dieses Level wird bereits eine Rolle vergeben. Bitte wähle ein anderes Level.**", ephemeral=True)
            return
        
        await db["levelroles"].insert_one({"guild_id": str(str(interaction.guild.id)), "roleid": str(role.id), "level": level})
        
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Die Rolle {role} wird nun beim Erreichen von Level {level} vergeben.**")

    @role.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def delete(self, interaction: discord.Interaction, role: discord.Role, level: int):
        """Entferne eine Levelrolle."""
        
        await interaction.response.defer()
        
        if await checkstatus(self, interaction.guild) == False:
            await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
            return
        
        db = getMongoDataBase()
        
        r = await db['levelroles'].find_one({"guild_id": str(str(interaction.guild.id)), "roleid": str(role.id), "level": level})
        if r is None:
            await interaction.followup.send("**<:v_x:1264270921452224562> Diese Levelrolle existiert nicht.**", ephemeral=True)
            return
        
        await db['levelroles'].delete_one({"guild_id": str(str(interaction.guild.id)), "roleid": str(role.id), "level": level})
        
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Die Rolle {role} wird nun nicht mehr beim Erreichen von Level {level} vergeben.**")
    
    @role.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def list(self, interaction: discord.Interaction):
        """Liste von allen Levelrollen in diesem Server."""
        
        await interaction.response.defer()
        
        if await checkstatus(self, interaction.guild) == False:
            await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
            return
        
        db = getMongoDataBase()
        
        try:
            r = await db['levelroles'].find({"guild_id": str(str(interaction.guild.id))}).to_list(length=None)
            if r is None:
                return await interaction.followup.send("<:v_x:1264270921452224562> Ich habe auf diesem Server keine Levelrolle gefunden.", ephemeral=True)
        except:
            return await interaction.followup.send("<:v_x:1264270921452224562> Ich habe auf diesem Server keine Levelrolle gefunden.", ephemeral=True)


        result = await db['levelroles'].find({"guild_id": str(interaction.guild.id)}).sort([("level", 1)]).to_list(length=None)
        embed = discord.Embed(title="Alle Levelrollen", description="Hier kannst du alle Levelrollen auf diesem Server sehen.", color=await getcolour(self, interaction.user))

        if len(result) == 0:
            return await interaction.followup.send("<:v_x:1264270921452224562> Ich habe auf diesem Server keine Levelrolle gefunden.", ephemeral=True)

        for levelRole in result:
            role = interaction.guild.get_role(int(levelRole["roleid"]))
            level = levelRole['level']
            role_name = role.mention if role else "Gelöschte Rolle"
            
            embed.add_field(name=f"Level {level}", value=f"Jeder, der Level {level} erreicht, erhält die Rolle {role_name}.", inline=False)

        await interaction.followup.send(embed=embed)

    @levelsystem.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def levelupmessage(self, interaction: discord.Interaction, modus: typing.Literal["Custom Nachricht", "Deaktivieren"], nachricht: str=None):
        """Nutze %level für das neue Level und %member für den Member."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        if await checkstatus(self, interaction.guild) == False:
            await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
            return
        if nachricht:
            if len(nachricht) > 1000:
                await interaction.followup.send("**<:v_x:1264270921452224562> Deine Nachricht darf nicht größer als 1000 Charaktere sein.**", ephemeral=True)
                return
        if modus == "Deaktivieren":
            await db['levelup'].delete_one({"guild_id": str(str(interaction.guild.id))})
            
            return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Levelupnachricht wurde erfolgreich zurückgesetzt.**")
        if nachricht == None:
            await interaction.followup.send("**<:v_x:1264270921452224562> Du musst auch eine Nachricht angeben.**", ephemeral=True)
            return
        
        message = await db["levelup"].find_one({"guild_id": str(interaction.guild.id)})
        
        if message == None:
            await db["levelup"].insert_one({"guild_id": str(interaction.guild.id), "message": nachricht, "channel_id": "Normal"})
        else:
            await db["levelup"].update_one({"guild_id": str(interaction.guild.id)}, {"$set": {"message": nachricht}})
        
        await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Levelupnachricht wurde erfolgreich geändert.**")

    @levelsystem.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def levelupkanal(self, interaction: discord.Interaction, modus: typing.Literal["Kanal des Levelups","Private Nachricht","Deaktivieren","Spezieller Kanal (Kanalangabe benötigt)"], kanal: discord.TextChannel=None):
        """Lege einen Levelup-Kanal fest."""
        
        await interaction.response.defer()
        
        if await checkstatus(self, interaction.guild) == False:
            await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
            return
        
        db = getMongoDataBase()
        
        
        channel = await db['levelup'].find_one({"guild_id": str(interaction.guild.id)})

        if modus == "Deaktivieren":
            if channel == None:
                await interaction.followup.send("**<:v_x:1264270921452224562> Hier ist kein Levelupkanal eingerichtet.", ephemeral=True)
                return
            await db['levelup'].delete_one({"guild_id": str(interaction.guild.id)})
            
            return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Der Levelupkanal wurde erfolgreich zurückgesetzt.**")

        if modus == "Kanal des Levelups":
            if channel == None:
                await db["levelup"].insert_one({"guild_id": str(interaction.guild.id), "channel_id": "Normal"})
                
            await db["levelup"].update_one({"guild_id": str(interaction.guild.id)}, {"$set": {"channel_id": "Normal"}})
                
            return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Der Levelupkanal wurde erfolgreich geändert.**")
                 
        if modus == "Private Nachricht":
            if channel == None:
                await db["levelup"].insert_one({"guild_id": str(interaction.guild.id), "channel_id": "Privat"})
                
            await db["levelup"].update_one({"guild_id": str(interaction.guild.id)}, {"$set": {"channel_id": "Privat"}})
                
            return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Der Levelupkanal wurde erfolgreich geändert.**")

        if modus == "Spezieller Kanal (Kanalangabe benötigt)":
            if kanal == None:
                await interaction.followup.send("**<:v_x:1264270921452224562> Du musst auch einen Kanal angeben.**", ephemeral=True)
                return
            if channel == None:
                await db["levelup"].insert_one({"guild_id": str(interaction.guild.id), "channel_id": str(kanal.id)})
                
                
            await db["levelup"].update_one({"guild_id": str(interaction.guild.id)}, {"$set": {"channel_id": str(kanal.id)}})
            
            return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Der Levelupkanal wurde erfolgreich geändert.**")

    @block.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def channel(self, interaction: discord.Interaction, modus: typing.Literal["Der Blacklist hinzufügen","Von der Blacklist entfernen"], kanal: discord.abc.GuildChannel):
        """Entferne einen Kanal vom Levelsystem."""
        
        await interaction.response.defer()
        
        if await checkstatus(self, interaction.guild) == False:
            await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
            return
        
        db = getMongoDataBase()
        
        
        channel = await db['lb_channel'].find_one({"guild_id": str(interaction.guild.id), "channel_id": str(kanal.id)})

        if modus == "Der Blacklist hinzufügen":
            if channel:
                await interaction.followup.send("**<:v_x:1264270921452224562> Der Kanal ist bereits auf der Blacklist.**", ephemeral=True)
                return
            await db["lb_channel"].insert_one({"guild_id": str(interaction.guild.id), "channel_id": str(kanal.id)})
            
            await interaction.followup.send("**<:v_checkmark:1264271011818242159> Der Kanal ist nun auf der Blacklist.**")

        if modus == "Von der Blacklist entfernen":
            if channel == None:
                await interaction.followup.send("**<:v_x:1264270921452224562> Der Kanal ist nicht auf der Blacklist.**", ephemeral=True)
                return
            await db['lb_channel'].delete_one({"guild_id": str(interaction.guild.id), "channel_id": str(kanal.id)})
            
            await interaction.followup.send("**<:v_checkmark:1264271011818242159> Der Kanal ist nun nicht mehr auf der Blacklist.**")

    @block.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def rolle(self, interaction: discord.Interaction, modus: typing.Literal["Der Blacklist hinzufügen","Von der Blacklist entfernen"], rolle: discord.Role):
        """Entferne eine Rolle vom Levelsystem."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        if await checkstatus(self, interaction.guild) == False:
            await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
            return
        
        r = await db['lb_rollen'].find_one({"guild_id": str(interaction.guild.id), "role_id": str(rolle.id)})

        if modus == "Der Blacklist hinzufügen":
            if r:
                await interaction.followup.send("**<:v_x:1264270921452224562> Die Rolle ist bereits auf der Blacklist.**", ephemeral=True)
                return
            await db["lb_rollen"].insert_one({"guild_id": str(interaction.guild.id), "role_id": str(rolle.id)})
            await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Rolle ist nun auf der Blacklist.**")

        if modus == "Von der Blacklist entfernen":
            if r == None:
                await interaction.followup.send("**<:v_x:1264270921452224562> Die Rolle ist nicht auf der Blacklist.**", ephemeral=True)
                return
            await db['lb_rollen'].delete_one({"guild_id": str(interaction.guild.id), "role_id": str(rolle.id)})
            await interaction.followup.send("**<:v_checkmark:1264271011818242159> Die Rolle ist nun nicht mehr auf der Blacklist.**")
    
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def rang(self, interaction: discord.Interaction, member: discord.Member=None):
        """Dieser Befehl zeigt dein Level und deine Erfahrungspunkte."""
        
        await interaction.response.defer()
        
        if await checkstatus(self, interaction.guild) == False:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
        
        if member == None:
            member = interaction.user

        db = getMongoDataBase()
        
        result = await db['levelsystem'].find_one({"guild_id": str(interaction.guild.id), "client_id": str(member.id)})

        if result == None:
            return await interaction.followup.send(f"**<:v_x:1264270921452224562> {member} ist noch nicht eingestuft. Er/Sie muss erst noch ein paar Nachrichten senden.**", ephemeral=True)
        try:
            xp_start = result["user_xp"]
            lvl_start = result["user_level"]
            xp_end = round(5 * (math.pow(lvl_start , 2)) + (50 * lvl_start) + 100)
            multiplication = 100 / xp_end
            prozent = round(xp_start) * multiplication
        except Exception as e:
            print(e)
            return await interaction.followup.send(f"**<:v_x:1264270921452224562> {member} ist noch nicht eingestuft. Er/Sie muss erst noch ein paar Nachrichten senden.**", ephemeral=True)
        
        result = await db['levelsystem'].find({"guild_id": str(interaction.guild.id)}).sort([("user_level", -1), ("user_xp", -1)]).to_list(length=None)
        rang = next((i + 1 for i, user in enumerate(result) if user['client_id'] == str(member.id)), None)


        user = await interaction.guild.fetch_member(member.id)
        
        status = await haspremium(self, user)
                    
        if not status:
            user = await interaction.guild.fetch_member(member.id)
            ## Rank card
            if prozent >= 0:
                background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_0%.png")
            if prozent > 10:
                background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_10%.png")
            if prozent > 20:
                background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_20%.png")
            if prozent > 30:
                background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_30%.png")
            if prozent > 40:
                background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_40%.png")
            if prozent > 50:
                background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_50%.png")
            if prozent > 60:
                background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_60%.png")
            if prozent > 70:
                background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_70%.png")
            if prozent > 80:
                background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_80%.png")
            if prozent > 90:
                background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_90%.png")
            if prozent >= 100:
                background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_100%.png")
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
            background.text((300, 123), f"{rang}", color="white", font=poppins)
            file = File(fp=background.image_bytes, filename="rang.png")
            return await interaction.followup.send(file=file)
        else:
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

                farbe = None
                
                farbe = f"#{getcolour(self, user)}"
                progress_bar_fill_width = int(progress_bar_width * xp_progress / xp_needed)
                background.rectangle(position=(progress_bar_x, progress_bar_y), outline="white", width=progress_bar_width, height=progress_bar_height)
                background.rectangle(position=(progress_bar_x, progress_bar_y), fill=farbe, outline=None, width=progress_bar_fill_width, height=40)

                poppins = Font.poppins("bold", size=40)
                poppins_small = Font.poppins("bold", size=30)

                # Texte
                background.text((165, 65), limit_characters(str(member), 13), color="white", font=poppins)
                background.text((750, 61), f"Level {lvl_start}", color="white", font=poppins_small)
                background.text((180, 123), f"Rang {rang}", color="white", font=poppins)
                background.text((750, 95), f"{xp_start}/{xp_end}", color="white", font=poppins_small)

                file = File(fp=background.image_bytes, filename="rang.png")
                return await interaction.followup.send(file=file)
            else:
                user = interaction.guild.get_member(member.id)
                ## Rank card
                if prozent > 0:
                    background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_0%.png")
                if prozent > 10:
                    background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_10%.png")
                if prozent > 20:
                    background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_20%.png")
                if prozent > 30:
                    background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_30%.png")
                if prozent > 40:
                    background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_40%.png")
                if prozent > 50:
                    background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_50%.png")
                if prozent > 60:
                    background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_60%.png")
                if prozent > 70:
                    background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_70%.png")
                if prozent > 80:
                    background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_80%.png")
                if prozent > 90:
                    background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_90%.png")
                if prozent >= 100:
                    background = Editor("Medien/Rank_Bilder/Rank_Image_Entwurf_100%.png")
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
                background.text((300, 123), f"{rang}", color="white", font=poppins)
                file = File(fp=background.image_bytes, filename="rang.png")
                return await interaction.followup.send(file=file)
        
    @levelsystem.command()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def status(self, interaction: discord.Interaction, modus: typing.Literal["An","Aus"]):
        """Aktiviert/Deaktiviert das Levelsystem auf deinem Server."""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        if modus == "An":
            levelstatus = await checkstatus(self, interaction.guild)
            
            if levelstatus:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist hier bereits aktiviert.**", ephemeral=True)
            
            db["levelstatus"].update_one(
                {"guildID": str(interaction.guild.id)},
                {"$set": {"guildID": str(interaction.guild.id), "status": "1"}},
                upsert=True
            )
            
            return await interaction.followup.send("**<:v_checkmark:1264271011818242159> Das Levelsystem ist jetzt auf diesem Server aktiviert.**")
        if modus == "Aus":
            
            levelstatus = await checkstatus(self, interaction.guild)
            
            if levelstatus == False:
                return await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist hier bereits deaktiviert.**", ephemeral=True)
            
            db["levelstatus"].update_one({"guildID": str(interaction.guild.id)}, {"$set": {"status": "0"}})
            
            await interaction.followup.send("**<:v_checkmark:1264271011818242159> Das Levelsystem ist jetzt auf diesem Server deaktiviert.**")

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def setlevel(self, interaction: discord.Interaction, member: discord.Member, level: int):
        """Bearbeite das Level eines Nutzers."""
        
        await interaction.response.defer()
        
        if await checkstatus(self, interaction.guild) == False:
            await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
            return
        
        db = getMongoDataBase()
        
        result = await db['levelsystem'].find_one({"guild_id": str(interaction.guild.id), "client_id": str(member.id)})
        
        if result is None:
            await interaction.followup.send("**<:v_x:1264270921452224562> Der Nutzer hat bisher noch keinen Rang. Er muss erst ein paar Nachrichten schreiben.**", ephemeral=True)
            return
        
        await db['levelsystem'].update_one({"guild_id": str(interaction.guild.id), "client_id": str(member.id)}, {"$set": {"user_level": level, "user_xp": 0}})
        
        await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Der Benutzer {member.mention} ist nun Level {level}.**")

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def xpboost(self, interaction: discord.Interaction, status: typing.Literal["Anschalten (2x)", "Ausschalten (1x)"]):
        """Starte einen XP Boost auf deinem Server."""
        
        premium_status = await haspremium_forserver(self, interaction.guild)
        if premium_status == False:
            return await interaction.followup.send("**<:v_x:1264270921452224562> Du kannst keinen XP Boost verwalten, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")

        if await checkstatus(self, interaction.guild) == False:
            await interaction.followup.send("**<:v_x:1264270921452224562> Das Levelsystem ist auf diesem Server deaktiviert.**", ephemeral=True)
            return
        
        db = getMongoDataBase()
        
        result = await db['xpboost'].find_one({"guildID": str(interaction.guild.id)})
        
        if result == None:
            if status == "Anschalten (2x)":
                await db['xpboost'].insert_one({"guildID": str(interaction.guild.id), "status": 1})
                return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Der XP Boost wurde auf diesem Server aktiviert.**")
            if status == "Ausschalten (1x)":
                await interaction.followup.send("**<:v_x:1264270921452224562> Hier ist kein XP Boost aktiviert.**", ephemeral=True)
                
        if result != None:
            if status == "Anschalten (2x)":
                if result["status"] == 1:
                    return await interaction.followup.send("**<:v_x:1264270921452224562> Hier ist der XP Boost bereits aktiviert.**", ephemeral=True)
                await db['xpboost'].update_one({"guildID": str(interaction.guild.id)}, {"$set": {"status": 1}})
                return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Der XP Boost wurde auf diesem Server aktiviert.**")
            if status == "Ausschalten (1x)":
                if result["status"] == 0:
                    return await interaction.followup.send("**<:v_x:1264270921452224562> Hier ist der XP Boost bereits deaktiviert.**", ephemeral=True)
                await db['xpboost'].update_one({"guildID": str(interaction.guild.id)}, {"$set": {"status": 0}})
                return await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Der XP Boost wurde auf diesem Server deaktiviert.**")
                
async def setup(bot):
    await bot.add_cog(levelsystem(bot))