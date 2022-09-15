import discord
from discord.ext import commands
import mysql.connector
import typing
##########

class joinrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            try:
                cursor = mydb.cursor(buffered=True)
                cursor.execute(f"SELECT role_id FROM botroles WHERE guild_id = {member.guild.id}")
                result = cursor.fetchall()
                for role in result:
                    r = discord.utils.get(member.guild.roles, id=int(role[0]))
                    await member.add_roles(r)
                mydb.close()
                return
            except:
                return
        else:
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            try:
                cursor = mydb.cursor(buffered=True)
                cursor.execute(f"SELECT role_id FROM joinroles WHERE guild_id = {member.guild.id}")
                result = cursor.fetchall()
                for role in result:
                    r = discord.utils.get(member.guild.roles, id=int(role[0]))
                    await member.add_roles(r)
                mydb.close()
                return
            except:
                return

    @commands.command(usage="<role/ID> [remove]")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.channel)
    async def joinrole(self, ctx, role: typing.Union[discord.Role, str]=None):
        """Lege Joinrollen für User fest."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        if role == "remove":
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"DELETE FROM joinroles WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Joinrollen gelöscht.")
            mydb.commit()
            return
        if role is None:
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT role_id FROM joinroles WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchall()
            if str(result) != "[]":
                rollen = ""
                for role in result:
                    r = discord.utils.get(ctx.guild.roles, id=int(role[0]))
                    rollen += f"{r.mention}\n"
                embed = discord.Embed(colour=discord.Colour.orange(),
                                      description=f"Aktuelle Joinrollen für User in diesem Server: \n{rollen}")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.",
                                 icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                await ctx.send(embed=embed)
                return
            if str(result) == "[]":
                embed = discord.Embed(colour=discord.Colour.orange(),
                                      description=f"Es wurde noch keine Joinrolle für User festgelegt. Füge eine mit **{ctx.prefix}joinrole <role/ID>** hinzu.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.",
                                 icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                await ctx.send(embed=embed)
                return
        if role is not None:
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"INSERT INTO joinroles (role_id, guild_id) VALUES (%s, %s)", (role.id, ctx.guild.id))
            mydb.commit()

            embed = discord.Embed(colour=discord.Colour.orange(),
                                    description=f"{role.mention} wurde zu den Joinrollen für User hinzugefügt.")
            embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.", icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        mydb.close()

    @commands.command(usage="<role/ID> [remove]")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.channel)
    async def botrole(self, ctx, role: typing.Union[discord.Role, str]=None):
        """Lege Joinrollen für Bots fest."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        if role == "remove":
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"DELETE FROM botroles WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Joinrollen gelöscht.")
            mydb.commit()
            return
        if role is None:
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT role_id FROM botroles WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchall()
            if str(result) != "[]":
                rollen = ""
                for role in result:
                    r = discord.utils.get(ctx.guild.roles, id=int(role[0]))
                    rollen += f"{r.mention}\n"
                embed = discord.Embed(colour=discord.Colour.orange(),
                                      description=f"Aktuelle Joinrollen für Bots in diesem Server: \n{rollen}")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.",
                                 icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                await ctx.send(embed=embed)
                return
            if str(result) == "[]":
                embed = discord.Embed(colour=discord.Colour.orange(),
                                      description=f"Es wurde noch keine Joinrolle für Bots festgelegt. Füge eine mit **{ctx.prefix}joinrole <role/ID>** hinzu.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.",
                                 icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
                await ctx.send(embed=embed)
                return
        if role is not None:
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"INSERT INTO botroles (role_id, guild_id) VALUES (%s, %s)", (role.id, ctx.guild.id))
            mydb.commit()

            embed = discord.Embed(colour=discord.Colour.orange(),
                                    description=f"{role.mention} wurde zu den Joinrollen für Bots hinzugefügt.")
            embed.set_footer(text="Stell sicher, dass meine Rolle höher als die Joinrollen gelistet ist.", icon_url="https://cdn.discordapp.com/emojis/814202875387183145.png")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        mydb.close()
                
async def setup(bot):
    await bot.add_cog(joinrole(bot))