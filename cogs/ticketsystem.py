import datetime
import math
import discord
from discord.ext import commands
import os
from discord import app_commands
from utils.utils import discord_timestamp, send_error
from utils.utils import getcolour
from utils.MongoDB import getMongoDataBase

class PanelbuttonView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Ticket öffnen", emoji="🎫", custom_id="Button-CreateTicket", style=discord.ButtonStyle.grey)
    async def button_createticket(self, interaction: discord.Interaction, button):
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = await db['panels'].find_one({"guildID": str(interaction.guild_id), "msgID": str(interaction.message.id)})
        
        if not result:
            return
        
        role = interaction.guild.get_role(int(result['role']))
        category = await interaction.guild.fetch_channel(int(result['categoryID']))
        
        if role == None or category == None:
            embed = discord.Embed(title="Fehler", description="Es wurde keine Supportrolle oder Kategorie gefunden, bitte Informiere das lokale Server Team", color=discord.Color.red())
            interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        member = await interaction.guild.fetch_member(interaction.user.id)
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False,
                send_messages=False,
            ),
            role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=False,
            ),
            member: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True, 
            )
        }
        
        new_channel = await category.create_text_channel(name=f"ticket-{member.name}", overwrites=overwrites)
        
        embed = discord.Embed(color=discord.Color.orange(), title=f"Ticket von {member.name}", description=f"Hallo {member.mention}. Ein Teammitglied wird sich gleich um dich kümmern.\nBitte beschreibe dein Problem in der Zwischenzeit.")
        embed.add_field(name="Thema", value=interaction.message.embeds[0].title)
        embed.add_field(name="Bearbeiter", value="Keiner")
        embed.set_author(name=interaction.user, icon_url=member.avatar)
        
        view = ClosebuttonView(self.bot)
        panelnachricht = await new_channel.send(f"{member.mention} | {role.mention}", embed=embed, view=view)
        await panelnachricht.pin()
        await interaction.followup.send(f"<:v_checkmark:1264271011818242159> Ich habe ein Ticket für dich erstellt\nDu findest es dort: {new_channel.mention}", ephemeral=True)
        
        await db['tickets'].insert_one({"guildID": str(interaction.guild_id), "channelID": str(new_channel.id), "userID": str(interaction.user.id), "panelID": str(interaction.message.id), "msgID": str(panelnachricht.id)})
        
        log = await db['ticketlog'].find_one({"guildid": str(interaction.guild_id)})
        
        if log is None:
            return        
        
        ticketlog = await interaction.guild.fetch_channel(int(log['channelid']))
        
        if ticketlog is None:
            return
        
        embed = discord.Embed(title="Ticket erstellt", description=f"{interaction.user.mention} ({interaction.user}) hat ein Ticket erstellt. \n**Ticket:** {new_channel.mention}\n**Thema:** {interaction.message.embeds[0].title}", color=discord.Color.green())
        embed.set_author(name=interaction.user, icon_url=member.avatar)
        
        await ticketlog.send(embed=embed)
        
class ClosebuttonView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Ticket schließen", emoji="<:v_x:1264270921452224562>", custom_id="Button-CloseTicket", style=discord.ButtonStyle.red)
    async def button_closeticket(self, interaction: discord.Interaction, button):
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = await db['tickets'].find_one({"channelID": str(interaction.channel_id)})
        
        if not result:
            return
        
        try:
            role = interaction.guild.get_role(int(result['role']))
            if role not in interaction.user.roles:
                return await interaction.followup.send(f"**<:v_x:1264270921452224562> Du hast keine Rechte dazu. Du benötigst die Rolle {role.mention}**", ephemeral=True)
        except:
            pass
        
        user = await interaction.guild.fetch_member(int(result['userID']))
        
        member = interaction.user
        channel = interaction.channel
        
        message = await channel.fetch_message(result["msgID"])
        
        
        if message is None:
            return
        
        result = await db['panels'].find_one({"guildID": str(interaction.guild_id), "categoryID": channel.category_id})
        
        if not result:
            return
        
        archiv = await interaction.guild.fetch_channel(int(result['archivID']))
        
        role = interaction.guild.get_role(int(result['role']))
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False,
                send_messages=False,
            ),
            user: discord.PermissionOverwrite(
                read_messages=False,
                send_messages=False, 
            ),
            role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True, 
            )
        }
        
        await channel.edit(category=archiv, overwrites=overwrites)
        
        view = DeletebuttonView(self.bot)
        
        await channel.send(f"{member.mention} hat das Ticket geschlossen", view=view)
        
        button.disabled = True
        
        await message.edit(view=self)
        
        log = await db['ticketlog'].find_one({"guildid": str(interaction.guild_id)})
        
        if log is None:
            return
        
        ticketlog = await interaction.guild.fetch_channel(int(log['channelid']))
        
        if ticketlog is None:
            return
        
        embed = discord.Embed(title="Ticket geschlossen", description=f"{interaction.user.mention} ({interaction.user}) hat ein Ticket geschlossen. \n**Ticket:** {channel.mention}({channel.name})", color=discord.Color.gold())
        embed.set_author(name=interaction.user, icon_url=member.avatar)
        
        await ticketlog.send(embed=embed)

    @discord.ui.button(label="Ticket claimen", emoji="<:v_25:1264264906505715752>", custom_id="Button-ClaimTicket", style=discord.ButtonStyle.grey)
    async def button_claimticket(self, interaction: discord.Interaction, button):
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = await db['tickets'].find_one({"channelID": str(interaction.channel_id)})
        
        if result is None:
            return
        
        r = await db['panels'].find_one({"guildID": str(interaction.guild_id), "categoryID": str(interaction.channel.category_id), "msgID": result['panelID']})
        
        if not r:
            return
        
        role = interaction.guild.get_role(int(r['role']))
        if role not in interaction.user.roles:
            return await interaction.followup.send(f"**<:v_x:1264270921452224562> Du hast keine Rechte dazu. Du benötigst die Rolle {role.mention}**", ephemeral=True)
        
        channel = interaction.channel
        member = await interaction.guild.fetch_member(int(result['userID']))
        
        claim = discord.Embed(color=discord.Color.green(), title="Ticket geclaimt", description=f"{member.mention}, du wirst nun von {interaction.user.mention} supportet.")
                
        await channel.send(embed=claim)
        button.disabled = True
        
        title = interaction.message.embeds[0].title
        description = interaction.message.embeds[0].description
        Themaheader = interaction.message.embeds[0].fields[0].name
        Thema = interaction.message.embeds[0].fields[0].value
        Claimer = interaction.message.embeds[0].fields[1].name
        authorname = interaction.message.embeds[0].author.name
        authoricon = interaction.message.embeds[0].author.icon_url
        embed = discord.Embed(title=title, description=description, color=discord.Color.orange())
            
        embed.set_author(name=authorname, icon_url=authoricon)
        embed.add_field(name=Themaheader, value=Thema)
        embed.add_field(name=Claimer, value=interaction.user.mention)

        # Overwrites dictionary
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False,
                send_messages=False,
            ),
            interaction.user: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
            ),
            role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=False, 
            ),
            member: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            )
        }

        await interaction.channel.edit(overwrites=overwrites)
            
        message = await interaction.channel.fetch_message(result["msgID"])
            
        await message.edit(content=f"{member.mention}", embed=embed, view=self)

        log = await getMongoDataBase()["ticketlog"].find_one({"guildid": str(interaction.guild_id)})
        if log is None:
            return
        
        ticketlog = await interaction.guild.fetch_channel(int(log['channelid']))
        
        if ticketlog is None:
            return
        
        embed = discord.Embed(title="Ticket geclaimt", description=f"{interaction.user.mention} ({interaction.user}) hat ein Ticket geclaimt. \n**Ticket:** {interaction.channel.mention} ({interaction.channel.name})\n**Thema:** {Thema}", color=discord.Color.blurple())
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            
        await ticketlog.send(embed=embed)

    @discord.ui.button(label="Userinfo", emoji="<:v_arrow_left:1264271794936746054>", custom_id="Button-UserInfo", style=discord.ButtonStyle.grey)
    async def button_userinfo(self, interaction: discord.Interaction, button):
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = await db['tickets'].find_one({"channelID": str(interaction.channel_id)})
        
        if result is None:
            return
        
        member = await interaction.guild.fetch_member(int(result['userID']))
        
        t1 = math.floor(member.created_at.timestamp())
        t2 = datetime.datetime.fromtimestamp(int(t1))
        t3 = math.floor(member.joined_at.timestamp())
        t4= datetime.datetime.fromtimestamp(int(t3))
        embed = discord.Embed(colour=member.color, description=f"Der Account wurde {discord_timestamp(t2, 'R')} erstellt.")
        embed.set_thumbnail(url=member.avatar)
        
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Beitritt", value=f"Der User ist {discord_timestamp(t4, 'R')} dem Server beigetreten.", inline=True)
        embed.add_field(name="Bot?", value='Ja' if member.bot else 'Nein', inline=False)
        embed.add_field(name="Höchte Rolle", value=member.top_role.mention, inline=True)
        
        if member.public_flags:
            flags = ""
            for flag in member.public_flags:
                if flag[1] == True:
                    if flag[0] == "staff":
                        flags += "<:v_discordstaff:1037069155008000042> "
                    if flag[0] == "partner":
                        flags += "<:v_discordpartner:1037069463532601404> "
                    if flag[0] == "bug_hunter":
                        flags += "<:v_bughunter:1037069367483060244> "
                    if flag[0] == "hypesquad_bravery":
                        flags += "<:v_bravery:1037069608127037500> "
                    if flag[0] == "hypesquad_brilliance":
                        flags += "<:brilliance:1037069659708600435> "
                    if flag[0] == "hypesquad_balance":
                        flags += "<:v_balance:1037069709318819950> "
                    if flag[0] == "early_supporter":
                        flags += "<:v_supporter:1037069787043483678> "
                    if flag[0] == "bug_hunter_level_2":
                        flags += "<:v_bughuntergold:1037069871286059058> "
                    if flag[0] == "verified_bot":
                        flags += "<:v_verifiedbot:1037069972226179182> "
                    if flag[0] == "verified_bot_developer":
                        flags += "<:v_verifiedbotdeveloper:1037070049539788851>"
                    if flag[0] == "discord_certified_moderator":
                        flags += "<:v_168:1264268507193806900>"
            if flags != "":
                embed.add_field(name="🎖 Abzeichen", value=flags, inline=False)

        liste = ""
        m = interaction.guild.get_member(member.id)
        for a in m.activities:
            if a.name not in liste:
                if liste == "":
                    liste += f"{a.name}"
                else:
                    liste += f", {a.name}"
        
        if liste != "":
            embed.add_field(name="🎮 Aktivitäten", value=liste, inline=False)
        user = await self.bot.fetch_user(member.id)
        
        if user.banner:
            embed.set_image(url=user.banner)
            
        embed.set_author(name=f"Userinfo {member}", icon_url=member.avatar)
        await interaction.followup.send(embed=embed, ephemeral=True)

    @discord.ui.button(label="Einstellungen", emoji="<:v_82:1264266106307215370>", custom_id="Button-einstellungen", style=discord.ButtonStyle.blurple)
    async def button_einstellungen(self, interaction: discord.Interaction, button):
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = await db['tickets'].find_one({"channelID": str(interaction.channel_id)})
        
        if result is None:
            return
        
        r = await db['panels'].find_one({"guildID": str(interaction.guild_id), "categoryID": str(interaction.channel.category_id), "msgID": result['panelID']})
        
        if not r:
            return
        
        role = interaction.guild.get_role(int(r['role']))
        if role not in interaction.user.roles:
            return await interaction.followup.send(f"**<:v_x:1264270921452224562> Du hast keine Rechte dazu. Du benötigst die Rolle {role.mention}**", ephemeral=True)
        
        
        view = discord.ui.View(timeout=None)
        view.add_item(menu_member(self.bot))
        await interaction.followup.send(f"<:v_82:1264266106307215370> **Du kannst hier Nutzer auswählen, die vom Ticket entfernt werden sollen und welche hinzugefügt werden sollen.**", ephemeral=True, view=view)

class DeletebuttonView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Ticket löschen", emoji="<:v_x:1264270921452224562>", custom_id="Button-DeleteTicket", style=discord.ButtonStyle.red)
    async def button_deleteticket(self, interaction: discord.Interaction, button):
        await interaction.response.defer()
        await interaction.channel.send(f"{interaction.user.mention} hat das Ticket gelöscht.")
        
        db = getMongoDataBase()
        
        result = await db["tickets"].find_one({"channelID": str(interaction.channel_id)})
        
        if result is None:
            return
        
        panel = await db["panels"].find_one({"guildID": str(interaction.guild_id)})
        
        if panel is None:
            return
        
        member = interaction.user       
        
        log = await db["ticketlog"].find_one({"guildid": str(interaction.guild_id)})
        
        if log is None:
            return
        
        ticketlog = interaction.guild.get_channel(int(log["channelid"]))
        
        if ticketlog is None:
            return
        
        logFile = f'{interaction.channel}.log'
        counter = 0
        with open(logFile, 'w', encoding='UTF-8') as f:
            f.write(f'Nachrichten vom Kanal: {interaction.channel} am {interaction.message.created_at.strftime("%d.%m.%Y %H:%M:%S")}\n')
            async for message in interaction.channel.history(limit=1000, oldest_first=True):
                try:
                    attachment = '[File:: {}]'.format(message.attachments[0].url)
                except IndexError:
                    attachment = ''
                f.write('{} {!s:20s}: {} {}\r\n'.format(message.created_at.strftime('%d.%m.%Y %H:%M:%S'), message.author,message.clean_content, attachment))
                counter += 1
        f = discord.File(logFile)
        async for message in interaction.channel.history(limit=1, oldest_first=True):
            embed = discord.Embed(title=f"Ein Ticket wurde gelöscht", description=f"Das Ticket gehörte {message.content}.\nHier erhältst du wichtige Informationen über das gelöschte Ticket.", color=discord.Color.red())
            embed.set_footer(text=message.embeds[0].title, icon_url=message.embeds[0].author.icon_url)
            embed.add_field(name=message.embeds[0].fields[0].name, value=message.embeds[0].fields[0].value)
            embed.add_field(name=message.embeds[0].fields[1].name, value=message.embeds[0].fields[1].value)
            embed.add_field(name="Gelöscht von", value=f"{interaction.user} ({interaction.user.mention})")
            embed.set_author(name=interaction.user, icon_url=member.avatar)
            await ticketlog.send(embed=embed, file=f)
            break
        
        await db["tickets"].delete_one({"channelID": str(interaction.channel_id)})
                
        await interaction.channel.delete()
        
        try:
            os.remove(logFile)
        except OSError as e:
            pass
                

    @discord.ui.button(label="Ticket erneut öffnen", emoji="<:v_86:1264266242345402388>", custom_id="Button-ReopenTicket", style=discord.ButtonStyle.green)
    async def button_reopenticket(self, interaction: discord.Interaction, button):
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        result = await db["tickets"].find_one({"channelID": str(interaction.channel_id)})
    
        if result is None:
            return
        try:
            r = await db["panels"].find_one({"guildID": str(interaction.guild_id), "categoryID": str(interaction.channel.category_id), "msgID": result["panelID"]})
            role = await interaction.guild.get_role(int(r[0]))
            if role not in interaction.user.roles:
                return await interaction.followup.send(f"**<:v_x:1264270921452224562> Du hast keine Rechte dazu. Du benötigst die Rolle {role.mention}**", ephemeral=True)
        except:
            pass
        
        member = interaction.user
        channel = interaction.channel
        r = await db["panels"].find_one({"guildID": str(interaction.guild_id), "archivID": str(channel.category.id)})
        category = await interaction.guild.fetch_channel(int(r["categoryID"]))
        user = await interaction.guild.fetch_member(int(result["userID"]))
        role = interaction.guild.get_role(int(r["role"]))
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False,
                send_messages=False,
            ),
            user: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True, 
            ),
            role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True, 
            )
        }
        await channel.edit(category=category, overwrites=overwrites)
        await channel.send(f"{member.mention} hat das Ticket erneut geöffnet.")
        button.disabled = True
        await interaction.edit_original_response(view=self)

        log = await db["ticketlog"].find_one({"guildid": str(interaction.guild_id)})
        
        if log is None:
            return
        
        ticketlog = await interaction.guild.fetch_channel(int(log["channelid"]))
        
        if ticketlog is None:
            return
        
        embed = discord.Embed(title="Ticket erneut geöffnet", description=f"{interaction.user.mention} ({interaction.user}) hat ein Ticket erneut geöffnet. \n**Ticket:** {interaction.channel.mention} ({interaction.channel.name})", color=discord.Color.gold())
        embed.set_author(name=interaction.user, icon_url=member.avatar)
        
        await ticketlog.send(embed=embed)
                
    
class menu_member(discord.ui.UserSelect):
    def __init__(self, bot=None):
        super().__init__(placeholder="Wähle aus", min_values=1, max_values=1, custom_id="erfweraf")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=False, ephemeral=True)
        overwrites = interaction.channel.overwrites
        endtext = ""
        for member in self.values:
            if member not in interaction.channel.members:
                overwrites[member] = discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                )
                endtext += f"\n<:v_checkmark:1264271011818242159> **{member.mention} wurde von {interaction.user.mention} zum Ticket hinzugefügt.**"
            
            if member in interaction.channel.members:
                try:
                    del overwrites[member]
                except:
                    overwrites[member] = discord.PermissionOverwrite(
                        read_messages=False,
                        send_messages=False,
                    )
                endtext += f"\n<:v_x:1264270921452224562> **{member.mention} wurde von {interaction.user.mention} vom Ticket entfernt.**"
        
        await interaction.channel.edit(overwrites=overwrites)
        await interaction.followup.send(endtext)

class Ticketsystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=PanelbuttonView(self.bot))
        self.bot.add_view(view=ClosebuttonView(self.bot))
        self.bot.add_view(view=DeletebuttonView(self.bot))

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def createpanel(self, interaction, kanal: discord.TextChannel, titel: str, beschreibung: str, supportrolle: discord.Role, kategorie: discord.CategoryChannel, archiv: discord.CategoryChannel):
        """Erstelle ein Panel für Tickets."""
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        finalemb = discord.Embed(title="Ticketsystem", description="Ein neues Panel wurde erstellt!", color=await getcolour(self, interaction.user))

        finalemb.add_field(name="Kanal", value=kanal.mention, inline=False)
        finalemb.add_field(name="Embedtitel", value=titel, inline=False)
        finalemb.add_field(name="Embedbeschreibung", value=beschreibung, inline=False)
        finalemb.add_field(name="Supportrolle", value=supportrolle.mention, inline=False)
        finalemb.add_field(name="Kategorie für offene Tickets", value=kategorie.name, inline=False)
        finalemb.add_field(name="Kategorie für geschlossene Tickets", value=archiv.name, inline=False)
        await interaction.followup.send(f"{interaction.user.mention} hat ein Panel erstellt.", embed=finalemb)

        embed = discord.Embed(title=titel, description=beschreibung, color=await getcolour(self, interaction.user))
                
        if interaction.guild.icon != None:
            embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_footer(text="Drücke auf den Button um ein Ticket zu erstellen")
        
        panel = await kanal.send(embed=embed, view=PanelbuttonView(self.bot))

        await db["panels"].insert_one({"guildID": str(interaction.guild.id), "msgID": str(panel.id), "role": str(supportrolle.id), "categoryID": str(kategorie.id), "archivID": str(archiv.id)})                    
            
async def setup(bot):
    await bot.add_cog(Ticketsystem(bot))