import asyncio
import typing
import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import random_color, discord_timestamp, getcolour
import math
import datetime
from utils.MongoDB import getMongoDataBase

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

        db = getMongoDataBase()

        winner = view.check_board_winner()
        
        
        if winner is None:
            return
        
        playerone = db["ttt"].find_one({"userID": self.playerone.id})
        playertwo = db["ttt"].find_one({"userID": self.playertwo.id})
        
        if winner == view.X:
            content = f'**Tik-Tak-Toe BIG**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. **{self.playertwo.mention} hat dieses Match gewonnen.**\n*Noch ein Spiel?*'
            
            db["ttt"].update_one({"userID": self.playertwo.id}, {"$set": {"wins": playertwo["wins"] + 1}})
            db["ttt"].update_one({"userID": self.playerone.id}, {"$set": {"loses": playerone["loses"] + 1}})
            rating1 = (playerone["wins"] * 3) + (playerone["loses"] * -1) + (playerone["ties"] * 2)
            rating2 = (playertwo["wins"] * 3) + (playertwo["loses"] * -1) + (playertwo["ties"] * 2)
            db["ttt"].update_one({"userID": self.playertwo.id}, {"$set": {"rating": rating2}})
            db["ttt"].update_one({"userID": self.playerone.id}, {"$set": {"rating": rating1}})
        elif winner == view.O:
            content = f'**Tik-Tak-Toe BIG**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. **{self.playerone.mention} hat dieses Match gewonnen.**\n*Noch ein Spiel?*'
            db["ttt"].update_one({"userID": self.playertwo.id}, {"$set": {"loses": playertwo["loses"] + 1}})
            db["ttt"].update_one({"userID": self.playerone.id}, {"$set": {"wins": playerone["wins"] + 1}})
            rating1 = (playerone["wins"] * 3) + (playerone["loses"] * -1) + (playerone["ties"] * 2)
            rating2 = (playertwo["wins"] * 3) + (playertwo["loses"] * -1) + (playertwo["ties"] * 2)
            db["ttt"].update_one({"userID": self.playertwo.id}, {"$set": {"rating": rating2}})
            db["ttt"].update_one({"userID": self.playerone.id}, {"$set": {"rating": rating1}})
        else:
            content = f'**Tik-Tak-Toe BIG**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. **Es gab keinen Gewinner. Unentschieden.**\n*Noch ein Spiel?*'
            db["ttt"].update_one({"userID": self.playertwo.id}, {"$set": {"ties": playertwo["ties"] + 1}})
            db["ttt"].update_one({"userID": self.playerone.id}, {"$set": {"ties": playerone["ties"] + 1}})
            rating1 = (playerone["wins"] * 3) + (playerone["loses"] * -1) + (playerone["ties"] * 2)
            rating2 = (playertwo["wins"] * 3) + (playertwo["loses"] * -1) + (playertwo["ties"] * 2)
            db["ttt"].update_one({"userID": self.playertwo.id}, {"$set": {"rating": rating2}})
            db["ttt"].update_one({"userID": self.playerone.id}, {"$set": {"rating": rating1}})
            
        for child in view.children:
            child.disabled = True
        
        return await interaction.response.edit_message(content=content, view=view)

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
        
        db = getMongoDataBase()
        
        if winner is None:
            return
        
        playerone = db["ttt"].find_one({"userID": self.playerone.id})
        playertwo = db["ttt"].find_one({"userID": self.playertwo.id})
        
        if winner == view.X:
            content = f'**Tik-Tak-Toe**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. **{self.playertwo.mention} hat dieses Match gewonnen.**\n*Noch ein Spiel?*'
            
            db["ttt"].update_one({"userID": self.playertwo.id}, {"$set": {"wins": playertwo["wins"] + 1}})
            db["ttt"].update_one({"userID": self.playerone.id}, {"$set": {"loses": playerone["loses"] + 1}})
            rating1 = (playerone["wins"] * 3) + (playerone["loses"] * -1) + (playerone["ties"] * 2)
            rating2 = (playertwo["wins"] * 3) + (playertwo["loses"] * -1) + (playertwo["ties"] * 2)
            db["ttt"].update_one({"userID": self.playertwo.id}, {"$set": {"rating": rating2}})
            db["ttt"].update_one({"userID": self.playerone.id}, {"$set": {"rating": rating1}})
        elif winner == view.O:
            content = f'**Tik-Tak-Toe**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. **{self.playerone.mention} hat dieses Match gewonnen.**\n*Noch ein Spiel?*'
            db["ttt"].update_one({"userID": self.playertwo.id}, {"$set": {"loses": playertwo["loses"] + 1}})
            db["ttt"].update_one({"userID": self.playerone.id}, {"$set": {"wins": playerone["wins"] + 1}})
            rating1 = (playerone["wins"] * 3) + (playerone["loses"] * -1) + (playerone["ties"] * 2)
            rating2 = (playertwo["wins"] * 3) + (playertwo["loses"] * -1) + (playertwo["ties"] * 2)
            db["ttt"].update_one({"userID": self.playertwo.id}, {"$set": {"rating": rating2}})
            db["ttt"].update_one({"userID": self.playerone.id}, {"$set": {"rating": rating1}})
        else:
            content = f'**Tik-Tak-Toe**\n{self.playerone.mention} wurde herausgefordert von {self.playertwo.mention}. **Es gab keinen Gewinner. Unentschieden.**\n*Noch ein Spiel?*'
            db["ttt"].update_one({"userID": self.playertwo.id}, {"$set": {"ties": playertwo["ties"] + 1}})
            db["ttt"].update_one({"userID": self.playerone.id}, {"$set": {"ties": playerone["ties"] + 1}})
            rating1 = (playerone["wins"] * 3) + (playerone["loses"] * -1) + (playerone["ties"] * 2)
            rating2 = (playertwo["wins"] * 3) + (playertwo["loses"] * -1) + (playertwo["ties"] * 2)
            db["ttt"].update_one({"userID": self.playertwo.id}, {"$set": {"rating": rating2}})
            db["ttt"].update_one({"userID": self.playerone.id}, {"$set": {"rating": rating1}})
        
        for child in view.children:
            child.disabled = True
            
        return await interaction.response.edit_message(content=content, view=view)

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
        """Spiele mit jemanden tictactoe"""
        
        await interaction.response.defer()
        
        db = getMongoDataBase()
        
        if modus == "Klassisch":
            if spieler2 == interaction.user:
                return await interaction.followup.send("**❌ Du kannst nicht gegen dich selbst spielen.**", ephemeral=True)
            
            playerone = await db["ttt"].find_one({"userID": interaction.user.id})
            
            if playerone == None:
                await db["ttt"].insert_one({"userID": interaction.user.id, "wins": 0, "loses": 0, "ties": 0, "rating": 0})
                
            playertwo = await db["ttt"].find_one({"userID": spieler2.id})
            
            if playertwo == None:
                await db["ttt"].insert_one({"userID": spieler2.id, "wins": 0, "loses": 0, "ties": 0, "rating": 0})
            
            t1 = math.floor(datetime.datetime.now().timestamp() + 300)
            t2 = datetime.datetime.fromtimestamp(int(t1))
            await interaction.followup.send(f'**Tik-Tak-Toe**\n{spieler2.mention}, du wurdest von {interaction.user.mention} herausgefordert.\n*Die Herausforderung läuft {discord_timestamp(t2, "R")} aus.*', view=tictactoeherausforderung(spieler2, interaction.user, self.bot))
            await asyncio.sleep(300)
            message = await interaction.original_response()
            if "Die Herausforderung läuft" in message.content:
                await interaction.edit_original_response(content=f"**Tik-Tak-Toe**\n{spieler2.mention}, du wurdest von {interaction.user.mention} herausgefordert. Jedoch ist die Zeit abgelaufen, dem Match beizutreten.", view=None)
        if modus == "BIG":
            if spieler2 == interaction.user:
                return await interaction.followup.send("**❌ Du kannst nicht gegen dich selbst spielen.**", ephemeral=True)
            
            playerone = await db["ttt"].find_one({"userID": interaction.user.id})
            
            if playerone == None:
                await db["ttt"].insert_one({"userID": interaction.user.id, "wins": 0, "loses": 0, "ties": 0, "rating": 0})
                
            playertwo = await db["ttt"].find_one({"userID": spieler2.id})
            
            if playertwo == None:
                await db["ttt"].insert_one({"userID": spieler2.id, "wins": 0, "loses": 0, "ties": 0, "rating": 0})
            
            t1 = math.floor(datetime.datetime.now().timestamp() + 300)
            t2 = datetime.datetime.fromtimestamp(int(t1))
            await interaction.followup.send(f'**Tik-Tak-Toe**\n{spieler2.mention}, du wurdest von {interaction.user.mention} herausgefordert.\n*Die Herausforderung läuft {discord_timestamp(t2, "R")} aus.*', view=tictactoeherausforderung2(spieler2, interaction.user, self.bot))
            await asyncio.sleep(300)
            message = await interaction.original_response()
            if "Die Herausforderung läuft" in message.content:
                await interaction.edit_original_response(content=f"**Tik-Tak-Toe BIG**\n{spieler2.mention}, du wurdest von {interaction.user.mention} herausgefordert. Jedoch ist die Zeit abgelaufen, dem Match beizutreten.", view=None)
    
    @tictactoe.command()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def stats(self, interaction: discord.Interaction, member: discord.Member=None):
        """Sieh dir deine tictactoe Stats an."""
        
        await interaction.response.defer()
        
        if member == None:
            member = interaction.user
            
        db = getMongoDataBase()
        
        result = await db["ttt"].find_one({"userID": member.id})
        
        if result == None:
            if member == interaction.user:
                return await interaction.followup.send("**❌ Du hast noch kein Match gespielt. Aufgrund dessen hast du auch keine Punkte. Du musst zuerst ein Match spielen.**", ephemeral=True)
            return await interaction.followup.send(f"**❌ {member.mention} hat noch kein Match gespielt. Aufgrund dessen hat er/sie auch keine Punkte. Er/Sie muss zuerst ein Match spielen.**", ephemeral=True)
        
        rating = (result["wins"] * 3) + (result["loses"] * -1) + (result["ties"] * 2)
        total_plays = result["wins"] + result["loses"] + result["ties"]
        embed = discord.Embed(color=await getcolour(self, interaction.user), title="❌ **| __TicTacToe Stats__ |** ⭕", description=f"""
Aktuelle Stats von {member.mention}
**Rating: `{rating}`**

Insgesamt gespielte Spiele: `{total_plays}`
Davon gewonnen: `{result["wins"]}`
Davon unentschieden: `{result["ties"]}`
Davon verloren: `{result["loses"]}`""")
        
        embed.set_thumbnail(url=member.avatar)
        
        await interaction.followup.send(embed=embed)
                
async def setup(bot):
    await bot.add_cog(Ttt(bot))