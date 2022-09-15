import discord
from discord.ext import commands
import expr
import asyncio
from discord import app_commands

class countconfirm(discord.ui.View):
    def __init__(self, kanal=None, bot=None):
        super().__init__(timeout=None)
        self.kanal = kanal
        self.bot = bot

    @discord.ui.button(label='Ja', style=discord.ButtonStyle.green, custom_id="A94bA4bG98bGbG4Fb5b5AG", emoji="✅")
    async def ja(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("UPDATE counting SET channelID = (%s) WHERE guildID = (%s)", (self.kanal.id, interaction.guild.id))
                await cursor.execute("UPDATE counting SET zahl = (%s) WHERE guildID = (%s)", (0, interaction.guild.id))
        
        await interaction.response.edit_message(content=f"**✅ Der Kanal {self.kanal.mention} ist nun der neue Zähl-Kanal. Die nächste Zahl ist 1!**", view=None)

    @discord.ui.button(label='Abbrechen', style=discord.ButtonStyle.red, custom_id="67D799H969i69796HDiiU7", emoji="🗑")
    async def nein(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="**❌ Vorgang abbgebrochen**", view=None)

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=countconfirm(None, self.bot))

    counting = app_commands.Group(name='counting', description='Nehme Einstellungen am Count-System vor.')

    @counting.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def set(self, interaction: discord.Interaction, kanal: discord.TextChannel):
        """Lege einen Kanal fest, indem gezählt wird."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelID FROM counting WHERE guildID = {interaction.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    await cursor.execute("INSERT INTO counting (channelID, guildID, zahl) VALUES (%s, %s, %s)", (kanal.id, interaction.guild.id, 0))
                    
                    await interaction.response.send_message(f"**✅ Der Kanal {kanal.mention} ist nun ein Zähl-Kanal.**")
                if result != None:
                    aktueller_kanal = interaction.guild.get_channel(int(result[0]))
                    if aktueller_kanal == None:
                        await cursor.execute("UPDATE counting SET channelID = (%s) WHERE guildID = (%s)", (kanal.id, interaction.guild.id))
                        await cursor.execute("UPDATE counting SET zahl = (%s) WHERE guildID = (%s)", (0, interaction.guild.id))
                        
                        await interaction.response.send_message(f"**✅ Der Kanal {kanal.mention} ist nun ein Zähl-Kanal.**")
                    if aktueller_kanal != None:
                        await interaction.response.send_message(f"Der aktuelle Zähl-Kanal ist der Kanal {aktueller_kanal.mention}.\nMöchtest du die Count Funktion dort deaktivieren und in {kanal.mention} aktivieren?", view=countconfirm(kanal, self.bot), ephemeral=True)

    @counting.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def zahl(self, interaction: discord.Interaction, zahl: int):
        """Setze die aktuelle Countzahl zu einer beliebigen."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelID FROM counting WHERE guildID = {interaction.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    await interaction.response.send_message(f"**❌ Hier ist kein Count-Channel eingerichtet. Richte einen mit `/count <kanal>` ein**", ephemeral=True)
                    return
                if result != None:
                    aktueller_kanal = interaction.guild.get_channel(int(result[0]))
                    if aktueller_kanal == None:
                        await interaction.response.send_message(f"**❌ Hier ist kein Count-Channel eingerichtet. Richte einen mit `/count <kanal>` ein**", ephemeral=True)
                        return
                    if aktueller_kanal != None:
                        await cursor.execute("UPDATE counting SET zahl = (%s) WHERE guildID = (%s)", (zahl - 1, interaction.guild.id))
                        
                        await interaction.response.send_message(f"**✅ Die nächste Zahl ist {zahl} in {aktueller_kanal.mention}**")

    @counting.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def disable(self, interaction: discord.Interaction):
        """Schalte das Zählsystem aus."""
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelID FROM counting WHERE guildID = {interaction.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    await interaction.response.send_message(f"**❌ Hier ist kein Count-Channel eingerichtet. Richte einen mit `/count <kanal>` ein**", ephemeral=True)
                    return
                if result != None:
                    aktueller_kanal = interaction.guild.get_channel(int(result[0]))
                    if aktueller_kanal == None:
                        await interaction.response.send_message(f"**❌ Hier ist kein Count-Channel eingerichtet. Richte einen mit `/count <kanal>` ein**", ephemeral=True)
                        return
                    if aktueller_kanal != None:
                        await cursor.execute(f"DELETE FROM counting WHERE guildID = {interaction.guild.id}")
                        
                        await interaction.response.send_message(f"**✅ Erfolgreich ausgeschaltet.**")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot:
            return
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT channelID, zahl FROM counting WHERE guildID = {msg.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    return
                if result != None:
                    if int(result[0]) == int(msg.channel.id):
                        try:
                            neue_zahl = expr.evaluate(msg.content)
                        except:
                            await msg.delete()
                            return
                        a = 0
                        zahl = int(result[1])
                        if int(neue_zahl) == int(zahl + 1):
                            async for message in msg.channel.history(limit=2, oldest_first=False):
                                a += 1
                                if a == 2:
                                    if int(message.author.id) == int(msg.author.id):
                                        m = await msg.reply("**❌ Warte bitte bis jemand anderes mitzählt. Alleine zählen ist doof.**\n*Diese Nachricht wird in 3 Sekunden gelöscht*")
                                        await asyncio.sleep(3)
                                        await m.delete()
                                        await msg.delete()
                                        return
                                    else:
                                        await cursor.execute("UPDATE counting SET zahl = (%s) WHERE guildID = (%s)", (zahl + 1, msg.guild.id))
                                        await msg.add_reaction("✅")
                                        if int(msg.content) == 100:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 200:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 300:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 400:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 500:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 600:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 700:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 800:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 900:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 1000:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 1100:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 1200:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 1300:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 1400:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 1500:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 1600:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 1700:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 1800:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 1900:
                                            await msg.add_reaction("🎉")
                                        if int(msg.content) == 2000:
                                            await msg.add_reaction("🎉")
                        else:
                            m = await msg.reply(f"**❌ Die nächste Zahl wäre {zahl + 1}**\n*Diese Nachricht wird in 3 Sekunden gelöscht*")
                            await asyncio.sleep(3)
                            await m.delete()
                            await msg.delete()
                            return

async def setup(bot):
    await bot.add_cog(Counting(bot))