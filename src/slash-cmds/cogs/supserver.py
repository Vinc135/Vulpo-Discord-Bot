import asyncio
from discord.ext import commands
import discord
import random


        
def random_color():
    return discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

class Supserver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot:
            return
        
        if int(msg.channel.id) == 960133645140623390:
            await asyncio.sleep(1800)
            await msg.delete()
                    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 925729625580113951:
            channel = member.guild.get_channel(926224205639467108)
            message = await channel.send(f"<a:winken:964852677945204786> Hallo {member.mention}, wähle hier deine Rollen aus!")
            await asyncio.sleep(60)
            await message.delete()

async def setup(bot):
    await bot.add_cog(Supserver(bot))