import typing
import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import getcolour, haspremium_forserver
from utils.MongoDB import getMongoDataBase
##########

class joinrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        db = getMongoDataBase()
        
        if member.bot:
            try:
                result = await db['botroles'].find({"guild_id": member.guild.id}).to_list(length=None)
                if result == None:
                    return
                for role in result:
                    r = discord.utils.get(member.guild.roles, id=int(role[0]))
                    if r is not None:
                        await member.add_roles(r)
                return
            except:
                return
        else:
            try:
                result = await db['joinroles'].find({"guild_id": member.guild.id}).to_list(length=None)
                if result == None:
                    return
                for role in result:
                    r = discord.utils.get(member.guild.roles, id=int(role[0]))
                    if r is not None:
                        await member.add_roles(r)
                return
            except:
                return

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def joinrole(self, interaction: discord.Interaction, argument: typing.Literal["Hinzufügen (Rolle muss mit angegeben werden)", "Löschen","Anzeigen"], rolle: discord.Role=None):
                """Lege Joinrollen für User fest."""
        
                await interaction.response.defer()
                
                db = getMongoDataBase()
        
                if argument == "Löschen":
                    await db['joinroles'].delete_many({"guild_id": interaction.guild.id})
                    await interaction.followup.send("**<:v_158:1264268251916009553> Alle Joinrollen gelöscht.**")           
                    return
                if argument == "Hinzufügen (Rolle muss mit angegeben werden)":
                    if rolle is None:
                        await interaction.followup.send("**<:v_9:1264264656831119462> Eine Rollen-Angabe ist erforderlich beim Einrichten.**", ephemeral=True)           
                        return
                    
                    
                    existing = await db['joinroles'].find({"guild_id": interaction.guild.id}).to_list(length=None)
                    
                    premium = await haspremium_forserver(self, interaction.guild)
                    
                    if not premium and len(existing) >= 3:
                        return await interaction.followup.send("**<:v_9:1264264656831119462> Du kannst keine weiteren Joinrollen für Mitglieder erstellen, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")

                    result = await db['joinroles'].find({"role_id": rolle.id}).to_list(length=None)

                    if result:
                        await interaction.followup.send("**<:v_9:1264264656831119462> Diese Rolle ist bereits eingestellt.**", ephemeral=True)           
                        return
                    
                    
                    db["joinroles"].insert_one({"role_id": rolle.id, "guild_id": interaction.guild.id})
                    embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                            description=f"{rolle.mention} wurde zu den Joinrollen für User hinzugefügt.")
                    embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.", icon_url="https://cdn.discordapp.com/filename/814202875387183145.png")
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    await interaction.followup.send(embed=embed)
                if argument == "Anzeigen":
                    
                    result = await db['joinroles'].find({"guild_id": interaction.guild.id}).to_list(length=None)
                    
                    if str(result) != "[]":
                        rollen = ""
                        for r in result:
                            r = discord.utils.get(interaction.guild.roles, id=int(r[0]))
                            if r is not None:
                                rollen += f"{r.mention}\n"
                        embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                            description=f"Aktuelle Joinrollen für User in diesem Server: \n{rollen}")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.",
                                        icon_url="https://cdn.discordapp.com/filename/814202875387183145.png")
                        await interaction.followup.send(embed=embed)
                        return
                    if str(result) == "[]":
                        embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                            description=f"Es wurde noch keine Joinrolle für User festgelegt. Füge eine mit **/joinrole <role/ID>** hinzu.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.",
                                        icon_url="https://cdn.discordapp.com/filename/814202875387183145.png")
                        await interaction.followup.send(embed=embed)
                        return

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def botrole(self, interaction: discord.Interaction, argument: typing.Literal["Hinzufügen (Rolle muss mit angegeben werden)", "Löschen","Anzeigen"], rolle: discord.Role=None):
                """Lege Joinrollen für Bots fest."""
                
                await interaction.response.defer()
                
                db = getMongoDataBase()
                
                if argument == "Löschen":
                    db["botroles"].delete_many({"guild_id": interaction.guild.id})
                    await interaction.followup.send("**<:v_158:1264268251916009553> Alle Joinrollen gelöscht.**")           
                    return
                if argument == "Hinzufügen (Rolle muss mit angegeben werden)":
                    if rolle is None:
                        await interaction.followup.send("**<:v_9:1264264656831119462> Eine Rollen-Angabe ist erforderlich beim Einrichten.**", ephemeral=True)           
                        return
                    
                    existing = await db['botroles'].find({"guild_id": interaction.guild.id}).to_list(length=None)
                    
                    premium = await haspremium_forserver(self, interaction.guild)
                    
                    if not premium and len(existing) >= 3:
                        return await interaction.followup.send("**<:v_9:1264264656831119462> Du kannst keine weiteren Joinrollen für Bots erstellen, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")               

                    result = await db['botroles'].find({"role_id": rolle.id}).to_list(length=None)

                    if result:
                        await interaction.followup.send("**<:v_9:1264264656831119462> Diese Rolle ist bereits eingestellt.**", ephemeral=True)           
                        return
                    
                    await db['botroles'].insert_one({"role_id": rolle.id, "guild_id": interaction.guild.id})
                    embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                            description=f"{rolle.mention} wurde zu den Joinrollen für Bots hinzugefügt.")
                    embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.", icon_url="https://cdn.discordapp.com/filename/814202875387183145.png")
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    await interaction.followup.send(embed=embed)
                if argument == "Anzeigen":
                    
                    result = await db['botroles'].find({"guild_id": interaction.guild.id}).to_list(length=None)
                    
                    if len(result) != 0:
                        rollen = ""
                        for r in result:
                            r = discord.utils.get(interaction.guild.roles, id=int(r[0]))
                            if r is not None:
                                rollen += f"{r.mention}\n"
                        embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                            description=f"Aktuelle Joinrollen für Bots in diesem Server: \n{rollen}")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.",
                                        icon_url="https://cdn.discordapp.com/filename/814202875387183145.png")
                        await interaction.followup.send(embed=embed)
                        return
                    
                    embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                        description=f"Es wurde noch keine Joinrolle für Bots festgelegt. Füge eine mit **/joinrole <role/ID>** hinzu.")
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.",
                                    icon_url="https://cdn.discordapp.com/filename/814202875387183145.png")
                    await interaction.followup.send(embed=embed)
                    return
 
async def setup(bot):
    await bot.add_cog(joinrole(bot))