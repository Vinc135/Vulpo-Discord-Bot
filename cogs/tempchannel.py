import discord
from discord.ext import commands
from discord import app_commands
##########

async def isTempChannel(self, member, channel):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT userID FROM tempchannel WHERE guildID = (%s) AND channelID = (%s)", (member.guild.id, channel.id))
            result = await cursor.fetchone()
            if result:
                return channel
            else:
                return False
    
async def isJoinHub(self, channel):
    try:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT channel_id FROM tempchannels WHERE guild_id = (%s) AND channel_id = (%s)", (channel.guild.id, channel.id))
                result = await cursor.fetchone()
                if result is None:
                    return False
                else:
                    return True
                
    except:
        pass

async def isOwner(self, member, channel):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT channelID FROM tempchannel WHERE guildID = (%s) AND channelID = (%s) AND userID = (%s)", (member.guild.id, channel.id, member.id))
            result = await cursor.fetchone()
            if result:
                return member
            else:
                return False

class rename(discord.ui.Modal, title="Kanalname ändern"):
    def __init__(self):
        super().__init__(custom_id="zjrzujzrujzujzuj")
        self.add_item(discord.ui.TextInput(label="Neuer Name", style=discord.TextStyle.short, required=True, placeholder="Zockerhöhle"))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.user.voice.channel.edit(name=self.children[0].value)
        await interaction.response.defer(thinking=False, ephemeral=True)

class limit(discord.ui.Modal, title="Kanallimit ändern"):
    def __init__(self):
        super().__init__(custom_id="gwrtgrtgwrtg")
        self.add_item(discord.ui.TextInput(label="Neues Limit", style=discord.TextStyle.short, required=True, placeholder="1"))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.user.voice.channel.edit(name=interaction.user.voice.channel.name, user_limit=self.children[0].value)
        await interaction.response.defer(thinking=False, ephemeral=True)

class interface(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="wefhqiwuzdlgkedf", emoji="<:v_sperren:1037124926919938130>")
    async def lock_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.voice == None:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du bist in keinem Tempchannel.**", ephemeral=True)

        channel = await isTempChannel(self, interaction.user, interaction.user.voice.channel)
        owner = await isOwner(self, interaction.user, interaction.user.voice.channel)
        if channel == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du bist in keinem Tempchannel.**", ephemeral=True)
        
        if owner == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du kannst das nicht tun, da du nicht der Besitzer des Kanals bist.**", ephemeral=True)
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                connect=False
            )
        }
        await channel.edit(overwrites=overwrites)
        await interaction.response.defer(thinking=False, ephemeral=True)
    
    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="qvweifuqgieuzfviuw", emoji="<:v_entsperren:1037124922805330001>")
    async def unlock_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.voice == None:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du bist in keinem Tempchannel.**", ephemeral=True)

        channel = await isTempChannel(self, interaction.user, interaction.user.voice.channel)
        owner = await isOwner(self, interaction.user, interaction.user.voice.channel)
        if channel == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du bist in keinem Tempchannel.**", ephemeral=True)
        
        if owner == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du kannst das nicht tun, da du nicht der Besitzer des Kanals bist.**", ephemeral=True)
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                connect=True
            )
        }
        await channel.edit(overwrites=overwrites)
        await interaction.response.defer(thinking=False, ephemeral=True)
    
    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="ergwrgwrg", emoji="<:v_unsichtbar:1037124928345997322>")
    async def hide_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.voice == None:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du bist in keinem Tempchannel.**", ephemeral=True)

        channel = await isTempChannel(self, interaction.user, interaction.user.voice.channel)
        owner = await isOwner(self, interaction.user, interaction.user.voice.channel)
        if channel == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du bist in keinem Tempchannel.**", ephemeral=True)
        
        if owner == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du kannst das nicht tun, da du nicht der Besitzer des Kanals bist.**", ephemeral=True)
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            )
        }
        await channel.edit(overwrites=overwrites)
        await interaction.response.defer(thinking=False, ephemeral=True)
    
    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="öqhefoiuhioudgwc", emoji="<:v_enthullen:1037124921685442591>")
    async def unhide_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.voice == None:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du bist in keinem Tempchannel.**", ephemeral=True)

        channel = await isTempChannel(self, interaction.user, interaction.user.voice.channel)
        owner = await isOwner(self, interaction.user, interaction.user.voice.channel)
        if channel == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du bist in keinem Tempchannel.**", ephemeral=True)
        
        if owner == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du kannst das nicht tun, da du nicht der Besitzer des Kanals bist.**", ephemeral=True)
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                view_channel=True
            )
        }
        await channel.edit(overwrites=overwrites)
        await interaction.response.defer(thinking=False, ephemeral=True)
    
    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="faegvwtgethr", emoji="<:v_chat:1037065910567055370>")
    async def rename_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.voice == None:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du bist in keinem Tempchannel.**", ephemeral=True)

        channel = await isTempChannel(self, interaction.user, interaction.user.voice.channel)
        owner = await isOwner(self, interaction.user, interaction.user.voice.channel)
        if channel == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du bist in keinem Tempchannel.**", ephemeral=True)
        
        if owner == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du kannst das nicht tun, da du nicht der Besitzer des Kanals bist.**", ephemeral=True)
        
        await interaction.response.send_modal(rename())
    
    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="iuehrofgweiuzfzg", emoji="<:v_limit:1037124925653274674>")
    async def limit_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.voice == None:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du bist in keinem Tempchannel.**", ephemeral=True)

        channel = await isTempChannel(self, interaction.user, interaction.user.voice.channel)
        owner = await isOwner(self, interaction.user, interaction.user.voice.channel)
        if channel == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du bist in keinem Tempchannel.**", ephemeral=True)
        
        if owner == False:
            return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du kannst das nicht tun, da du nicht der Besitzer des Kanals bist.**", ephemeral=True)
        
        await interaction.response.send_modal(limit())

class tempchannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=interface(self.bot))

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def voicesetup(self, interaction: discord.Interaction, interfacekanal: discord.TextChannel=None):
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
                                            description=f"Die Einrichtung des Sprachsystems war erfolgreich.\n{vc.mention}")
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    await interaction.response.send_message(embed=embed)
                
                    
                    await cursor.execute(f"INSERT INTO tempchannels (channel_id, guild_id) VALUES (%s, %s)", (vc.id, interaction.guild.id))
                    
                if result != None:
                    new_category = await interaction.guild.create_category('Private Sprachkanäle')
                    category1 = discord.utils.get(interaction.guild.categories, id=int(new_category.id))
                    vc = await interaction.guild.create_voice_channel("Join to create", category=category1)

                    embed = discord.Embed(colour=discord.Colour.blue(),
                                            description=f"Die Aktualisierung des Sprachsystems war erfolgreich.\n{vc.mention}")
                    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    await interaction.response.send_message(embed=embed)
                
                    
                    await cursor.execute(f"UPDATE tempchannels SET channel_id = {str(vc.id)} WHERE guild_id = {str(interaction.guild.id)}")
                
                if interfacekanal:
                    embed = discord.Embed(title="Tempchannel Interface", description=f"""
<:v_support:1037065931588894841> Willkommen im Interface Menü von Vulpo.
<:v_play:1037065922134945853> [KLICK HIER]({vc.jump_url}) um einen eigenen Talk zu erstellen.
<:v_play:1037065922134945853> Nutze diesen Kanal um deinen Channel zu individualisieren.

————————————————————————
> <:v_sperren:1037124926919938130> Sperren
> <:v_entsperren:1037124922805330001> Entsperren

> <:v_unsichtbar:1037124928345997322> Verstecken
> <:v_enthullen:1037124921685442591> Enthüllen

> <:v_chat:1037065910567055370> Namen ändern
> <:v_limit:1037124925653274674> Limit ändern
""", colour=discord.Color.orange())
                    await interfacekanal.send(embed=embed, view=interface(self.bot))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if before.channel:
                    if await isTempChannel(self, member, before.channel):
                        bchan = before.channel
                        if len(bchan.members) == 0:
                            await bchan.delete(reason="Kein User im Tempchannel.")
                            await cursor.execute("DELETE FROM tempchannel WHERE channelID = (%s)", (bchan.id))
                            return
                    else:
                        pass
                if after.channel:
                    if await isJoinHub(self, after.channel):
                        name = f"⌛️ | {member.name}"
                        output = await after.channel.clone(name=name, reason="Ist dem Joinhub beigetreten.")
                        if output:
                            await member.move_to(output, reason="Erstellte einen Tempchannel")
                            await cursor.execute("INSERT INTO tempchannel(guildID, channelID, userID) VALUES(%s, %s, %s)", (member.guild.id, output.id, member.id))
                    else:
                        pass

async def setup(bot):
    await bot.add_cog(tempchannel(bot))