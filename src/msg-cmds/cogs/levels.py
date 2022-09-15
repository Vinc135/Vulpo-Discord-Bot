import discord
from discord.ext import commands
from disrank.generator import Generator
import functools
import random
import asyncio
import mysql.connector
from info import get_syntax, levelup_role_check
import math

##########
class levelsystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1.0, 3.0, commands.BucketType.guild)

        
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
                return
        if msg.channel.type == discord.ChannelType.private:
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        try:
            bucket = self._cd.get_bucket(msg)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                return
            else:
                cursor = mydb.cursor(buffered=True)
                cursor.execute(f"SELECT user_xp, user_level FROM levelsystem WHERE client_id = (%s) AND guild_id = (%s)", (msg.author.id, msg.guild.id))
                result = cursor.fetchall()

                cursor.execute(f"SELECT enabled FROM levelsystem WHERE guild_id = {msg.guild.id}")
                enabled = cursor.fetchone()
                if len(result) == 0:
                    cursor.execute(f"INSERT INTO levelsystem (client_id, user_xp, user_level, guild_id, enabled) VALUES (%s, %s, %s, %s, %s)", (msg.author.id, 2, 0, msg.guild.id, 0))
                    mydb.commit()
                else:
                    if enabled[0] == 0:
                        return
                    if enabled[0] == 1:
                        xp_start = int(result[0][0])
                        lvl_start = int(result[0][1])
                        xp_end = 5 * (math.pow(lvl_start , 2)) + (50 * lvl_start) + 100
                        newxp = random.randint(15, 30)

                        cursor.execute("UPDATE levelsystem SET user_xp = (%s) WHERE client_id = (%s) AND guild_id = (%s)", (result[0][0] + newxp, msg.author.id, msg.guild.id))
                        mydb.commit()

                        if xp_end < (xp_start + newxp):
                            cursor.execute("UPDATE levelsystem SET user_level = (%s) WHERE client_id = (%s) AND guild_id = (%s)", (int(lvl_start) + 1, msg.author.id, msg.guild.id))
                            cursor.execute("UPDATE levelsystem SET user_xp = (%s) WHERE client_id = (%s) AND guild_id = (%s)", (0 + 1, msg.author.id, msg.guild.id))
                            mydb.commit()
                            try:
                                await levelup_role_check(self.bot, msg.guild.id, msg.author.id, int(lvl_start) + 1)
                            except:
                                pass
                            await msg.channel.send(f"Alles Gute {msg.author.mention}! Du hast Level {int (lvl_start) + 1} erreicht.")
            mydb.close()
        except:
            pass

    @commands.command(aliases=["nlr"], usage="<level> <role>")
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def newlevelrole(self, ctx, level=None, *, role: discord.Role=None):
        """Setze eine neue Levelrolle."""
        if role is None or level is None:
            await get_syntax(ctx)
            return
        try:
            level = int(level)
        except:
            await ctx.send("Die Stufe muss eine Zahl zwischen 1 und 100 sein.")
            return
        if not int(level) > 0 or not int(level) < 101:
            await ctx.send("Die Stufe muss eine Zahl zwischen 1 und 100 sein.")
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute("INSERT INTO levelroles(guild_id, roleid, level) VALUES (%s, %s, %s)", (ctx.guild.id, role.id, level))
        mydb.commit()
        mydb.close()
        await ctx.send(f"Die Rolle {role} wird nun beim Erreichen von Level {level} vergeben.")

    @commands.command(aliases=["dlr"], usage="<level> <role>")
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def deletelevelrole(self, ctx, level=None, *, role: discord.Role=None):
        """Entferne eine Levelrolle."""
        if role is None or level is None:
            await get_syntax(ctx)
            return
        try:
            level = int(level)
        except:
            await ctx.send("Die Stufe muss eine Zahl zwischen 1 und 100 sein.")
            return
        if not int(level) > 0 or not int(level) < 101:
            await ctx.send("Die Stufe muss eine Zahl zwischen 1 und 100 sein.")
            return
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute("DELETE FROM levelroles WHERE guild_id = (%s) AND roleid = (%s) AND level = (%s)", (ctx.guild.id, role.id, level))
        mydb.commit()
        mydb.close()
        await ctx.send(f"Die Rolle {role} wird nun nicht mehr beim Erreichen von Level {level} vergeben.")
    
    @commands.command(aliases=["llr"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def listlevelroles(self, ctx):
        """Liste von allen Levelrollen in diesem Server."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        try:
            cursor.execute(f"SELECT roleid FROM levelroles WHERE guild_id = {ctx.guild.id}")
            r = cursor.fetchall()
            if r is None:
                return await ctx.respond("❌ Ich habe auf diesem Server keine Levelrolle gefunden.")
        except:
            return await ctx.respond("❌ Ich habe auf diesem Server keine Levelrolle gefunden.")

        cursor.execute(f"SELECT roleid, level FROM levelroles WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchall()
        embed = discord.Embed(title="Alle Levelrollen", description="Hier kannst du alle Levelrollen auf diesem Server sehen.", color=discord.Color.purple())
        a = 0
        for i in result:
            try:
                role = ctx.guild.get_role(int(i[0]))
                level = i[1]
                if role is None or level is None:
                    pass
            except:
                pass
            role = ctx.guild.get_role(int(i[0]))
            level = i[1]
            a += 1

            embed.add_field(name=f"Level {level}", value=f"Jeder, der Level {level} erreicht, erhält die Rolle {role.mention}.")
        await asyncio.sleep(1)
        if a >= 1:
            await ctx.send(embed=embed)
        if a < 1:
            return await ctx.send("❌ Ich habe auf diesem Server keine Levelrolle gefunden.")
        mydb.close()
        

    def get_card(self, args):
        image = Generator().generate_profile(**args)
        return image
    
    @commands.command(aliases=["level"], usage="[user]")
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rank(self, ctx, user: discord.User=None):
        """Dieser Befehl zeigt dein Level und deine Erfahrungspunkte."""
        if user == None:
            user = ctx.author

        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT enabled FROM levelsystem WHERE guild_id = {ctx.guild.id}")
        enabled = cursor.fetchone()
        if enabled[0] == 0 or enabled[0] == "0":
            await ctx.send("Das Levelsystem ist auf diesem Server deaktiviert.")
            return

        cursor.execute(f"SELECT user_xp, user_level FROM levelsystem WHERE client_id = (%s) AND guild_id = (%s)", (user.id, ctx.guild.id))
        result = cursor.fetchall()
        if result == None or result == False:
            await ctx.send(f"{user} bist noch nicht eingestuft. Sende erst noch ein paar Nachrichten.")
            return
        try:
            xp_start = result[0][0]
            lvl_start = result[0][1]
            xp_end = 5 * (math.pow(lvl_start , 2)) + (50 * lvl_start) + 100
        except:
            await ctx.send(f"{user} bist noch nicht eingestuft. Sende erst noch ein paar Nachrichten.")
            return
        cursor.execute(f"SELECT client_id FROM levelsystem WHERE guild_id = {ctx.guild.id} ORDER BY user_level DESC")
        result = cursor.fetchall()
        a = 0
        for u in result:
            a += 1
            if str(ctx.author.id) == str(u[0]):
                break

        args = {
            'bg_image' : 'https://cdn.discordapp.com/attachments/904001685737857065/906512391079088128/dunkler-sechseckiger-hintergrund-mit-verlaufsfarbe_79603-1410.jpg', # Background image link (Optional)
            'profile_image' : user.avatar, # User profile picture link
            'level' : lvl_start, # User current level 
            'current_xp' : 0, # Current level minimum xp
            'user_xp' : xp_start, # User current xp
            'user_position' : a, # User position in leaderboard
            'next_xp' : xp_end, # xp required for next level
            'user_name' : user.name, # user name with descriminator 
            'user_status' : "online", # User status eg. online, offline, idle, streaming, dnd
        }

        func = functools.partial(self.get_card, args)
        image = await asyncio.get_event_loop().run_in_executor(None, func)

        file = discord.File(fp=image, filename='image.png')
        await ctx.send(file=file)
        mydb.close()

    @commands.command(aliases=["best"])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def top(self, ctx):
        """Bekomme eine Liste von den Top-10 erfahrensten Membern."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT enabled FROM levelsystem WHERE guild_id = {ctx.guild.id}")
        enabled = cursor.fetchone()
        if enabled[0] == 0 or enabled[0] == "0":
            await ctx.send("Das Levelsystem ist auf diesem Server deaktiviert.")
            return
            
        cursor.execute(f"SELECT user_level, user_xp, client_id FROM levelsystem WHERE guild_id = {ctx.guild.id} ORDER BY user_level DESC, user_xp DESC")
        leaderboard = cursor.fetchall()
        embed = discord.Embed(title="Die erfahrensten Member", color=discord.Color.green())
        for i, pos in enumerate(leaderboard, start=1):
            lvl, xp, member_id = pos
            xp_end = 5 * (math.pow(int(lvl) , 2)) + (50 * int(lvl)) + 100
            name = self.bot.get_user(int(member_id))
            embed.add_field(name=f"{i}. {name}", value=f"Level {lvl} Erfahrung: {xp}/{xp_end}", inline=False)
            if i >= 10:
                await ctx.send(embed=embed)
                break
        await asyncio.sleep(1.5)
        if not i >= 10:
            await ctx.send(embed=embed)
        mydb.close()
        return
    
    @commands.command(usage="<on/off>")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def levelsystem(self, ctx, arg=None):
        """Aktiviert/Deaktiviert das Levelsystem auf deinem Server."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        if arg is None:
            await get_syntax(ctx)
            return
        if arg == "off":
            cursor.execute(f"SELECT enabled FROM levelsystem WHERE guild_id = {ctx.guild.id}")
            enabled = cursor.fetchone()
            if enabled[0] == 0:
                await ctx.send("Das Levelsystem ist hier bereits deaktiviert.")
                return
            if enabled[0] == 1:
                cursor.execute(f"UPDATE levelsystem SET enabled = 0 WHERE guild_id = {ctx.guild.id}")
                mydb.commit()
                await ctx.send("Das Levelsystem ist jetzt auf diesem Server deaktiviert.")
                return
        if arg == "on":
            cursor.execute(f"SELECT enabled FROM levelsystem WHERE guild_id = {ctx.guild.id}")
            enabled = cursor.fetchone()
            if enabled[0] == 0:
                cursor.execute(f"UPDATE levelsystem SET enabled = 1 WHERE guild_id = {ctx.guild.id}")
                mydb.commit()
                await ctx.send("Das Levelsystem ist jetzt auf diesem Server aktiviert.")
                return
            if enabled[0] == 1:
                await ctx.send("Das Levelsystem ist hier bereits aktiviert.")
                return
        mydb.close()

async def setup(bot):
    await bot.add_cog(levelsystem(bot))