import discord
from discord.ext import commands
import mysql.connector
import asyncio
import os

class PanelbuttonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket öffnen", emoji="🎫", custom_id="Button-CreateTicket", style=discord.ButtonStyle.blurple)
    async def button_createticket(self, interaction, button):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT msgID, role, categoryID FROM panels WHERE guildID = (%s) AND msgID = (%s)", (interaction.guild_id, interaction.message.id))
        result = cursor.fetchall()
        if result is None:
            return

        for i in result:
            role = interaction.guild.get_role(int(i[1]))
            category = interaction.guild.get_channel(int(i[2]))
            if str(interaction.message.id) != str(i[0]) or role == None or category == None:
                return
            member = interaction.guild.get_member(int(interaction.user.id))
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    read_messages=False,
                    send_messages=False,
                ),
                role: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                ),
                member: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True, 
                )
            }
            new_channel = await category.create_text_channel(name=f"ticket-{member.name}", overwrites=overwrites)
            embed=discord.Embed(color=discord.Color.orange(), title=f"Ticket von {member.name}", description=f"Hallo {member.mention}. Ein Teammitglied wird sich gleich um dich kümmern.\nBitte beschreibe dein Problem in der Zwischenzeit.")
            embed.add_field(name="Thema", value=interaction.message.embeds[0].title)
            embed.add_field(name="Bearbeiter", value="Keiner")
            embed.set_author(name=interaction.user, icon_url=member.avatar)
            view = ClosebuttonView()
            await new_channel.send(f"{member.mention} | {role.mention}", embed=embed, view=view)
            await interaction.response.send_message(f"✅ Ich habe ein Ticket für dich erstellt\nDu findest es dort: {new_channel.mention}", ephemeral=True)
            
            cursor.execute("INSERT INTO tickets(guildID, channelID, userID) VALUES(%s, %s, %s)", (interaction.guild_id, new_channel.id, member.id))
            mydb.commit()
            try:
                cursor.execute(f"SELECT channelid FROM ticketlog WHERE guildid = {interaction.guild_id}")
                log = cursor.fetchone()
                if log is None:
                    return
                ticketlog = interaction.guild.get_channel(int(log[0]))
                if ticketlog is None:
                    return
                embed = discord.Embed(title="Ticket erstellt", description=f"{interaction.user.mention}({interaction.user}) hat ein Ticket erstellt. \n**Ticket:** {new_channel.mention}\n**Thema:** {interaction.message.embeds[0].title}", color=discord.Color.green())
                embed.set_author(name=interaction.user, icon_url=member.avatar)
                await ticketlog.send(embed=embed)
            except:
                pass
        mydb.commit()
        mydb.close()

class ClosebuttonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Ticket schließen", emoji="🔒", custom_id="Button-CloseTicket", style=discord.ButtonStyle.red)
    async def button_closeticket(self, interaction, button):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID, userID FROM tickets WHERE channelID = {interaction.channel_id}")
        result = cursor.fetchone()
        if result is None:
            return
        member = interaction.user
        channel = interaction.channel
        cursor.execute("SELECT archivID, role FROM panels WHERE guildID = (%s) AND categoryID = (%s)", (interaction.guild.id, channel.category.id))
        r = cursor.fetchone()
        archiv = interaction.guild.get_channel(int(r[0]))
        user = interaction.guild.get_member(int(result[1]))
        role = interaction.guild.get_role(int(r[1]))
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False,
                send_messages=False,
            ),
            user: discord.PermissionOverwrite(
                read_messages=False,
                send_messages=False, 
            ),
            role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True, 
            )
        }
        await channel.edit(category=archiv, overwrites=overwrites)
        view = DeletebuttonView()
        await channel.send(f"{member.mention} hat das Ticket geschlossen.\nDrücke unter dieser Nachricht auf den Mülleimer um das Ticket zu löschen.", view=view)
        button.disabled = True
        await interaction.response.edit_message(view=self)

        try:
            cursor.execute(f"SELECT channelid FROM ticketlog WHERE guildid = {interaction.guild_id}")
            log = cursor.fetchone()
            if log is None:
                return
            ticketlog = interaction.guild.get_channel(int(log[0]))
            if ticketlog is None:
                return
            embed = discord.Embed(title="Ticket geschlossen", description=f"{interaction.user.mention}({interaction.user}) hat ein Ticket geschlossen. \n**Ticket:** {interaction.channel.mention}({interaction.channel.name})", color=discord.Color.gold())
            embed.set_author(name=interaction.user, icon_url=member.avatar)
            await ticketlog.send(embed=embed)
        except:
            pass
            
        mydb.commit()
        mydb.close()

    @discord.ui.button(label="Ticket claimen", emoji="🎫", custom_id="Button-ClaimTicket", style=discord.ButtonStyle.blurple)
    async def button_claimticket(self, interaction, button):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID, userID FROM tickets WHERE channelID = {interaction.channel_id}")
        result = cursor.fetchone()
        if result is None:
            return
        channel = interaction.channel
        claim = discord.Embed(color=discord.Color.green(), title="Ticket geclaimt", description=f"{interaction.guild.get_member(int(result[1])).mention}, du wirst nun von {interaction.user.mention} supportet.")
        await channel.send(embed=claim)
        button.disabled = True

        member = interaction.guild.get_member(int(result[1]))
        title = interaction.message.embeds[0].title
        description = interaction.message.embeds[0].description
        Themaheader = interaction.message.embeds[0].fields[0].name
        Thema = interaction.message.embeds[0].fields[0].value
        Claimer = interaction.message.embeds[0].fields[1].name
        authorname = interaction.message.embeds[0].author.name
        authoricon = interaction.message.embeds[0].author.icon_url
        embed = discord.Embed(title=title, description=description, color=discord.Color.orange())
        embed.set_author(name=authorname, icon_url=authoricon)
        embed.add_field(name=Themaheader, value=Thema)
        embed.add_field(name=Claimer, value=interaction.user.mention)
        await interaction.response.edit_message(content=f"{member.mention}", embed=embed, view=self)

        try:
            cursor.execute(f"SELECT channelid FROM ticketlog WHERE guildid = {interaction.guild_id}")
            log = cursor.fetchone()
            if log is None:
                return
            ticketlog = interaction.guild.get_channel(int(log[0]))
            if ticketlog is None:
                return
            embed = discord.Embed(title="Ticket geclaimt", description=f"{interaction.user.mention}({interaction.user}) hat ein Ticket geclaimt. \n**Ticket:** {interaction.channel.mention}({interaction.channel.name})\n**Thema:** {Thema}", color=discord.Color.dark_green())
            embed.set_author(name=interaction.user, icon_url=member.avatar)
            await ticketlog.send(embed=embed)
        except:
            pass

        mydb.commit()
        mydb.close()

class DeletebuttonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Ticket löschen", emoji="🗑", custom_id="Button-DeleteTicket", style=discord.ButtonStyle.red)
    async def button_deleteticket(self, interaction, button):
        await interaction.channel.send(f"{interaction.user.mention} hat das Ticket gelöscht.")
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        member = interaction.user
        channel = interaction.channel
        try:
            cursor.execute(f"SELECT channelid FROM ticketlog WHERE guildid = {interaction.guild_id}")
            log = cursor.fetchone()
            if log is None:
                pass
            ticketlog = interaction.guild.get_channel(int(log[0]))
            if ticketlog is None:
                pass
            logFile = f'{interaction.channel}.log'
            counter = 0
            with open(logFile, 'w', encoding='UTF-8') as f:
                f.write(f'Nachrichten vom Kanal: {interaction.channel} am {interaction.message.created_at.strftime("%d.%m.%Y %H:%M:%S")}\n')
                async for message in interaction.channel.history(limit=1000, oldest_first=True):
                    try:
                        attachment = '[File:: {}]'.format(message.attachments[0].url)
                    except IndexError:
                        attachment = ''
                    f.write('{} {!s:20s}: {} {}\r\n'.format(message.created_at.strftime('%d.%m.%Y %H:%M:%S'), message.author,message.clean_content, attachment))
                    counter += 1
            f = discord.File(logFile)
            os.remove(logFile)
            async for message in interaction.channel.history(limit=1, oldest_first=True):
                embed = discord.Embed(title=f"Ein Ticket wurde gelöscht", description=f"Das Ticket gehörte {message.content}.\nHier erhältst du wichtige Informationen über das gelöschte Ticket.", color=discord.Color.red())
                embed.set_footer(text=message.embeds[0].title, icon_url=message.embeds[0].author.icon_url)
                embed.add_field(name=message.embeds[0].fields[0].name, value=message.embeds[0].fields[0].value)
                embed.add_field(name=message.embeds[0].fields[1].name, value=message.embeds[0].fields[1].value)
                embed.add_field(name="Gelöscht von", value=f"{interaction.user}({interaction.user.mention})")
                embed.set_author(name=interaction.user, icon_url=member.avatar)
                await ticketlog.send(embed=embed, file=f)
                break
        except:
            pass

        cursor.execute(f"DELETE FROM tickets WHERE channelID = {channel.id}")
        await interaction.channel.delete()
        mydb.commit()
        mydb.close()

    @discord.ui.button(label="Ticket erneut öffnen", emoji="🔓", custom_id="Button-ReopenTicket", style=discord.ButtonStyle.green)
    async def button_reopenticket(self, interaction, button):
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT channelID, userID FROM tickets WHERE channelID = {interaction.channel_id}")
        result = cursor.fetchone()
        if result is None:
            return
        member = interaction.user
        channel = interaction.channel
        cursor.execute("SELECT categoryID, role FROM panels WHERE guildID = (%s) AND archivID = (%s)", (interaction.guild.id, channel.category.id))
        r = cursor.fetchone()
        category = interaction.guild.get_channel(int(r[0]))
        user = interaction.guild.get_member(int(result[1]))
        role = interaction.guild.get_role(int(r[1]))
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False,
                send_messages=False,
            ),
            user: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True, 
            ),
            role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True, 
            )
        }
        await channel.edit(category=category, overwrites=overwrites)
        await channel.send(f"{member.mention} hat das Ticket erneut geöffnet.")
        button.disabled = True
        await interaction.response.edit_message(view=self)

        try:
            cursor.execute(f"SELECT channelid FROM ticketlog WHERE guildid = {interaction.guild_id}")
            log = cursor.fetchone()
            if log is None:
                return
            ticketlog = interaction.guild.get_channel(int(log[0]))
            if ticketlog is None:
                return
            embed = discord.Embed(title="Ticket erneut geöffnet", description=f"{interaction.user.mention}({interaction.user}) hat ein Ticket erneut geöffnet. \n**Ticket:** {interaction.channel.mention}({interaction.channel.name})", color=discord.Color.gold())
            embed.set_author(name=interaction.user, icon_url=member.avatar)
            await ticketlog.send(embed=embed)
        except:
            pass

        mydb.commit()
        mydb.close()

class Ticketsystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=PanelbuttonView())
        self.bot.add_view(view=ClosebuttonView())
        self.bot.add_view(view=DeletebuttonView())

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def createpanel(self, ctx):
        """Erstelle ein Panel für Tickets."""
        a = 0
        b = 0
        embed = discord.Embed(title="__Erstelle ein Panel__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
        message = await ctx.send(embed=embed)
        await asyncio.sleep(3)

        fragen = [1, 2, 3, 4, 5, 6]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in fragen:
            b += 1
            if b == 1:
                newembed = discord.Embed(title="__Erstelle ein Panel__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                newembed.add_field(name="Kanal", value="In welchem Kanal soll das Panel sein? Bitte erwähne einen Kanal.", inline=False)
                await message.edit(embed=newembed)
            try:
                input = await self.bot.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("❌ Du hast die Fragen nicht in der vorgegebenen Zeit beantwortet. Sei beim nächstem Mal schneller!")
                return
            else:
                await input.delete()
                answers.append(input.content)
                a += 1

                if a == 1:
                    try:
                        channel_id = int(answers[0][2:-1])
                        channel = self.bot.get_channel(channel_id)
                        newembed = discord.Embed(title="__Erstelle ein Panel__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                        newembed.add_field(name="Kanal", value=channel.mention, inline=False)
                        newembed.add_field(name="Embedtext", value="Was soll im Titel des Embeds vom Panels stehen?", inline=False)
                        await message.edit(embed=newembed)
                    except:
                        newembed = discord.Embed(title="❌ __Panelsetup abgebrochen__", description=f"Du hast keinen Kanal erwähnt. Mach es beim nächstem Mal so wie: {ctx.channel.mention}", color=discord.Color.red())
                        await message.edit(embed=newembed)
                        return
                if a == 2:
                    embedtitle = answers[1]
                    newembed = discord.Embed(title="__Erstelle ein Panel__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                    newembed.add_field(name="Kanal", value=channel.mention, inline=False)
                    newembed.add_field(name="Embedtitel", value=answers[1], inline=False)
                    newembed.add_field(name="Embedbeschreibung", value="Was soll in der Beschreibung des Embeds vom Panels stehen?", inline=False)
                    await message.edit(embed=newembed)
                if a == 3:
                    embeddescription = answers[2]
                    newembed = discord.Embed(title="__Erstelle ein Panel__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                    newembed.add_field(name="Kanal", value=channel.mention, inline=False)
                    newembed.add_field(name="Embedtitel", value=answers[1], inline=False)
                    newembed.add_field(name="Embedbeschreibung", value=answers[2], inline=False)
                    newembed.add_field(name="Supportrolle", value="Welche Rolle soll Zugriff zu Tickets haben und Rechte zum Verwalten der Tickets bekommen? **Schreibe den __exakten Rollen-Name__.**", inline=False)
                    await message.edit(embed=newembed)
                if a == 4:
                    try:
                        role = discord.utils.get(ctx.guild.roles, name=answers[3])
                        if role is None or role is False:
                            newembed = discord.Embed(title="❌ __Panelsetup abgebrochen__", description=f"Rolle nicht gefunden.", color=discord.Color.red())
                            await message.edit(embed=newembed)
                            return
                        else:
                            newembed = discord.Embed(title="__Erstelle ein Panel__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                            newembed.add_field(name="Kanal", value=channel.mention, inline=False)
                            newembed.add_field(name="Embedtitel", value=answers[1], inline=False)
                            newembed.add_field(name="Embedbeschreibung", value=answers[2], inline=False)
                            newembed.add_field(name="Supportrolle", value=role.mention, inline=False)
                            newembed.add_field(name="Kategorie für offene Tickets", value="In welche Kategorie sollen geöffnete Tickets? **Gib den __exakten Namen__ der Kategorie an.**", inline=False)
                            await message.edit(embed=newembed)
                    except:
                        newembed = discord.Embed(title="❌ __Panelsetup abgebrochen__", description=f"Rolle nicht gefunden.", color=discord.Color.red())
                        await message.edit(embed=newembed)
                        return
                if a == 5:
                    try:
                        c = answers[4]
                        category = discord.utils.get(ctx.guild.categories, name=c)
                        if category is None or category is False:
                            newembed = discord.Embed(title="❌ __Panelsetup abgebrochen__", description=f"Kategorie nicht gefunden.", color=discord.Color.red())
                            await message.edit(embed=newembed)
                            return
                        else:
                            newembed = discord.Embed(title="__Erstelle ein Panel__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.blue())
                            newembed.add_field(name="Kanal", value=channel.mention, inline=False)
                            newembed.add_field(name="Embedtitel", value=answers[1], inline=False)
                            newembed.add_field(name="Embedbeschreibung", value=answers[2], inline=False)
                            newembed.add_field(name="Supportrolle", value=role.mention, inline=False)
                            newembed.add_field(name="Kategorie für offene Tickets", value=category.name, inline=False)
                            newembed.add_field(name="Kategorie für geschlossene Tickets", value="In welche Kategorie sollen geschlossene Tickets? **Gib den __exakten Namen__ der Kategorie an.**", inline=False)
                            await message.edit(embed=newembed)
                    except:
                        newembed = discord.Embed(title="❌ __Panelsetup abgebrochen__", description=f"Kategorie nicht gefunden.", color=discord.Color.red())
                        await message.edit(embed=newembed)
                        return
                if a == 6:
                    try:
                        ca = answers[5]
                        archiv = discord.utils.get(ctx.guild.categories, name=ca)
                        if archiv is None or archiv is False:
                            newembed = discord.Embed(title="❌ __Panelsetup abgebrochen__", description=f"Kategorie nicht gefunden.", color=discord.Color.red())
                            await message.edit(embed=newembed)
                            return
                        else:
                            finalemb = discord.Embed(title="__Erstelle ein Panel__", description="Beantworte die folgenden Fragen innerhalb einer Minute!", color=discord.Color.orange())
                            finalemb.add_field(name="Kanal", value=channel.mention, inline=False)
                            finalemb.add_field(name="Embedtitel", value=answers[1], inline=False)
                            finalemb.add_field(name="Embedbeschreibung", value=answers[2], inline=False)
                            finalemb.add_field(name="Supportrolle", value=role.mention, inline=False)
                            finalemb.add_field(name="Kategorie für offene Tickets", value=category.name, inline=False)
                            finalemb.add_field(name="Kategorie für geschlossene Tickets", value=archiv.name, inline=False)
                            await message.edit(embed=finalemb)
                    except:
                        newembed = discord.Embed(title="❌ __Panelsetup abgebrochen__", description=f"Kategorie nicht gefunden.", color=discord.Color.red())
                        await message.edit(embed=newembed)
                        return

        await message.edit(content=f"{ctx.author.mention} hat ein Panel erstellt.", embed=finalemb)

        embed = discord.Embed(title=embedtitle, description=embeddescription, color=discord.Color.purple())
        if ctx.guild.icon != None:
            embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(text="Reagiere mit 🎫 um ein Ticket zu erstellen")

        view = PanelbuttonView()
        m = await channel.send(embed=embed, view=view)
        #Insert in mysql
        try:
            mydb = mysql.connector.connect(
                host="54.37.204.19",
                user="u60388_adFMo8yi8w",
                password="dNPaL8=W2qapSVrwv=Q9Me8I",
                database="s60388_Vulpo"
            )
            cursor = mydb.cursor(buffered=True)
            cursor.execute("INSERT INTO panels(guildID, msgID, role, categoryID, archivID) VALUES(%s, %s, %s, %s, %s)", (ctx.guild.id, m.id, role.id, category.id, archiv.id))
            mydb.commit()
            mydb.close()
            await ctx.message.delete()
        except Exception as e:
            return await ctx.send(e)
            
            
async def setup(bot):
    await bot.add_cog(Ticketsystem(bot))