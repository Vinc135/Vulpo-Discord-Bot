import asyncio
import typing
import discord
from discord.ext import commands
from discord import app_commands
from info import random_color, discord_timestamp
import math
import datetime
from info import getcolour

class tictactoeherausforderung2(discord.ui.View):
    def __init__(self, member: discord.Member=None, membertwo: discord.Member=None, bot=None):
        super().__init__(timeout=None)
        self.member = member
        self.membertwo = membertwo
        self.bot = bot

    @discord.ui.button(label='Akzeptieren', style=discord.ButtonStyle.green, custom_id="rgwrg4wghwrtherther")
    async def ja(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id != interaction.user.id:
            return await interaction.response.defer(thinking=False)
        await interaction.response.edit_message(content=f"**Tik-Tak-Toe BIG**\n{self.member.mention} wurde herausgefordert von {self.membertwo.mention}. Es steht noch kein Gewinner fest.\n**{self.membertwo.mention} ist am Zuge.**", view=TicTacToe2(interaction.user, self.membertwo, self.bot))

    @discord.ui.button(label='Ablehnen', style=discord.ButtonStyle.red, custom_id="wrthwrghwrthwrthrthwrht")
    async def nein(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id != interaction.user.id:
            return await interaction.response.defer(thinking=False)
        await interaction.response.edit_message(content=f"**Tik-Tak-Toe BIG**\n{self.member.mention} wurde herausgefordert von {self.membertwo.mention}. Das Match wurde nicht angenommen.", view=None)
        
class TicTacToeButton2(discord.ui.Button):
    def __init__(self, x: int=None, y: int=None, playerone: discord.Member=None, playertwo: discord.Member=None, bot=None):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y
        self.playerone = playerone
        self.playertwo = playertwo
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            if self.playertwo.id != interaction.user.id:
                return await interaction.response.defer(thinking=False)
            self.style = discord.ButtonStyle.danger
            self.label = '❌'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = f"**Tik-Tak-Toe BIG**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. Es steht noch kein Gewinner fest.\n**{self.playerone.mention} ist am Zuge.**"
        else:
            if self.playerone.id != interaction.user.id:
                return await interaction.response.defer(thinking=False)
            self.style = discord.ButtonStyle.success
            self.label = '⭕️'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = f"**Tik-Tak-Toe BIG**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. Es steht noch kein Gewinner fest.\n**{self.playertwo.mention} ist am Zuge.**"

        winner = view.check_board_winner()
        if winner is not None:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playerone.id))
                    result1 = await cursor.fetchone()
                    await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playertwo.id))
                    result2 = await cursor.fetchone()
                    
                    
                    if winner == view.X:
                        content = f'**Tik-Tak-Toe BIG**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. **{self.playertwo.mention} hat dieses Match gewonnen.**\n*Noch ein Spiel?*'
                        await cursor.execute("UPDATE ttt SET wins = (%s) WHERE userID = (%s)", (result2[0] + 1, self.playertwo.id))
                        await cursor.execute("UPDATE ttt SET loses = (%s) WHERE userID = (%s)", (result1[1] + 1, self.playerone.id))
                        await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playerone.id))
                        rating1 = await cursor.fetchone()
                        await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playertwo.id))
                        rating2 = await cursor.fetchone()
                        await cursor.execute("UPDATE ttt SET rating = (%s) WHERE userID = (%s)", ((rating2[0] * 3) + (rating2[1] * -1) + (rating2[2] * 2), self.playertwo.id))
                        await cursor.execute("UPDATE ttt SET rating = (%s) WHERE userID = (%s)", ((rating1[0] * 3) + (rating1[1] * -1) + (rating1[2] * 2), self.playerone.id))
                    elif winner == view.O:
                        content = f'**Tik-Tak-Toe BIG**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. **{self.playerone.mention} hat dieses Match gewonnen.**\n*Noch ein Spiel?*'
                        await cursor.execute("UPDATE ttt SET loses = (%s) WHERE userID = (%s)", (result2[1] + 1, self.playertwo.id))
                        await cursor.execute("UPDATE ttt SET wins = (%s) WHERE userID = (%s)", (result1[0] + 1, self.playerone.id))
                        await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playerone.id))
                        rating1 = await cursor.fetchone()
                        await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playertwo.id))
                        rating2 = await cursor.fetchone()
                        await cursor.execute("UPDATE ttt SET rating = (%s) WHERE userID = (%s)", ((rating2[0] * 3) + (rating2[1] * -1) + (rating2[2] * 2), self.playertwo.id))
                        await cursor.execute("UPDATE ttt SET rating = (%s) WHERE userID = (%s)", ((rating1[0] * 3) + (rating1[1] * -1) + (rating1[2] * 2), self.playerone.id))
                    else:
                        content = f'**Tik-Tak-Toe BIG**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. **Es gab keinen Gewinner. Unentschieden.**\n*Noch ein Spiel?*'
                        await cursor.execute("UPDATE ttt SET ties = (%s) WHERE userID = (%s)", (result2[2] + 1, self.playertwo.id))
                        await cursor.execute("UPDATE ttt SET ties = (%s) WHERE userID = (%s)", (result1[2] + 1, self.playerone.id))
                        await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playerone.id))
                        rating1 = await cursor.fetchone()
                        await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playertwo.id))
                        rating2 = await cursor.fetchone()
                        await cursor.execute("UPDATE ttt SET rating = (%s) WHERE userID = (%s)", ((rating2[0] * 3) + (rating2[1] * -1) + (rating2[2] * 2), self.playertwo.id))
                        await cursor.execute("UPDATE ttt SET rating = (%s) WHERE userID = (%s)", ((rating1[0] * 3) + (rating1[1] * -1) + (rating1[2] * 2), self.playerone.id))

                    for child in view.children:
                        child.disabled = True

                    view.stop()

        await interaction.response.edit_message(content=content, view=view)

class TicTacToe2(discord.ui.View):
    children: typing.List[TicTacToeButton2]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, playerone: discord.Member=None, playertwo: discord.Member=None, bot=None):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.playerone = playerone
        self.playertwo = playertwo
        self.bot = bot
        for x in range(4):
            for y in range(4):
                self.add_item(TicTacToeButton2(x, y, self.playerone, self.playertwo, self.bot))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 4:
                return self.O
            elif value == -4:
                return self.X

        for line in range(4):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line] + self.board[3][line]
            if value == 4:
                return self.O
            elif value == -4:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 4:
            return self.O
        elif diag == -4:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2] + self.board[3][3]
        if diag == 4:
            return self.O
        elif diag == -4:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None




class tictactoeherausforderung(discord.ui.View):
    def __init__(self, member: discord.Member=None, membertwo: discord.Member=None, bot=None):
        super().__init__(timeout=None)
        self.member = member
        self.membertwo = membertwo
        self.bot = bot

    @discord.ui.button(label='Akzeptieren', style=discord.ButtonStyle.green, custom_id="whwrhwrthwrhtwrth")
    async def ja(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id != interaction.user.id:
            return await interaction.response.defer(thinking=False)
        await interaction.response.edit_message(content=f"**Tik-Tak-Toe**\n{self.member.mention} wurde herausgefordert von {self.membertwo.mention}. Es steht noch kein Gewinner fest.\n**{self.membertwo.mention} ist am Zuge.**", view=TicTacToe(interaction.user, self.membertwo, self.bot))

    @discord.ui.button(label='Ablehnen', style=discord.ButtonStyle.red, custom_id="rhtsrtze5getgrthet")
    async def nein(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id != interaction.user.id:
            return await interaction.response.defer(thinking=False)
        await interaction.response.edit_message(content=f"**Tik-Tak-Toe**\n{self.member.mention} wurde herausgefordert von {self.membertwo.mention}. Das Match wurde nicht angenommen.", view=None)
        
class TicTacToeButton(discord.ui.Button):
    def __init__(self, x: int=None, y: int=None, playerone: discord.Member=None, playertwo: discord.Member=None, bot=None):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y
        self.playerone = playerone
        self.playertwo = playertwo
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            if self.playertwo.id != interaction.user.id:
                return await interaction.response.defer(thinking=False)
            self.style = discord.ButtonStyle.danger
            self.label = '❌'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = f"**Tik-Tak-Toe**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. Es steht noch kein Gewinner fest.\n**{self.playerone.mention} ist am Zuge.**"
        else:
            if self.playerone.id != interaction.user.id:
                return await interaction.response.defer(thinking=False)
            self.style = discord.ButtonStyle.success
            self.label = '⭕️'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = f"**Tik-Tak-Toe**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. Es steht noch kein Gewinner fest.\n**{self.playertwo.mention} ist am Zuge.**"

        winner = view.check_board_winner()
        if winner is not None:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playerone.id))
                    result1 = await cursor.fetchone()
                    await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playertwo.id))
                    result2 = await cursor.fetchone()
                    
                    
                    if winner == view.X:
                        content = f'**Tik-Tak-Toe**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. **{self.playertwo.mention} hat dieses Match gewonnen.**\n*Noch ein Spiel?*'
                        await cursor.execute("UPDATE ttt SET wins = (%s) WHERE userID = (%s)", (result2[0] + 1, self.playertwo.id))
                        await cursor.execute("UPDATE ttt SET loses = (%s) WHERE userID = (%s)", (result1[1] + 1, self.playerone.id))
                        await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playerone.id))
                        rating1 = await cursor.fetchone()
                        await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playertwo.id))
                        rating2 = await cursor.fetchone()
                        await cursor.execute("UPDATE ttt SET rating = (%s) WHERE userID = (%s)", ((rating2[0] * 3) + (rating2[1] * -1) + (rating2[2] * 2), self.playertwo.id))
                        await cursor.execute("UPDATE ttt SET rating = (%s) WHERE userID = (%s)", ((rating1[0] * 3) + (rating1[1] * -1) + (rating1[2] * 2), self.playerone.id))
                    elif winner == view.O:
                        content = f'**Tik-Tak-Toe**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. **{self.playerone.mention} hat dieses Match gewonnen.**\n*Noch ein Spiel?*'
                        await cursor.execute("UPDATE ttt SET loses = (%s) WHERE userID = (%s)", (result2[1] + 1, self.playertwo.id))
                        await cursor.execute("UPDATE ttt SET wins = (%s) WHERE userID = (%s)", (result1[0] + 1, self.playerone.id))
                        await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playerone.id))
                        rating1 = await cursor.fetchone()
                        await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playertwo.id))
                        rating2 = await cursor.fetchone()
                        await cursor.execute("UPDATE ttt SET rating = (%s) WHERE userID = (%s)", ((rating2[0] * 3) + (rating2[1] * -1) + (rating2[2] * 2), self.playertwo.id))
                        await cursor.execute("UPDATE ttt SET rating = (%s) WHERE userID = (%s)", ((rating1[0] * 3) + (rating1[1] * -1) + (rating1[2] * 2), self.playerone.id))
                    else:
                        content = f'**Tik-Tak-Toe**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. **Es gab keinen Gewinner. Unentschieden.**\n*Noch ein Spiel?*'
                        await cursor.execute("UPDATE ttt SET ties = (%s) WHERE userID = (%s)", (result2[2] + 1, self.playertwo.id))
                        await cursor.execute("UPDATE ttt SET ties = (%s) WHERE userID = (%s)", (result1[2] + 1, self.playerone.id))
                        await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playerone.id))
                        rating1 = await cursor.fetchone()
                        await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (self.playertwo.id))
                        rating2 = await cursor.fetchone()
                        await cursor.execute("UPDATE ttt SET rating = (%s) WHERE userID = (%s)", ((rating2[0] * 3) + (rating2[1] * -1) + (rating2[2] * 2), self.playertwo.id))
                        await cursor.execute("UPDATE ttt SET rating = (%s) WHERE userID = (%s)", ((rating1[0] * 3) + (rating1[1] * -1) + (rating1[2] * 2), self.playerone.id))

                    for child in view.children:
                        child.disabled = True

                    view.stop()

        await interaction.response.edit_message(content=content, view=view)

class TicTacToe(discord.ui.View):
    children: typing.List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, playerone: discord.Member=None, playertwo: discord.Member=None, bot=None):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.playerone = playerone
        self.playertwo = playertwo
        self.bot = bot
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y, self.playerone, self.playertwo, self.bot))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

class Ttt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view=tictactoeherausforderung(None, None, self.bot))
        self.bot.add_view(view=tictactoeherausforderung2(None, None, self.bot))

    tictactoe = app_commands.Group(name='tictactoe', description='Alle Commands vom Tictactoe System.', guild_only=True)

    @tictactoe.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def start(self, interaction: discord.Interaction, spieler2: discord.Member, modus: typing.Literal["Klassisch", "BIG"]):
        """Spiele mit jemanden Tik-Tik-Toe."""
        if modus == "Klassisch":
            if spieler2 == interaction.user:
                return await interaction.response.send_message("**❌ Du kannst nicht gegen dich selbst spielen.**", ephemeral=True)
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (interaction.user.id))
                    result1 = await cursor.fetchone()
                    if result1 == None:
                        await cursor.execute("INSERT INTO ttt (userID, wins, loses, ties) VALUES (%s, %s, %s, %s)", (interaction.user.id, 0, 0, 0))

                    await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (spieler2.id))
                    result2 = await cursor.fetchone()
                    if result2 == None:
                        await cursor.execute("INSERT INTO ttt (userID, wins, loses, ties) VALUES (%s, %s, %s, %s)", (spieler2.id, 0, 0, 0))
            
            t1 = math.floor(datetime.datetime.utcnow().timestamp() + 300)
            t2 = datetime.datetime.fromtimestamp(int(t1))
            await interaction.response.send_message(f'**Tik-Tak-Toe**\n{spieler2.mention}, du wurdest von {interaction.user.mention} herausgefordert.\n*Die Herausforderung läuft {discord_timestamp(t2, "R")} aus.*', view=tictactoeherausforderung(spieler2, interaction.user, self.bot))
            await asyncio.sleep(300)
            message = await interaction.original_response()
            if "Die Herausforderung läuft" in message.content:
                await interaction.edit_original_response(content=f"**Tik-Tak-Toe**\n{spieler2.mention}, du wurdest von {interaction.user.mention} herausgefordert. Jedoch ist die Zeit abgelaufen, dem Match beizutreten.", view=None)
        if modus == "BIG":
            if spieler2 == interaction.user:
                return await interaction.response.send_message("**❌ Du kannst nicht gegen dich selbst spielen.**", ephemeral=True)
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (interaction.user.id))
                    result1 = await cursor.fetchone()
                    if result1 == None:
                        await cursor.execute("INSERT INTO ttt (userID, wins, loses, ties) VALUES (%s, %s, %s, %s)", (interaction.user.id, 0, 0, 0))

                    await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (spieler2.id))
                    result2 = await cursor.fetchone()
                    if result2 == None:
                        await cursor.execute("INSERT INTO ttt (userID, wins, loses, ties) VALUES (%s, %s, %s, %s)", (spieler2.id, 0, 0, 0))
            
            t1 = math.floor(datetime.datetime.utcnow().timestamp() + 300)
            t2 = datetime.datetime.fromtimestamp(int(t1))
            await interaction.response.send_message(f'**Tik-Tak-Toe**\n{spieler2.mention}, du wurdest von {interaction.user.mention} herausgefordert.\n*Die Herausforderung läuft {discord_timestamp(t2, "R")} aus.*', view=tictactoeherausforderung2(spieler2, interaction.user, self.bot))
            await asyncio.sleep(300)
            message = await interaction.original_response()
            if "Die Herausforderung läuft" in message.content:
                await interaction.edit_original_response(content=f"**Tik-Tak-Toe BIG**\n{spieler2.mention}, du wurdest von {interaction.user.mention} herausgefordert. Jedoch ist die Zeit abgelaufen, dem Match beizutreten.", view=None)
    
    @tictactoe.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def stats(self, interaction: discord.Interaction, member: discord.Member=None):
        """Sieh dir deine Tik Tak Toe Stats an."""
        if member == None:
            member = interaction.user
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT wins, loses, ties FROM ttt WHERE userID = (%s)", (member.id))
                result = await cursor.fetchone()
                if result == None:
                    if member == interaction.user:
                        return await interaction.response.send_message("**❌ Du hast noch kein Match gespielt. Aufgrund dessen hast du auch keine Punkte. Du musst zuerst ein Match spielen.**", ephemeral=True)
                    return await interaction.response.send_message(f"**❌ {member.mention} hat noch kein Match gespielt. Aufgrund dessen hat er/sie auch keine Punkte. Er/Sie muss zuerst ein Match spielen.**", ephemeral=True)
                else:
                    rating = (result[0] * 3) + (result[1] * -1) + (result[2] * 2)
                    total_plays = result[0] + result[1] + result[2]
                    embed = discord.Embed(color=await getcolour(self, interaction.user), title="❌ **| __TicTacToe Stats__ |** ⭕", description=f"""
Aktuelle Stats von {member.mention}
**Rating: `{rating}`**

Insgesamt gespielte Spiele: `{total_plays}`
Davon gewonnen: `{total_plays - result[1] - result[2]}`
Davon unentschieden: `{total_plays - result[0] - result[1]}`
Davon verloren: `{total_plays - result[0] - result[2]}`""")
                    embed.set_thumbnail(url=member.avatar)
                    await interaction.response.send_message(embed=embed)
                
async def setup(bot):
    await bot.add_cog(Ttt(bot))