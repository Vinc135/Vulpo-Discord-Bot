import discord
from discord.ext import commands
from discord import app_commands
##########
tempchannels = []
def isTempChannel(channel):
    if channel.id in tempchannels:
        return True
    else:
        return False
    
async def isJoinHub(self, channel):
    try:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channel_id FROM tempchannels WHERE guild_id = {channel.guild.id}")
                result = await cursor.fetchone()
                
                if int(channel.id) == int(result[0]):
                    return True
                else:
                    return False
                
    except:
        pass

class tempchannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def voicesetup(self, interaction: discord.Interaction):
        """Richt eine Kanalverbindung ein, um einen Sprachkanal beim Betreten eines anderen erstellt wird. Alias: Join-to-create"""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
        
                await cursor.execute(f"SELECT channel_id FROM tempchannels WHERE guild_id = {interaction.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    new_category = await interaction.guild.create_category('Private Sprachkanäle')
                    category1 = discord.utils.get(interaction.guild.categories, id=int(new_category.id))
                    vc = await interaction.guild.create_voice_channel("Join to create", category=category1)

                    embed = discord.Embed(colour=discord.Colour.blue(),
                                            description=f"The voice system setup was succesfully!.\n{vc.mention}")
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    await interaction.response.send_message(embed=embed)
                
                    
                    await cursor.execute(f"INSERT INTO tempchannels (channel_id, guild_id) VALUES (%s, %s)", (vc.id, interaction.guild.id))
                    
                    

                if result != None:
                    new_category = await interaction.guild.create_category('Private Sprachkanäle')
                    category1 = discord.utils.get(interaction.guild.categories, id=int(new_category.id))
                    vc = await interaction.guild.create_voice_channel("Join to create", category=category1)

                    embed = discord.Embed(colour=discord.Colour.blue(),
                                            description=f"Die Einrichtung des Sprachsystems wurde erfolgreich aktualisiert!.\n{vc.mention}")
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    await interaction.response.send_message(embed=embed)
                
                    
                    await cursor.execute(f"UPDATE tempchannels SET channel_id = {str(vc.id)} WHERE guild_id = {str(interaction.guild.id)}")

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
            if await isJoinHub(self, after.channel):
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