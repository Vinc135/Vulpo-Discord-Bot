import json
import os
from flask import Flask, redirect, request, render_template, session
from requests_oauthlib import OAuth2Session
from credentials import client_id, client_secret, base_discord_api_url, authorize_url, token_url, redirect_uri, scope
import requests
import aiomysql
import asyncio
from flask_session import Session
import paypalrestsdk

async def open_acc(userid, p):
    async with p.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT rucksack, bank, job, stunden FROM economy WHERE userID = (%s)", (userid))
            result = await cursor.fetchone()
            if result is None:
                await cursor.execute("INSERT INTO economy(rucksack, bank, job, stunden, userID) VALUES(%s, %s, %s, %s, %s)",("0", "0", "Kein Job", "0", userid))
                
                liste = ["0","0","Kein Job","0",userid]
                return liste
            else:
                return result
            
async def addcookies(userid, p):
    await open_acc(userid, p)
    async with p.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT stunden FROM economy WHERE userID = (%s)", (userid))
            result = await cursor.fetchone()
            await cursor.execute("UPDATE economy SET stunden = (%s) WHERE userID = (%s)", (int(result[0]) + 1, userid))

async def create_pool(loop):
    pool = await aiomysql.create_pool(
        host='142.132.233.69',
        user='u64287_IF3HQ8wHRH',
        password='3oKMMVfuEqv^Xcvf@i!3bzw^',
        db='s64287_VulpoDB',
        autocommit=True,
        port=3306,
        loop=loop,
        maxsize=25
    )
    return pool

async def checkpremium(response, p):
    async with p.get() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT status FROM premium WHERE userID = (%s)", (response.json()["id"]))
            status = await cursor.fetchone()
            if status == None:
                return False
            if status[0] == 0:
                return False
            return True
        
async def insert_join_roles(type, guildid, roles, p):
    async with p.get() as conn:
        async with conn.cursor() as cursor:
            if type == "Member":
                await cursor.execute("DELETE FROM joinroles WHERE guild_id = (%s)", (guildid))
                for role in roles:
                    await cursor.execute("INSERT INTO joinroles(guild_id, role_id) VALUES(%s, %s)", (guildid, role))
            if type == "Bot":
                await cursor.execute("DELETE FROM botroles WHERE guild_id = (%s)", (guildid))
                for role in roles:
                    await cursor.execute("INSERT INTO botroles(guild_id, role_id) VALUES(%s, %s)", (guildid, role))

async def insert_starboard(guildid, channel, p):
    async with p.get() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM starboard WHERE guildID = (%s)", (guildid))
            await cursor.execute("INSERT INTO starboard(guildID, channelID) VALUES(%s, %s)", (guildid, channel))

async def delete_starboard(guildid, p):
    async with p.get() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM starboard WHERE guildID = (%s)", (guildid))
        
async def add_premium(orderID, subscriptionID, userID, p):
    async with p.get() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("INSERT INTO premium(orderID ,subscriptionID, userID, status) VALUES(%s, %s, %s, %s)", (orderID, subscriptionID, userID, 1))
            await addcookies(userID, p)
    
loop = asyncio.get_event_loop()
pool = loop.run_until_complete(create_pool(loop))

#—————————————————————————————————————————————#
#Flask Webserver App erstellen.
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PAYPAL_MODE'] = 'live'
app.config['PAYPAL_CLIENT_ID'] = 'AdNZxDHdmW7iJebIw1XY-YuwXHhI5VN7sGeuL-GfgSekyNw93QzQnsCin5A6BjWzE_SGOog1AnH-Id1t'
app.config['PAYPAL_CLIENT_SECRET'] = 'EATcxSp0L9b6-W7QyuoOE7pYzbmI3RkFstVuDG1_B4imPa2qRLhHEC6bezP-2rck9FSmmM-ZgYUES_Bx'

Session(app)

paypalrestsdk.configure({
    'mode': app.config['PAYPAL_MODE'],
    'client_id': app.config['PAYPAL_CLIENT_ID'],
    'client_secret': app.config['PAYPAL_CLIENT_SECRET']
})
#—————————————————————————————————————————————#
#Die Umleitungen zu den Pages.
#Beispiel: vulpo-bot.de/premium anstatt /premium.html
@app.route('/')
def index():
    """Umleitung zur Hauptseite."""
    return render_template('index.html')

@app.route('/support')
def support():
    """Umleitung zum Supportserver."""
    return redirect("https://discord.gg/49jD3VXksp")

@app.route('/invite')
def invite():
    """Umleitung zum Einladen."""
    return redirect("https://discord.com/oauth2/authorize?client_id=925799559576322078&permissions=8&scope=bot%20applications.commands")

@app.route('/premium')
def premium():
    """Umleitung zur Premium Seite."""
    return render_template('premium.html')

@app.route('/impressum')
def impressum():
    """Umleitung zur Impressum Seite."""
    return render_template('impressum.html')

@app.route('/datenschutz')
def datenschutz():
    """Umleitung zur Datenschutz Seite."""
    return render_template('datenschutz.html')

@app.route('/formulare')
def formulare():
    """Umleitung zur Formulare Seite."""
    return render_template('formulare.html')

@app.route('/agb')
def agb():
    """Umleitung zur AGB Seite."""
    return render_template('agb.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    if data['kennung'] == 'Member':
        task = loop.create_task(insert_join_roles("Member", data['guild_id'], data['selected_roles'], pool))
        loop.run_until_complete(task)
        return "OK"
    if data['kennung'] == 'Bot':
        task = loop.create_task(insert_join_roles("Bot", data['guild_id'], data['selected_roles'], pool))
        loop.run_until_complete(task)
        return "OK"
    if data['kennung'] == 'Starboard':
        task = loop.create_task(insert_starboard(data['guild_id'], data['channel_id'], pool))
        loop.run_until_complete(task)
        return "OK"
    
@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    if data['kennung'] == 'Starboard':
        task = loop.create_task(delete_starboard(data['guild_id'], pool))
        loop.run_until_complete(task)
        return "OK"

@app.route('/paypal/gekauft', methods=['GET', 'POST'])
def gekauft():
    try:
        data = request.json
        orderID = data['data']['orderID']
        subscriptionID = data['data']['subscriptionID']
        userID = data['userid']
        task = loop.create_task(add_premium(orderID, subscriptionID, userID, pool))
        loop.run_until_complete(task)
        render_template("index.html")
        return "OK"
    except Exception as e:
        return f"{e}\n{data}"

# @app.route('/paypal/webhooks', methods=['POST'])
# def paypal_webhook():
#     # Überprüfen, ob die Anfrage von PayPal kommt
#     auth_header = request.headers.get('Authorization')
#     if not auth_header or not auth_header.startswith('Bearer '):
#         return 'Unauthorized', 401
    
#     data = json.loads(request.data)
#     try:
#         task = loop.create_task(test(data, pool))
#         loop.run_until_complete(task)
#     except:
#         pass
#     try:
#         task = loop.create_task(get_discord_userid_from_subscriptionID(data["resource"]["id"], pool))
#         userid = loop.run_until_complete(task)
#         task = loop.create_task(cancel_premium(userid, pool))
#         loop.run_until_complete(task)
#     except Exception as e:
#         task = loop.create_task(test(f"fehler1: {e}", pool))
#         loop.run_until_complete(task)
#     return 'OK', 200

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Check if backend data is sent
    try:
        if not all(key in request.form for key in ['guild_name', 'guild_id', 'guild_icon', 'user', 'user_id', 'user_avatar']):
            return redirect("/login")
        
        guild_name = request.form.get('guild_name')
        guild_id = request.form.get('guild_id')
        guild_icon = request.form.get('guild_icon')
        user = request.form.get('user')
        user_name = request.form.get('user_name')
        user_id = request.form.get('user_id')
        user_avatar = request.form.get('user_avatar')
        kennung = request.form.get('kennung')

        if kennung == "None":
            return render_template('dashboard.html', guild_name=guild_name, guild_id=guild_id, guild_icon=guild_icon, user=user, user_id=user_id, user_avatar=user_avatar, user_name=user_name)
        if kennung == "1.1":
            try:
                headers = {
                        'Authorization': 'Bot OTI1Nzk5NTU5NTc2MzIyMDc4.GcwvXN.EkMMDxTqykR8em6L4lJqOouGfvAvH1J1rq9nJQ',
                }

                roles_response = requests.get(base_discord_api_url + f'/guilds/{guild_id}/roles', headers=headers)
                roles = []
                for role in roles_response.json():
                    roles.append(role)
                return render_template('1.1.html', guild_name=guild_name, guild_id=guild_id, guild_icon=guild_icon, user=user, user_id=user_id, user_avatar=user_avatar, user_name=user_name, roles=roles)
            except Exception as e:
                return f"fehler: {e}"
        if kennung == "1.2":
            try:
                headers = {
                        'Authorization': 'Bot OTI1Nzk5NTU5NTc2MzIyMDc4.GcwvXN.EkMMDxTqykR8em6L4lJqOouGfvAvH1J1rq9nJQ',
                }

                channels_response = requests.get(base_discord_api_url + f'/guilds/{guild_id}/channels', headers=headers)

                channels = []
                for channel in channels_response.json():
                    if channel['type'] == 0:
                        channels.append(channel)
                return render_template('1.2.html', guild_name=guild_name, guild_id=guild_id, guild_icon=guild_icon, user=user, user_id=user_id, user_avatar=user_avatar, user_name=user_name, channels=channels)
            except Exception as e:
                return f"fehler: {e}"
        if kennung == "1.3":
            return "Erfolgreich 1.3"
        if kennung == "2.1":
            return "Erfolgreich 2.1"
        if kennung == "2.2":
            return "Erfolgreich 2.2"
        if kennung == "2.3":
            return "Erfolgreich 2.3"
        if kennung == "3.1":
            return "Erfolgreich 3.1"
        if kennung == "3.2":
            return "Erfolgreich 3.2"
        if kennung == "3.3":
            return "Erfolgreich 3.3"
        if kennung == "4.1":
            return "Erfolgreich 4.1"
        if kennung == "4.2":
            return "Erfolgreich 4.2"
        if kennung == "4.3":
            return "Erfolgreich 4.3"
        if kennung == "5.1":
            return "Erfolgreich 5.1"
        if kennung == "5.2":
            return "Erfolgreich 5.2"
        if kennung == "5.3":
            return "Erfolgreich 5.3"
    except Exception as e:
        return f"fehler2: {e}\n{request.form}"
    
#—————————————————————————————————————————————#
#Backend, das abläuft, wenn bestimmte Routen eingegeben werden.
#Beispiel: vulpo-bot.de/login leitet zum Discord Login weiter.

@app.route("/login")
def login():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = oauth.authorization_url(authorize_url)

    session["state"] = f"{state}"

    return redirect(f"{login_url}")

@app.route("/oauth_callback")
def oauth_callback():
    try:
        discord = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
        token = discord.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.url,
        )
        session['discord_token'] = token
        discord1 = OAuth2Session(client_id, token=session['discord_token'])
        response = discord1.get(base_discord_api_url + '/users/@me')
        return render_template('nopremium.html', response=response.json())
        
        # Zugriff auf die verbundenen Server des Benutzers
        # guilds = []
        # guilds_response = discord1.get(base_discord_api_url + '/users/@me/guilds')
        
        # for guild in guilds_response.json():
        #     if int(guild["permissions"]) & 0x00000008:
        #         headers = {
        #             'Authorization': 'Bot OTI1Nzk5NTU5NTc2MzIyMDc4.GcwvXN.EkMMDxTqykR8em6L4lJqOouGfvAvH1J1rq9nJQ',
        #         }

        #         members_response = requests.get(base_discord_api_url + f'/guilds/{guild["id"]}/members/925799559576322078', headers=headers)
        #         if "Unknown Guild" in str(members_response.json()):
        #             continue
        #         else:
        #             guilds.append(guild)

        # return render_template('server.html', guilds=guilds, response=response.json())

    except Exception as e:
        return f"{e}"
        session.clear()
        return redirect("/logout")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
#—————————————————————————————————————————————#
#Starten des Webservers.
if __name__ == "__main__":
    app.run()