import typing
import discord
from discord.ext import commands
from discord import app_commands
from info import getcolour, haspremium_forserver
##########

class joinrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if member.bot:
                    try:
                        await cursor.execute(f"SELECT role_id FROM botroles WHERE guild_id = {member.guild.id}")
                        result = await cursor.fetchall()
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
                        await cursor.execute(f"SELECT role_id FROM joinroles WHERE guild_id = {member.guild.id}")
                        result = await cursor.fetchall()
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
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if argument == "Löschen":
                    await cursor.execute(f"DELETE FROM joinroles WHERE guild_id = {interaction.guild.id}")
                    await interaction.response.send_message("**<:v_haken:1048677657040134195> Alle Joinrollen gelöscht.**")           
                    return
                if argument == "Hinzufügen (Rolle muss mit angegeben werden)":
                    if rolle is None:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Eine Rollen-Angabe ist erforderlich beim Einrichten.**", ephemeral=True)           
                        return
                    
                    await cursor.execute(f"SELECT role_id FROM joinroles WHERE guild_id = {interaction.guild.id}")
                    a = await cursor.fetchall()

                    premium_status = await haspremium_forserver(self, interaction.guild)
                    if premium_status == False:
                        if len(a) >= 3:
                            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du kannst keine weiteren Joinrollen für Mitglieder erstellen, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")

                    await cursor.execute(f"SELECT guild_id FROM joinroles WHERE role_id = {rolle.id}")
                    result = await cursor.fetchone()
                    if result:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Diese Rolle ist bereits eingestellt.**", ephemeral=True)           
                        return
                    await cursor.execute("INSERT INTO joinroles (role_id, guild_id) VALUES (%s, %s)", (rolle.id, interaction.guild.id))
                    embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                            description=f"{rolle.mention} wurde zu den Joinrollen für User hinzugefügt.")
                    embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.", icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    await interaction.response.send_message(embed=embed)
                if argument == "Anzeigen":
                    await cursor.execute(f"SELECT role_id FROM joinroles WHERE guild_id = {interaction.guild.id}")
                    result = await cursor.fetchall()
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
                                        icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                        await interaction.response.send_message(embed=embed)
                        return
                    if str(result) == "[]":
                        embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                            description=f"Es wurde noch keine Joinrolle für User festgelegt. Füge eine mit **/joinrole <role/ID>** hinzu.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.",
                                        icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                        await interaction.response.send_message(embed=embed)
                        return

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def botrole(self, interaction: discord.Interaction, argument: typing.Literal["Hinzufügen (Rolle muss mit angegeben werden)", "Löschen","Anzeigen"], rolle: discord.Role=None):
        """Lege Joinrollen für Bots fest."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if argument == "Löschen":
                    await cursor.execute(f"DELETE FROM botroles WHERE guild_id = {interaction.guild.id}")
                    await interaction.response.send_message("**<:v_haken:1048677657040134195> Alle Joinrollen gelöscht.**")           
                    return
                if argument == "Hinzufügen (Rolle muss mit angegeben werden)":
                    if rolle is None:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Eine Rollen-Angabe ist erforderlich beim Einrichten.**", ephemeral=True)           
                        return
                    
                    await cursor.execute(f"SELECT role_id FROM botroles WHERE guild_id = {interaction.guild.id}")
                    a = await cursor.fetchall()

                    premium_status = await haspremium_forserver(self, interaction.guild)
                    if premium_status == False:
                        if len(a) >= 3:
                            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du kannst keine weiteren Joinrollen für Bots erstellen, da der Serverowner kein Premium besitzt. [Premium auschecken](https://vulpo-bot.de/premium)**")

                    await cursor.execute(f"SELECT guild_id FROM botroles WHERE role_id = {rolle.id}")
                    result = await cursor.fetchone()
                    if result:
                        await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Diese Rolle ist bereits eingestellt.**", ephemeral=True)           
                        return
                    await cursor.execute("INSERT INTO botroles (role_id, guild_id) VALUES (%s, %s)", (rolle.id, interaction.guild.id))
                    embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                            description=f"{rolle.mention} wurde zu den Joinrollen für Bots hinzugefügt.")
                    embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.", icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    await interaction.response.send_message(embed=embed)
                if argument == "Anzeigen":
                    await cursor.execute(f"SELECT role_id FROM botroles WHERE guild_id = {interaction.guild.id}")
                    result = await cursor.fetchall()
                    if str(result) != "[]":
                        rollen = ""
                        for r in result:
                            r = discord.utils.get(interaction.guild.roles, id=int(r[0]))
                            if r is not None:
                                rollen += f"{r.mention}\n"
                        embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                            description=f"Aktuelle Joinrollen für Bots in diesem Server: \n{rollen}")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.",
                                        icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                        await interaction.response.send_message(embed=embed)
                        return
                    if str(result) == "[]":
                        embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                            description=f"Es wurde noch keine Joinrolle für Bots festgelegt. Füge eine mit **/joinrole <role/ID>** hinzu.")
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.",
                                        icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                        await interaction.response.send_message(embed=embed)
                        return
 
async def setup(bot):
    await bot.add_cog(joinrole(bot))