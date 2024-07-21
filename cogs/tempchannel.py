import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import getcolour, haspremium_forserver
from utils.MongoDB import getMongoDataBase
##########

async def isTempChannel(self, member, channel):
    
    result = getMongoDataBase()['tempchannel'].find_one({"guildID": member.guild.id, "channelID": channel.id})
    
    if result:
        return channel
    else:
        return False
    
async def isJoinHub(self, channel):
    
    result = getMongoDataBase()['tempchannels'].find_one({"guildID": channel.guild.id, "channelID": channel.id})
    
    if result:
        return channel
    else:
        return False

async def isOwner(self, member, channel):
    
    result = getMongoDataBase()['tempchannel'].find_one({"guildID": member.guild.id, "channelID": channel.id, "userID": member.id})
    
    if result:
        return member
    
    else:
        return False

class rename(discord.ui.Modal, title="Kanalname ändern"):
    def __init__(self):
        super().__init__(custom_id="zjrzujzrujzujzuj")
        self.add_item(discord.ui.TextInput(label="Neuer Name", style=discord.TextStyle.short, required=True, placeholder="Zockerhöhle"))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.user.voice.channel.edit(name=self.children[0].value)
        except:
            return await interaction.followup.send(f"**<:v_9:1264264656831119462> Der Name ist zu lang.**", ephemeral=True)
        await interaction.response.defer(thinking=False, ephemeral=True)

class limit(discord.ui.Modal, title="Kanallimit ändern"):
    def __init__(self):
        super().__init__(custom_id="gwrtgrtgwrtg")
        self.add_item(discord.ui.TextInput(label="Neues Limit", style=discord.TextStyle.short, required=True, placeholder="1", max_length=2))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            int(self.children[0].value)
        except:
            return await interaction.followup.send(f"**<:v_9:1264264656831119462> Das ist keine Zahl. Bitte gib eine Zahl beim nächsten Mal an.**", ephemeral=True)
        await interaction.user.voice.channel.edit(name=interaction.user.voice.channel.name, user_limit=self.children[0].value)
        await interaction.response.defer(thinking=False, ephemeral=True)

class interface(discord.ui.View):
    def __init__(self, bot=None):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="wefhqiwuzdlgkedf", emoji="<:v_15:1264264716679905360>")
    async def lock_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.voice == None:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du bist in keinem Tempchannel.**", ephemeral=True)

        channel = await isTempChannel(self, interaction.user, interaction.user.voice.channel)
        owner = await isOwner(self, interaction.user, interaction.user.voice.channel)
        if channel == False:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du bist in keinem Tempchannel.**", ephemeral=True)
        
        if owner == False:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du kannst das nicht tun, da du nicht der Besitzer des Kanals bist.**", ephemeral=True)
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                connect=False
            )
        }
        await channel.edit(overwrites=overwrites)
        await interaction.response.defer(thinking=False, ephemeral=True)
    
    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="qvweifuqgieuzfviuw", emoji="<:v_86:1264266242345402388>")
    async def unlock_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.voice == None:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du bist in keinem Tempchannel.**", ephemeral=True)

        channel = await isTempChannel(self, interaction.user, interaction.user.voice.channel)
        owner = await isOwner(self, interaction.user, interaction.user.voice.channel)
        if channel == False:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du bist in keinem Tempchannel.**", ephemeral=True)
        
        if owner == False:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du kannst das nicht tun, da du nicht der Besitzer des Kanals bist.**", ephemeral=True)
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                connect=True
            )
        }
        await channel.edit(overwrites=overwrites)
        await interaction.response.defer(thinking=False, ephemeral=True)
    
    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="ergwrgwrg", emoji="<:v_117:1264267042945761320>")
    async def hide_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.voice == None:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du bist in keinem Tempchannel.**", ephemeral=True)

        channel = await isTempChannel(self, interaction.user, interaction.user.voice.channel)
        owner = await isOwner(self, interaction.user, interaction.user.voice.channel)
        if channel == False:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du bist in keinem Tempchannel.**", ephemeral=True)
        
        if owner == False:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du kannst das nicht tun, da du nicht der Besitzer des Kanals bist.**", ephemeral=True)
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            )
        }
        await channel.edit(overwrites=overwrites)
        await interaction.response.defer(thinking=False, ephemeral=True)
    
    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="öqhefoiuhioudgwc", emoji="<:v_104:1264266670810071202>")
    async def unhide_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.voice == None:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du bist in keinem Tempchannel.**", ephemeral=True)

        channel = await isTempChannel(self, interaction.user, interaction.user.voice.channel)
        owner = await isOwner(self, interaction.user, interaction.user.voice.channel)
        if channel == False:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du bist in keinem Tempchannel.**", ephemeral=True)
        
        if owner == False:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du kannst das nicht tun, da du nicht der Besitzer des Kanals bist.**", ephemeral=True)
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                view_channel=True
            )
        }
        await channel.edit(overwrites=overwrites)
        await interaction.response.defer(thinking=False, ephemeral=True)
    
    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="faegvwtgethr", emoji="<:v_31:1264264994774585445>")
    async def rename_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.voice == None:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du bist in keinem Tempchannel.**", ephemeral=True)

        channel = await isTempChannel(self, interaction.user, interaction.user.voice.channel)
        owner = await isOwner(self, interaction.user, interaction.user.voice.channel)
        if channel == False:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du bist in keinem Tempchannel.**", ephemeral=True)
        
        if owner == False:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du kannst das nicht tun, da du nicht der Besitzer des Kanals bist.**", ephemeral=True)
        
        await interaction.response.send_modal(rename())
    
    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id="iuehrofgweiuzfzg", emoji="<:v_114:1264266960011526165>")
    async def limit_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.voice == None:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du bist in keinem Tempchannel.**", ephemeral=True)

        channel = await isTempChannel(self, interaction.user, interaction.user.voice.channel)
        owner = await isOwner(self, interaction.user, interaction.user.voice.channel)
        if channel == False:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du bist in keinem Tempchannel.**", ephemeral=True)
        
        if owner == False:
            return await interaction.followup.send("**<:v_9:1264264656831119462> Du kannst das nicht tun, da du nicht der Besitzer des Kanals bist.**", ephemeral=True)
        
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
        
        db = getMongoDataBase()
        
        existing_channel = await db["tempchannels"].find_one({"guildID": interaction.guild.id})

        new_category = await interaction.guild.create_category('Private Sprachkanäle')
        vc = await interaction.guild.create_voice_channel("Join to create", category=new_category)
        interfaceChannel = await interaction.guild.create_text_channel("Interface", category=new_category)

        embed = discord.Embed(colour=await getcolour(interaction.user),
                              description=f"Die Einrichtung des JoinToCreate Kanals war erfolgreich.\n{vc.mention}")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.followup.send(embed=embed)

        if existing_channel:
            getMongoDataBase()["tempchannels"].update_one(
                {"guildID": interaction.guild.id},
                {"$set": {"channelID": vc.id}}
            )
        else:
            getMongoDataBase()["tempchannels"].insert_one({"channelID": vc.id, "guildID": interaction.guild.id})
                
        if interfacekanal:
            embed = discord.Embed(title="Tempchannel Interface", description=f"""
<:v_25:1264264906505715752> Willkommen im Interface Menü von Vulpo.
<:v_24:1264264867511144479> [KLICK HIER]({vc.jump_url}) um einen eigenen Talk zu erstellen.
<:v_24:1264264867511144479> Nutze diesen Kanal um deinen Channel zu individualisieren.

————————————————————————
> <:v_15:1264264716679905360> Sperren
> <:v_86:1264266242345402388> Entsperren

> <:v_117:1264267042945761320> Verstecken
> <:v_104:1264266670810071202> Enthüllen

> <:v_31:1264264994774585445> Namen ändern
> <:v_114:1264266960011526165> Limit ändern
""", colour=discord.Color.orange())
                    
        await interfacekanal.send(embed=embed, view=interface(self.bot))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        db = getMongoDataBase()
        
        if before.channel:
            if await isTempChannel(self, member, before.channel):
                bchan = before.channel
                if len(bchan.members) == 0:
                    await bchan.delete(reason="Kein User im Tempchannel.")
                    await db["tempchannel"].delete_one({"channelID": bchan.id})
                    return
            else:
                pass
        if after.channel:
            if await isJoinHub(self, after.channel):
                name = f"⌛️ | {member.name}"
                output = await after.channel.clone(name=name, reason="Ist dem Joinhub beigetreten.")
                if output:
                    await member.move_to(output, reason="Erstellte einen Tempchannel")
                    await db["tempchannel"].insert_one({"guildID": member.guild.id, "channelID": output.id, "userID": member.id})
            else:
                pass

async def setup(bot):
    await bot.add_cog(tempchannel(bot))