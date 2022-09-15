import discord
from discord.ext import commands
from discord import app_commands
import mysql.connector
##########
tempchannels = []
def isTempChannel(channel):
    if channel.id in tempchannels:
        return True
    else:
        return False
    
def isJoinHub(channel):
    try:
        mydb = mysql.connector.connect(
        host="54.37.204.19",
        user="u60388_adFMo8yi8w",
        password="dNPaL8=W2qapSVrwv=Q9Me8I",
        database="s60388_Vulpo"
    )
        cursor = mydb.cursor()
        cursor.execute(f"SELECT channel_id FROM tempchannels WHERE guild_id = {channel.guild.id}")
        result = cursor.fetchone()
        mydb.close()
        if int(channel.id) == int(result[0]):
            return True
        else:
            return False
        
    except:
        pass

class tempchannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def voicesetup(self, ctx):
        """Richt eine Kanalverbindung ein, um einen Sprachkanal beim Betreten eines anderen erstellt wird. Alias: Join-to-create"""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        if ctx.author.bot:
            return
        else:
            cursor = mydb.cursor()
            cursor.execute(f"SELECT channel_id FROM tempchannels WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result == None:
                new_category = await ctx.guild.create_category('Private Sprachkanäle')
                category1 = discord.utils.get(ctx.guild.categories, id=int(new_category.id))
                vc = await ctx.guild.create_voice_channel("Join to create", category=category1)

                embed = discord.Embed(colour=discord.Colour.blue(),
                                      description=f"The voice system setup was succesfully!.\n{vc.mention}")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
            
                cursor = mydb.cursor()
                cursor.execute(f"INSERT INTO tempchannels (channel_id, guild_id) VALUES (%s, %s)", (vc.id, ctx.guild.id))
                mydb.commit()

            if result != None:
                new_category = await ctx.guild.create_category('Private Sprachkanäle')
                category1 = discord.utils.get(ctx.guild.categories, id=int(new_category.id))
                vc = await ctx.guild.create_voice_channel("Join to create", category=category1)

                embed = discord.Embed(colour=discord.Colour.blue(),
                                      description=f"Die Einrichtung des Sprachsystems wurde erfolgreich aktualisiert!.\n{vc.mention}")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
            
                cursor = mydb.cursor()
                cursor.execute(f"UPDATE tempchannels SET channel_id = {str(vc.id)} WHERE guild_id = {str(ctx.guild.id)}")
                mydb.commit()
        mydb.close()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel:
            if isTempChannel(before.channel):
                bchan = before.channel
                if len(bchan.members) == 0:
                    await bchan.delete(reason="Kein User im Tempchannel.")
            else:
                pass
        if after.channel:
            if isJoinHub(after.channel):
                name = f"{member.name}"
                output = await after.channel.clone(name=name, reason="Ist dem Joinhub beigetreten.")
                overwrites = {
                    member: discord.PermissionOverwrite(
                        manage_channels=True,
                        mute_members=True, 
                    )
                }
                await output.edit(overwrites=overwrites)
                if output:
                    tempchannels.append(output.id)
                    await member.move_to(output, reason="Erstellte ein Tempchannel")
            else:
               	pass

async def setup(bot):
    await bot.add_cog(tempchannel(bot))