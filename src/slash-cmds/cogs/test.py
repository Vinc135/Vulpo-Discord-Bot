@bot.listen()
async def on_dbl_vote(data):
    if data["type"] == "test":
        return bot.dispatch('dbl_test', data)
    print("VOTE TRIGGERED")
    userid = data["user"]
    user = await bot.fetch_user(userid)
    server = bot.get_guild(989961082833608795)
    channel = server.get_channel(1023129908282658856)
    role = server.get_role(1003224529679683625)
    timelol = int(float(time.time()))
    async with bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SELECT lastvote, votecount FROM TopggVotes WHERE user_id = {user.id}")
            result = await cursor.fetchone()
            if result is None:
                await cursor.execute("INSERT INTO TopggVotes (user_id, votecount, lastvote, reminder) VALUES (%s, %s, %s, %s)",                                   
                                     (user.id, 0, time.time(), "nein"))
                await conn.commit() #muss nicht, wenn bei der pool erstellung autocommit = True gesetzt wurde.
                
            if result:
                await cursor.execute(f"UPDATE TopggVotes SET votecount = {int(result[1]) + 1} AND lastvote = {time.time()} WHERE user_id = {user.id}")
                await conn.commit() #muss nicht, wenn bei der pool erstellung autocommit = True gesetzt wurde.
            embed = discord.Embed(title=f"Danke {user}!",
                              		  description=f"{user.mention} hat nun insgesamt **{int(result[1]) + 1}** mal gevotet!\nAls Belohnung erhälst du die {role.mention} Rolle für **12** Stunden!\nDu kannst **[hier](https://top.gg/bot/965564884572065874/vote)** in <t:{timelol + 43200}:R> wieder voten!",
                              		  color=0xff3366)
            embed.set_author(name=user, icon_url=user.display_avatar.url)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/949420891702427688/1022554132621566052/NeverGonnaGiveYouUp-01.png?width=848&height=848")
            if user in server.members:
                try:
                    member = server.get_member(int(user.id))
                    await member.add_roles(role, reason="Topgg Vote")
                    embed.set_footer(text=f"Als Dankeschön bekommst du die {role.name} Rolle für 12 Stunden!",
                                        icon_url=server.icon.url)
                except:
                    embed.set_footer(text="Es gab leider einen Fehler beim hinzufügen der Voter Rolle!",
                                        icon_url=server.icon.url)
            else:
                embed.set_footer(text="Der User ist nicht auf diesem Server!", icon_url=server.icon.url)
                embed2 = discord.Embed(title=f"Danke {user}!", description=f"{user.mention} hat nun insgesamt **{int(result[1]) + 1}** mal gevotet!\nAls Belohnung erhälst du die {role.mention} Rolle für **12** Stunden!\nDu kannst **[hier](https://top.gg/bot/965564884572065874/vote)** in <t:{timelol + 43200}:R> wieder voten!",
                               		color=0xff3366)
                embed2.set_thumbnail(url="https://media.discordapp.net/attachments/949420891702427688/1022554132621566052/NeverGonnaGiveYouUp-01.png?width=848&height=848")
                view3 = View()
                view3.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="Vote wieder", url="https://top.gg/bot/965564884572065874/vote"))
                await channel.send(embed=embed, view=view3)

@bot.listen()
async def on_dbl_test(data):
    print("VOTE TEST TRIGGERED")
    userid = data["user"]
    user = await bot.fetch_user(userid)
    server = bot.get_guild(989961082833608795)
    channel = server.get_channel(1023129908282658856)
    role = server.get_role(1003224529679683625)
    timelol = int(float(time.time()))
    async with bot.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SELECT lastvote, votecount FROM TopggVotes WHERE user_id = {user.id}")
            result = await cursor.fetchone()
            if result is None:
                await cursor.execute("INSERT INTO TopggVotes (user_id, votecount, lastvote, reminder) VALUES (%s, %s, %s, %s)",                                   
                                     (user.id, 0, time.time(), "nein"))
                await conn.commit() #muss nicht, wenn bei der pool erstellung autocommit = True gesetzt wurde.
                
            if result:
                await cursor.execute(f"UPDATE TopggVotes SET votecount = {int(result[1]) + 1} AND lastvote = {time.time()} WHERE user_id = {user.id}")
                await conn.commit() #muss nicht, wenn bei der pool erstellung autocommit = True gesetzt wurde.
            embed = discord.Embed(title=f"Danke {user}!",
                              		  description=f"{user.mention} hat nun insgesamt **{int(result[1]) + 1}** mal gevotet!\nAls Belohnung erhälst du die {role.mention} Rolle für **12** Stunden!\nDu kannst **[hier](https://top.gg/bot/965564884572065874/vote)** in <t:{timelol + 43200}:R> wieder voten!",
                              		  color=0xff3366)
            embed.set_author(name=user, icon_url=user.display_avatar.url)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/949420891702427688/1022554132621566052/NeverGonnaGiveYouUp-01.png?width=848&height=848")
            if user in server.members:
                try:
                    member = server.get_member(int(user.id))
                    await member.add_roles(role, reason="Topgg Vote")
                    embed.set_footer(text=f"Als Dankeschön bekommst du die {role.name} Rolle für 12 Stunden!",
                                        icon_url=server.icon.url)
                except:
                    embed.set_footer(text="Es gab leider einen Fehler beim hinzufügen der Voter Rolle!",
                                        icon_url=server.icon.url)
            else:
                embed.set_footer(text="Der User ist nicht auf diesem Server!", icon_url=server.icon.url)
                embed2 = discord.Embed(title=f"Danke {user}!", description=f"{user.mention} hat nun insgesamt **{int(result[1]) + 1}** mal gevotet!\nAls Belohnung erhälst du die {role.mention} Rolle für **12** Stunden!\nDu kannst **[hier](https://top.gg/bot/965564884572065874/vote)** in <t:{timelol + 43200}:R> wieder voten!",
                               		color=0xff3366)
                embed2.set_thumbnail(url="https://media.discordapp.net/attachments/949420891702427688/1022554132621566052/NeverGonnaGiveYouUp-01.png?width=848&height=848")
                view3 = View()
                view3.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="Vote wieder", url="https://top.gg/bot/965564884572065874/vote"))
                await channel.send(embed=embed, view=view3) 