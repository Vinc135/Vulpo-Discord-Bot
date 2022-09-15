import discord
from discord.ext import commands
import aiohttp
import mysql.connector

class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["pus"])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pussy(self, ctx):
        """Schickt ein Foto einer Pussy."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT endtime FROM vote WHERE userid = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None or result is False:
            embed = discord.Embed(title="❌ Zugriff verweigert", description="Um diesen Command zu nutzen, musst du voten.\nVote hier: https://top.gg/bot/925799559576322078/vote", color=discord.Color.green(), url="https://top.gg/bot/925799559576322078/vote")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            mydb.close()
            return
        else:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://www.reddit.com/r/pussy/random/.json') as r:
                    res = await r.json()

                    image = res[0]['data']['children'][0]['data']['url']
                    permalink = res[0]['data']['children'][0]['data']['permalink']
                    url = f'https://reddit.com{permalink}'
                    title = res[0]['data']['children'][0]['data']['title']
                    ups = res[0]['data']['children'][0]['data']['ups']
                    comments = res[0]['data']['children'][0]['data']['num_comments']

                    embed = discord.Embed(colour=discord.Colour.blue(), title=title, url=url)
                    embed.set_image(url=image)
                    embed.set_footer(text=f"🔺 {ups} | 💬 {comments} ")
                    await ctx.send(embed=embed, content=None)

    @commands.command(aliases=["as"])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ass(self, ctx):
        """Schickt ein Foto eines Arsches."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT endtime FROM vote WHERE userid = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None or result is False:
            embed = discord.Embed(title="❌ Zugriff verweigert", description="Um diesen Command zu nutzen, musst du voten.\nVote hier: https://top.gg/bot/925799559576322078/vote", color=discord.Color.green(), url="https://top.gg/bot/925799559576322078/vote")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            mydb.close()
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/ass/random/.json') as r:
                res = await r.json()

                image = res[0]['data']['children'][0]['data']['url']
                permalink = res[0]['data']['children'][0]['data']['permalink']
                url = f'https://reddit.com{permalink}'
                title = res[0]['data']['children'][0]['data']['title']
                ups = res[0]['data']['children'][0]['data']['ups']
                comments = res[0]['data']['children'][0]['data']['num_comments']

                embed = discord.Embed(colour=discord.Colour.blue(), title=title, url=url)
                embed.set_image(url=image)
                embed.set_footer(text=f"🔺 {ups} | 💬 {comments} ")
                await ctx.send(embed=embed, content=None)

    @commands.command(aliases=["boobies"])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boobs(self, ctx):
        """Schickt ein Foto von Brüsten."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT endtime FROM vote WHERE userid = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None or result is False:
            embed = discord.Embed(title="❌ Zugriff verweigert", description="Um diesen Command zu nutzen, musst du voten.\nVote hier: https://top.gg/bot/925799559576322078/vote", color=discord.Color.green(), url="https://top.gg/bot/925799559576322078/vote")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            mydb.close()
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/boobs/random/.json') as r:
                res = await r.json()

                image = res[0]['data']['children'][0]['data']['url']
                permalink = res[0]['data']['children'][0]['data']['permalink']
                url = f'https://reddit.com{permalink}'
                title = res[0]['data']['children'][0]['data']['title']
                ups = res[0]['data']['children'][0]['data']['ups']
                comments = res[0]['data']['children'][0]['data']['num_comments']

                embed = discord.Embed(colour=discord.Colour.blue(), title=title, url=url)
                embed.set_image(url=image)
                embed.set_footer(text=f"🔺 {ups} | 💬 {comments} ")
                await ctx.send(embed=embed, content=None)
    
    @commands.command(aliases=["yif"])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def yiff(self, ctx):
        """Schickt ein Yiff-Foto."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT endtime FROM vote WHERE userid = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None or result is False:
            embed = discord.Embed(title="❌ Zugriff verweigert", description="Um diesen Command zu nutzen, musst du voten.\nVote hier: https://top.gg/bot/925799559576322078/vote", color=discord.Color.green(), url="https://top.gg/bot/925799559576322078/vote")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            mydb.close()
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/yiff/random/.json') as r:
                res = await r.json()

                image = res[0]['data']['children'][0]['data']['url']
                permalink = res[0]['data']['children'][0]['data']['permalink']
                url = f'https://reddit.com{permalink}'
                title = res[0]['data']['children'][0]['data']['title']
                ups = res[0]['data']['children'][0]['data']['ups']
                comments = res[0]['data']['children'][0]['data']['num_comments']

                embed = discord.Embed(colour=discord.Colour.blue(), title=title, url=url)
                embed.set_image(url=image)
                embed.set_footer(text=f"🔺 {ups} | 💬 {comments} ")
                await ctx.send(embed=embed, content=None)

    @commands.command(aliases=["asia"])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def asian(self, ctx):
        """Schickt ein Asian-Porn-Foto."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT endtime FROM vote WHERE userid = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None or result is False:
            embed = discord.Embed(title="❌ Zugriff verweigert", description="Um diesen Command zu nutzen, musst du voten.\nVote hier: https://top.gg/bot/925799559576322078/vote", color=discord.Color.green(), url="https://top.gg/bot/925799559576322078/vote")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            mydb.close()
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/asianporn/random/.json') as r:
                res = await r.json()

                image = res[0]['data']['children'][0]['data']['url']
                permalink = res[0]['data']['children'][0]['data']['permalink']
                url = f'https://reddit.com{permalink}'
                title = res[0]['data']['children'][0]['data']['title']
                ups = res[0]['data']['children'][0]['data']['ups']
                comments = res[0]['data']['children'][0]['data']['num_comments']

                embed = discord.Embed(colour=discord.Colour.blue(), title=title, url=url)
                embed.set_image(url=image)
                embed.set_footer(text=f"🔺 {ups} | 💬 {comments} ")
                await ctx.send(embed=embed, content=None)

    @commands.command(aliases=["bds"])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bdsm(self, ctx):
        """Schickt ein Bdsm-Porn-Foto."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
    )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT endtime FROM vote WHERE userid = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None or result is False:
            embed = discord.Embed(title="❌ Zugriff verweigert", description="Um diesen Command zu nutzen, musst du voten.\nVote hier: https://top.gg/bot/925799559576322078/vote", color=discord.Color.green(), url="https://top.gg/bot/925799559576322078/vote")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            mydb.close()
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/bdsm/random/.json') as r:
                res = await r.json()

                image = res[0]['data']['children'][0]['data']['url']
                permalink = res[0]['data']['children'][0]['data']['permalink']
                url = f'https://reddit.com{permalink}'
                title = res[0]['data']['children'][0]['data']['title']
                ups = res[0]['data']['children'][0]['data']['ups']
                comments = res[0]['data']['children'][0]['data']['num_comments']

                embed = discord.Embed(colour=discord.Colour.blue(), title=title, url=url)
                embed.set_image(url=image)
                embed.set_footer(text=f"🔺 {ups} | 💬 {comments} ")
                await ctx.send(embed=embed, content=None)
    
    @commands.command(aliases=["anl"])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def anal(self, ctx):
        """Schickt ein Anal-Porn-Foto."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT endtime FROM vote WHERE userid = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None or result is False:
            embed = discord.Embed(title="❌ Zugriff verweigert", description="Um diesen Command zu nutzen, musst du voten.\nVote hier: https://top.gg/bot/925799559576322078/vote", color=discord.Color.green(), url="https://top.gg/bot/925799559576322078/vote")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            mydb.close()
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/anal/random/.json') as r:
                res = await r.json()

                image = res[0]['data']['children'][0]['data']['url']
                permalink = res[0]['data']['children'][0]['data']['permalink']
                url = f'https://reddit.com{permalink}'
                title = res[0]['data']['children'][0]['data']['title']
                ups = res[0]['data']['children'][0]['data']['ups']
                comments = res[0]['data']['children'][0]['data']['num_comments']

                embed = discord.Embed(colour=discord.Colour.blue(), title=title, url=url)
                embed.set_image(url=image)
                embed.set_footer(text=f"🔺 {ups} | 💬 {comments} ")
                await ctx.send(embed=embed, content=None)

    @commands.command(aliases=["blowie"])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blowjob(self, ctx):
        """Schickt ein Blowjob-Porn-Foto."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT endtime FROM vote WHERE userid = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None or result is False:
            embed = discord.Embed(title="❌ Zugriff verweigert", description="Um diesen Command zu nutzen, musst du voten.\nVote hier: https://top.gg/bot/925799559576322078/vote", color=discord.Color.green(), url="https://top.gg/bot/925799559576322078/vote")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            mydb.close()
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/oralsex/random/.json') as r:
                res = await r.json()

                image = res[0]['data']['children'][0]['data']['url']
                permalink = res[0]['data']['children'][0]['data']['permalink']
                url = f'https://reddit.com{permalink}'
                title = res[0]['data']['children'][0]['data']['title']
                ups = res[0]['data']['children'][0]['data']['ups']
                comments = res[0]['data']['children'][0]['data']['num_comments']

                embed = discord.Embed(colour=discord.Colour.blue(), title=title, url=url)
                embed.set_image(url=image)
                embed.set_footer(text=f"🔺 {ups} | 💬 {comments} ")
                await ctx.send(embed=embed, content=None)

    @commands.command(aliases=["lesb"])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lesbian(self, ctx):
        """Schickt ein Lesbian-Porn-Foto."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT endtime FROM vote WHERE userid = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None or result is False:
            embed = discord.Embed(title="❌ Zugriff verweigert", description="Um diesen Command zu nutzen, musst du voten.\nVote hier: https://top.gg/bot/925799559576322078/vote", color=discord.Color.green(), url="https://top.gg/bot/925799559576322078/vote")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            mydb.close()
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/lesbianporn/random/.json') as r:
                res = await r.json()

                image = res[0]['data']['children'][0]['data']['url']
                permalink = res[0]['data']['children'][0]['data']['permalink']
                url = f'https://reddit.com{permalink}'
                title = res[0]['data']['children'][0]['data']['title']
                ups = res[0]['data']['children'][0]['data']['ups']
                comments = res[0]['data']['children'][0]['data']['num_comments']

                embed = discord.Embed(colour=discord.Colour.blue(), title=title, url=url)
                embed.set_image(url=image)
                embed.set_footer(text=f"🔺 {ups} | 💬 {comments} ")
                await ctx.send(embed=embed, content=None)

    @commands.command(aliases=["mlf"])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def milf(self, ctx):
        """Schickt ein Milf-Porn-Foto."""
        mydb = mysql.connector.connect(
            host="54.37.204.19",
            user="u60388_adFMo8yi8w",
            password="dNPaL8=W2qapSVrwv=Q9Me8I",
            database="s60388_Vulpo"
        )
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f"SELECT endtime FROM vote WHERE userid = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None or result is False:
            embed = discord.Embed(title="❌ Zugriff verweigert", description="Um diesen Command zu nutzen, musst du voten.\nVote hier: https://top.gg/bot/925799559576322078/vote", color=discord.Color.green(), url="https://top.gg/bot/925799559576322078/vote")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            mydb.close()
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/milf/random/.json') as r:
                res = await r.json()

                image = res[0]['data']['children'][0]['data']['url']
                permalink = res[0]['data']['children'][0]['data']['permalink']
                url = f'https://reddit.com{permalink}'
                title = res[0]['data']['children'][0]['data']['title']
                ups = res[0]['data']['children'][0]['data']['ups']
                comments = res[0]['data']['children'][0]['data']['num_comments']

                embed = discord.Embed(colour=discord.Colour.blue(), title=title, url=url)
                embed.set_image(url=image)
                embed.set_footer(text=f"🔺 {ups} | 💬 {comments} ")
                await ctx.send(embed=embed, content=None)
async def setup(bot):
    await bot.add_cog(Nsfw(bot))