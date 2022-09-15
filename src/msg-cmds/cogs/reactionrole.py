import discord
from discord.ext import commands
import mysql.connector
from info import get_syntax
#########

class reactionrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rr', 'reaction', 'setreaction'], usage="<role> <message> <emoji>")
    @commands.has_permissions(administrator=True)
    async def reactionrole(self, ctx, role: discord.Role=None, message: discord.Message=None, emoji: discord.Emoji=None):
        """Lege eine Reaktionsrolle fest."""
        if role is None or message is None or emoji is None:
            await get_syntax(ctx)
            return
        else:
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            if role != None or message != None or emoji != None:
                cursor = mydb.cursor(buffered=True)
                cursor.execute("INSERT INTO reactionroles (role_id, msg_id, emoji, guild_id) VALUES (%s, %s, %s, %s)", (role.id, message.id, emoji.name, ctx.guild.id))
                mydb.commit()
                embed = discord.Embed(title="Reaktionsrolle ist bereit!", description=f"Rolle: {role.mention}\nEmoji: {emoji}", color=discord.Colour.blue())
                emoj = self.bot.get_emoji(emoji.id)
                await message.add_reaction(emoj)
                await message.reply(embed=embed)
            else:
                await get_syntax(ctx)
                return
            mydb.close()

    ##########
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        if payload.member.bot:
            return
        try:
            guild = self.bot.get_guild(int(payload.guild_id))
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT role_id, msg_id, emoji FROM reactionroles WHERE guild_id = {guild.id}")
            result = cursor.fetchall()
            if result is None:
                return
            else:
                cursor.execute(f"SELECT role_id FROM reactionroles WHERE guild_id = (%s) AND msg_id = (%s) AND emoji = (%s)", (guild.id, payload.message_id, payload.emoji.name))
                r1 = cursor.fetchone()
                await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(int(r1[0])))
                return
            
        except:
            pass
        mydb.close()


    ##########
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        try:
            guild = self.bot.get_guild(int(payload.guild_id))
            cursor = mydb.cursor(buffered=True)
            cursor.execute(f"SELECT role_id, msg_id, emoji FROM reactionroles WHERE guild_id = {guild.id}")
            result = cursor.fetchall()
            if result is None:
                return
            else:
                cursor.execute(f"SELECT role_id FROM reactionroles WHERE guild_id = (%s) AND msg_id = (%s) AND emoji = (%s)", (guild.id, payload.message_id, payload.emoji.name))
                r1 = cursor.fetchone()
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(int(r1[0])))
                return
        except:
            pass
        mydb.close()

async def setup(bot):
    await bot.add_cog(reactionrole(bot))