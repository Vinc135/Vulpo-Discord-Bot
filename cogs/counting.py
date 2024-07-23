import discord
from discord.ext import commands
import asyncio
from discord import app_commands
import typing
from utils.MongoDB import getMongoDataBase

class countChangeConfirm(discord.ui.View):
    def __init__(self, kanal=None, bot=None):
        super().__init__(timeout=None)
        self.kanal = kanal
        self.bot = bot

    @discord.ui.button(label='Ja', style=discord.ButtonStyle.green, custom_id="CountingConfirmJa", emoji="<:v_checkmark:1264271011818242159> ")
    async def ja(self, interaction: discord.Interaction, button: discord.ui.Button):
        collection = getMongoDataBase()['counting']
        
        await collection.update_one(
            {'guildID': str(interaction.guild.id)},
            {'$set': {'channelID': str(self.kanal.id), 'zahl': 0}},
            upsert=True
        )
        
        await interaction.response.edit_message(content=f"**<:v_checkmark:1264271011818242159> Der Kanal {self.kanal.mention} ist nun der neue Zähl-Kanal. Die nächste Zahl ist 1!**", view=None)

    @discord.ui.button(label='Abbrechen', style=discord.ButtonStyle.red, custom_id="CountingConfirmNein", emoji="🗑")
    async def nein(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="**<:v_x:1264270921452224562> Vorgang abgebrochen**", view=None)

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=countChangeConfirm(None, self.bot))

    counting = app_commands.Group(name='counting', description='Nehme Einstellungen am Count-System vor.', guild_only=True)

    @counting.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def set(self, interaction: discord.Interaction, kanal: typing.Union[discord.TextChannel, discord.ForumChannel, discord.Thread]):
        """Lege einen Kanal fest, indem gezählt wird."""
        
        await interaction.response.defer()
        
        collection = getMongoDataBase()['counting']
        result = await collection.find_one({'guildID': str(interaction.guild.id)})
        
        if result is None:
            await collection.insert_one({'guildID': str(interaction.guild.id), 'channelID': str(kanal.id), 'zahl': 0})
            await interaction.followup.send(f"**<:v_checkmark:1264271011818242159>  Der Kanal {kanal.mention} ist nun ein Zähl-Kanal.**")
            return
        
        aktueller_kanal = interaction.guild.get_channel(result['channelID'])
        
        if aktueller_kanal is None:
            await collection.update_one(
                {'guildID': str(interaction.guild.id)},
                {'$set': {'channelID': str(kanal.id), 'zahl': 0}}
            )
            
            await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Der Kanal {kanal.mention} ist nun ein Zähl-Kanal.**")
            return
        
        await interaction.followup.send(f"Der aktuelle Zähl-Kanal ist der Kanal {aktueller_kanal.mention}. Möchtest du die Count Funktion dort deaktivieren und in {kanal.mention} aktivieren?", view=countChangeConfirm(kanal, self.bot), ephemeral=True)

    @counting.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def zahl(self, interaction: discord.Interaction, zahl: int):
        """Setze die aktuelle Countzahl zu einer beliebigen."""
        await interaction.response.defer()
        collection = getMongoDataBase()['counting']
        result = await collection.find_one({'guildID': str(interaction.guild.id)})

        if result is None:
            await interaction.followup.send(f"**<:v_x:1264270921452224562> Hier ist kein Count-Channel eingerichtet. Richte einen mit `/count <kanal>` ein**", ephemeral=True)
        else:
            aktueller_kanal = await interaction.guild.fetch_channel(result['channelID'])
            if aktueller_kanal is None:
                await interaction.followup.send(f"**<:v_x:1264270921452224562> Hier ist kein Count-Channel eingerichtet. Richte einen mit `/count <kanal>` ein**", ephemeral=True)
            else:
                await collection.update_one(
                    {'guildID': str(interaction.guild.id)},
                    {'$set': {'zahl': zahl - 1}}
                )
                await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Die nächste Zahl in {aktueller_kanal.mention} ist {zahl}**")

    @counting.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def disable(self, interaction: discord.Interaction):
        """Schalte das Zählsystem aus."""
        await interaction.response.defer()
        collection = getMongoDataBase()['counting']
        result = await collection.find_one({'guildID': str(interaction.guild.id)})

        if result is None:
            await interaction.followup.send(f"**<:v_x:1264270921452224562> Hier ist kein Count-Channel eingerichtet. Richte einen mit `/count <kanal>` ein**", ephemeral=True)
        else:
            aktueller_kanal = await interaction.guild.fetch_channel(result['channelID'])
            if aktueller_kanal is None:
                await interaction.followup.send(f"**<:v_x:1264270921452224562> Hier ist kein Count-Channel eingerichtet. Richte einen mit `/count <kanal>` ein**", ephemeral=True)
            else:
                await collection.delete_one({'guildID': str(interaction.guild.id)})
                await interaction.followup.send(f"**<:v_checkmark:1264271011818242159> Erfolgreich ausgeschaltet.**")

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.guild is None or msg.author.bot:
            return

        collection = getMongoDataBase()['counting']
        result = await collection.find_one({'guildID': str(msg.guild.id)})

        if result is None:
            return
        
        if result['channelID'] != str(msg.channel.id):
            return

        try:
            neue_zahl = int(msg.content)
        except:
            await msg.delete()
            return
        zahl = result['zahl']
        
        if neue_zahl != zahl + 1:
            m = await msg.reply(f"**<:v_x:1264270921452224562> Die nächste Zahl wäre {zahl + 1}**\n*Diese Nachricht wird in 3 Sekunden gelöscht*")
            await asyncio.sleep(3)
            await m.delete()
            await msg.delete()
            return
        
        if 'lastUserID' in result and result['lastUserID'] == str(msg.author.id):
            m = await msg.reply("**<:v_x:1264270921452224562> Warte bitte bis jemand anderes mitzählt. Alleine zählen ist doof.**\n*Diese Nachricht wird in 3 Sekunden gelöscht*")
            await asyncio.sleep(3)
            await m.delete()
            await msg.delete()
            return
            
        await collection.update_one(
            {'guildID': str(msg.guild.id)},
            {'$set': 
                {'zahl': zahl + 1, 'lastUserID': str(msg.author.id)}
            }
        )
        
        await msg.add_reaction("<:v_checkmark:1264271011818242159>")
        
        if neue_zahl % 100 == 0:
            await msg.add_reaction("🎉")
            await msg.pin(reason="Zähl-Meilenstein")

async def setup(bot):
    await bot.add_cog(Counting(bot))