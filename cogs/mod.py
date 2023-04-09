import typing
import discord
from discord.ext import commands
from datetime import datetime
from discord import app_commands
from info import getcolour

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def rolle(self, interaction: discord.Interaction, member: discord.Member, rolle: discord.Role):
        """Auf diese Weise können Sie Rollen zu einem Benutzer hinzufügen und entfernen."""
        if rolle not in member.roles:
            try:
                embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                      description=f"{rolle.mention} wurde hinzugefügt zu {member.mention}.")
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                await member.add_roles(rolle)
                await interaction.response.send_message(embed=embed)
                return
            except:
                await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Ich habe hier keine Brechtigungen dazu.**", ephemeral=True)
                return

        if rolle in member.roles:
            try:
                embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                    description=f"{rolle.mention} wurde entfernt von {member.mention}.")
                embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                await member.remove_roles(rolle)
                await interaction.response.send_message(embed=embed)
                return
            except:
                await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Ich habe hier keine Brechtigungen dazu.**", ephemeral=True)
    
    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, grund: str):
        """Lässt einen Benutzer kicken. Wenn möglich."""
        embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                description=f"Der Benutzer {member} (**{member.id}**) wurde gekickt.")
        embed.add_field(name=f"🎛️ Server:", value=f"{interaction.guild.name}", inline=False)
        embed.add_field(name=f"👮 Moderator:", value=f"{interaction.user} (**{interaction.user.id}**)", inline=False)
        embed.add_field(name=f"📄 Grund:", value=f"{grund}", inline=False)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)

        dm = discord.Embed(colour=await getcolour(self, interaction.user),
                            description=f"Hey {member.mention}! \nDu wurdest auf dem Server **{interaction.guild.name}** gekickt! Genauere Informationen hier:")
        dm.add_field(name=f"🎛️ Server:", value=f"{interaction.guild.name}", inline=False)
        dm.add_field(name=f"👮 Moderator:", value=f"{interaction.user.mention}", inline=False)
        dm.add_field(name=f"📄 Grund:", value=f"{grund}", inline=False)
        dm.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        try:
            await interaction.response.send_message(embed=embed)
            await member.kick(reason=grund)
            try:
                await member.send(embed=dm)
            except:
                pass
        except:
            await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Ich habe hier keine Brechtigungen dazu.**", ephemeral=True)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.User, grund: str, nachrichten_löschen: typing.Literal["Keine löschen","Letzte 24 Stunden","Letzte 7 Tage"]):
        """Sperrt einen Benutzer. Wenn möglich."""
        if interaction.user.id == user.id: return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Du kannst dich nicht selber bannen.**", ephemeral=True)
        embed = discord.Embed(colour=await getcolour(self, interaction.user),
                                description=f"Der Benutzer {user.mention} (**{user.id}**) wurde gebannt.")
        embed.add_field(name=f"🎛️ Server:", value=f"{interaction.guild.name}", inline=False)
        embed.add_field(name=f"👮 Moderator:", value=f"{interaction.user.mention} (**{interaction.user.id}**)", inline=False)
        embed.add_field(name=f"📄 Grund:", value=f"{grund}", inline=False)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)

        dm = discord.Embed(colour=await getcolour(self, interaction.user),
                            description=f"Hey {user.mention}! \nDu wurdest auf dem Server **{interaction.guild.name}** gebannt! Genauere Informationen hier:")
        dm.add_field(name=f"🎛️ Server:", value=f"{interaction.guild.name}", inline=False)
        dm.add_field(name=f"👮 Moderator:", value=f"{interaction.user.mention}", inline=False)
        dm.add_field(name=f"📄 Grund:", value=f"{grund}", inline=False)
        dm.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        try:
            member = interaction.guild.get_member(user.id)
            if member in interaction.guild.members: 
                if nachrichten_löschen == "Letzte 24 Stunden":
                    await user.ban(reason=grund, delete_message_days=1)
                if nachrichten_löschen == "Letzte 7 Tage":
                    await user.ban(reason=grund, delete_message_days=7)
                else:
                    await user.ban(reason=grund)
            if member not in interaction.guild.members:
                dobject = discord.Object(id=user.id)
                if nachrichten_löschen == "Letzte 24 Stunden":
                    await interaction.guild.ban(user=dobject, reason=grund, delete_message_days=1)
                if nachrichten_löschen == "Letzte 7 Tage":
                    await interaction.guild.ban(user=dobject, reason=grund, delete_message_days=7)
                else:
                    await interaction.guild.ban(user=dobject, reason=grund)
            await interaction.response.send_message(embed=embed)
            try:
                await user.send(embed=dm)
            except:
                pass
        except:
            await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Ich habe hier keine Berechtigungen dazu.**", ephemeral=True)

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, userstag: str):
        """Entbanne einen User."""
        try:
            banned_user = [ban async for ban in interaction.guild.bans()]
            member_name, member_discriminator = userstag.split('#')
            for ban_entry in banned_user:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await interaction.guild.unban(user)
                    await interaction.response.send_message(f"**<:v_haken:1048677657040134195> {userstag} wurde entbannt**")
                    return
            await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Der Benutzer ist nicht gebannt. Bitte beachte folgenden Syntax: `/unban userstag: <name#tag>`**", ephemeral=True)
        except:
            await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Der Benutzer ist nicht gebannt. Bitte beachte folgenden Syntax: `/unban userstag: <name#tag>`**", ephemeral=True)


    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(ban_members=True)
    async def banlist(self, interaction: discord.Interaction):
        """Listet alle gesperrten Benutzer auf diesem Server auf."""
        try:
            a = 0
            users = [ban async for ban in interaction.guild.bans()]
            if len(users) > 0:
                msg1 = f'__**Username**__ — __**Grund**__\n'
                for entry in users:
                    userName = str(entry.user)
                    if entry.user.bot:
                        userName = '🤖 ' + userName
                    reason = str(entry.reason)
                    msg1 += f'{userName} — {reason}\n'
                    a += 1
                try:
                    for chunk in [msg1[i:i + 2000] for i in range(0, len(msg1), 2000)]:
                        embed = discord.Embed(title="Banliste", description=f"{msg1}", color=await getcolour(self, interaction.user))
                        embed.set_thumbnail(url=interaction.guild.icon)
                        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                        embed.set_footer(text=f"{a} gesperrte Benutzer in diesem Server.")
                        await interaction.response.send_message(embed=embed)
                except discord.HTTPException:
                    embed2 = discord.Embed(title="Banliste", description=f"{msg1}", color=await getcolour(self, interaction.user))
                    embed2.set_thumbnail(url=interaction.guild.icon)
                    embed2.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    embed.set_footer(text=f"{a} gesperrte Benutzer in diesem Server.")
                    await interaction.response.send_message(embed=embed2)
            else:
                await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Hier gibt es keine gebannten Nutzer.**", ephemeral=True)
        except:
            await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Hier gibt es keine gebannten Nutzer.**", ephemeral=True)

    clear = app_commands.Group(name='clear', description='Lösche bestimmte Nachrichten.', guild_only=True)

    @clear.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id))
    async def channel(self, interaction: discord.Interaction, kanal: discord.TextChannel, anzahl: int):
        """Löscht eine bestimmte Anzahl von Nachrichten."""
        try:
            if anzahl > 100:
                return await interaction.response.send_message("**<:v_kreuz:1049388811353858069> Das Limit liegt bei 100 Nachrichten.**", ephemeral=True)
            await interaction.response.send_message(f"**<:v_info:1037065915113676891> Ich lösche jetzt {anzahl} {'Nachrichten' if anzahl >= 2 else 'Nachricht'} in {kanal.mention}. Einen Moment.**", ephemeral=True)
            deleted = await kanal.purge(limit=anzahl)
            await interaction.edit_original_response(content=f"**<:v_haken:1048677657040134195> Ich habe {len(deleted)} {'Nachrichten' if len(deleted) >= 2 else 'Nachricht'} in {kanal.mention} gelöscht.**")
        except:
            pass

    @clear.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def between(self, interaction: discord.Interaction, kanal: discord.TextChannel, erste_nachricht: str, zweite_nachricht: str):
        """Löscht eine bestimmte Anzahl von Nachrichten."""
        try:
            int(erste_nachricht)
            int(zweite_nachricht)
        except:
            await interaction.response.send_message(f"**<:v_kreuz:1049388811353858069> Ups, da ging etwas schief. Bitte stelle sicher, dass es sich bei deinem Input um Nachrichten ID's gehandelt hat.**", ephemeral=True)
            return
        try:
            message1 = await kanal.fetch_message(int(erste_nachricht))
            message2 = await kanal.fetch_message(int(zweite_nachricht))
            if message1 == None or message2 == None:
                await interaction.response.send_message(f"**<:v_kreuz:1049388811353858069> Ups, da ging etwas schief. Bitte stelle sicher, dass es sich bei deinem Input um Nachrichten ID's gehandelt hat.**", ephemeral=True)
                return
            await interaction.response.send_message(f"**<:v_info:1037065915113676891> Ich lösche jetzt die Nachrichten in {kanal.mention} zwischen [dieser]({message1.jump_url}) und [dieser]({message2.jump_url}) Nachricht. Einen Moment.**")
            deleted = await kanal.purge(before=discord.Object(erste_nachricht), after=discord.Object(zweite_nachricht))
            if len(deleted) == 0:
                await interaction.edit_original_response(content=f"**<:v_kreuz:1049388811353858069> Ups, da ging etwas schief. Bitte stelle sicher, dass es sich bei deinem Input um Nachrichten ID's gehandelt hat.**")
                return
            else:
                await interaction.edit_original_response(content=f"**<:v_haken:1048677657040134195> {len(deleted)} {'Nachrichten' if len(deleted) >= 2 else 'Nachricht'} in {kanal.mention} zwischen [dieser]({message1.jump_url}) und [dieser]({message2.jump_url}) Nachricht gelöscht.**")
        except:
            pass

async def setup(bot):
    await bot.add_cog(moderation(bot))