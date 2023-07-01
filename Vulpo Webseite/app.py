import os
from flask import Flask, redirect, request, render_template, session
from requests_oauthlib import OAuth2Session
from credentials import client_id, client_secret, base_discord_api_url, authorize_url, token_url, redirect_uri, scope
import aiomysql
import asyncio
import paypalrestsdk
from datetime import datetime, timedelta
import discord
import requests
import math

VERIFY_URL_PROD = 'https://ipnpb.paypal.com/cgi-bin/webscr'
VERIFY_URL_TEST = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'
VERIFY_URL = VERIFY_URL_PROD

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
            await cursor.execute("SELECT bank FROM economy WHERE userID = (%s)", (userid))
            result = await cursor.fetchone()
            await cursor.execute("UPDATE economy SET bank = (%s) WHERE userID = (%s)", (int(result[0]) + 100000, userid))

async def create_pool(loop):
    pool = await aiomysql.create_pool(
        host='157.90.72.7',
        user='databaseAdmin',
        password='OkUyBflP3l3i8ax$*A4',
        db='VulpoDB',
        autocommit=True,
        port=3306,
        loop=loop,
        maxsize=25
    )
    return pool

async def checkpremium(response, p):
    async with p.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT status FROM premium WHERE userID = (%s)", (response.json()["id"]))
            status = await cursor.fetchone()
            if status == None:
                return False
            if status[0] == 0:
                return False
            return True
        
# async def insert_join_roles(type, guildid, roles, p):
#     async with p.acquire() as conn:
#         async with conn.cursor() as cursor:
#             if type == "Member":
#                 await cursor.execute("DELETE FROM joinroles WHERE guild_id = (%s)", (guildid))
#                 for role in roles:
#                     await cursor.execute("INSERT INTO joinroles(guild_id, role_id) VALUES(%s, %s)", (guildid, role))
#             if type == "Bot":
#                 await cursor.execute("DELETE FROM botroles WHERE guild_id = (%s)", (guildid))
#                 for role in roles:
#                     await cursor.execute("INSERT INTO botroles(guild_id, role_id) VALUES(%s, %s)", (guildid, role))

# async def insert_starboard(guildid, channel, p):
#     async with p.acquire() as conn:
#         async with conn.cursor() as cursor:
#             await cursor.execute("DELETE FROM starboard WHERE guildID = (%s)", (guildid))
#             await cursor.execute("INSERT INTO starboard(guildID, channelID) VALUES(%s, %s)", (guildid, channel))

# async def delete_starboard(guildid, p):
#     async with p.acquire() as conn:
#         async with conn.cursor() as cursor:
#             await cursor.execute("DELETE FROM starboard WHERE guildID = (%s)", (guildid))

async def remove_premium(userID, p):
    async with p.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM premium WHERE userID = (%s)", (userID))

async def asyncio_task(userID, when: datetime, p):
    await discord.utils.sleep_until(when=when)
    await remove_premium(userID, p)

async def new_payment(first_name, last_name, payer_email, payer_id, txn_id, userID, item_name, p):
    async with p.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("INSERT INTO zahlungen(first_name, last_name, payer_email, payer_id, txn_id, userID, item_name) VALUES(%s, %s, %s, %s, %s, %s, %s)", (first_name, last_name, payer_email, payer_id, txn_id, userID, item_name))
            await cursor.execute("SELECT endtime FROM premium WHERE userID = (%s)", (userID))
            endtime = await cursor.fetchone()
            if endtime is not None:
                alte_endzeit_timestamp = int(endtime[0])
                neue_endzeit_timestamp = alte_endzeit_timestamp  # Setze den initialen Wert auf alte_endzeit_timestamp
                if item_name == "1 Monat":
                    neue_endzeit_timestamp += 2419200
                if item_name == "3 Monate":
                    neue_endzeit_timestamp += 7862400
                if item_name == "6 Monate":
                    neue_endzeit_timestamp += 15724800
                if item_name == "12 Monate":
                    neue_endzeit_timestamp += 31449600
                
                neue_endzeit_datetime = datetime.fromtimestamp(neue_endzeit_timestamp)
                await cursor.execute("UPDATE premium SET endtime = (%s) WHERE userID = (%s)", (neue_endzeit_timestamp, userID))
                
                # Vorhandene Task mit dem Namen userID suchen und um x Monate verlängern
                existing_task = asyncio.all_tasks()
                for task in existing_task:
                    if str(task.get_name()) == str(userID):
                        task.cancel()
                        break
                
                asyncio.create_task(asyncio_task(userID, neue_endzeit_datetime, p), name=f"{userID}")
            else:
                alte_endzeit_timestamp = math.floor(datetime.now().timestamp())
                neue_endzeit_timestamp = alte_endzeit_timestamp
                if item_name == "1 Monat":
                    neue_endzeit_timestamp += 2419200
                if item_name == "3 Monate":
                    neue_endzeit_timestamp += 7862400
                if item_name == "6 Monate":
                    neue_endzeit_timestamp += 15724800
                if item_name == "12 Monate":
                    neue_endzeit_timestamp += 31449600
                
                neue_endzeit_datetime = datetime.fromtimestamp(neue_endzeit_timestamp)
                await cursor.execute("INSERT INTO premium(endtime, userID, status) VALUES(%s, %s, %s)", (neue_endzeit_timestamp, userID, 1))
                await addcookies(userID, p)
                asyncio.create_task(asyncio_task(userID, neue_endzeit_datetime, p), name=f"{userID}")

async def start_all_tasks(p):
    async with p.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT endtime, userID FROM premium")
            result = await cursor.fetchall()
            if result != [] or result != () or result != []:
                for endtime in result:
                    neue_endzeit_datetime = datetime.fromtimestamp(endtime[0])
                    asyncio.create_task(asyncio_task(endtime[1], neue_endzeit_datetime, p), name=f"{endtime[1]}")

#—————————————————————————————————————————————#
#Flask Webserver App erstellen.
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PAYPAL_MODE'] = 'live'
app.config['PAYPAL_CLIENT_ID'] = 'AdNZxDHdmW7iJebIw1XY-YuwXHhI5VN7sGeuL-GfgSekyNw93QzQnsCin5A6BjWzE_SGOog1AnH-Id1t'
app.config['PAYPAL_CLIENT_SECRET'] = 'EATcxSp0L9b6-W7QyuoOE7pYzbmI3RkFstVuDG1_B4imPa2qRLhHEC6bezP-2rck9FSmmM-ZgYUES_Bx'

aiomysql_loop = asyncio.new_event_loop()
asyncio.set_event_loop(aiomysql_loop)
pool = aiomysql_loop.run_until_complete(create_pool(aiomysql_loop))

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

# @app.route('/process', methods=['POST'])
# def process():
#     data = request.json
#     if data['kennung'] == 'Member':
#         task = loop.create_task(insert_join_roles("Member", data['guild_id'], data['selected_roles'], pool))
#         loop.run_until_complete(task)
#         return "OK"
#     if data['kennung'] == 'Bot':
#         task = loop.create_task(insert_join_roles("Bot", data['guild_id'], data['selected_roles'], pool))
#         loop.run_until_complete(task)
#         return "OK"
#     if data['kennung'] == 'Starboard':
#         task = loop.create_task(insert_starboard(data['guild_id'], data['channel_id'], pool))
#         loop.run_until_complete(task)
#         return "OK"
    
# @app.route('/delete', methods=['POST'])
# def delete():
#     data = request.json
#     if data['kennung'] == 'Starboard':
#         task = loop.create_task(delete_starboard(data['guild_id'], pool))
#         loop.run_until_complete(task)
#         return "OK"

@app.route('/paypal/ipn', methods=['POST'])
def paypal_ipn():
    # Sending message as-is with the notify-validate request
    params = request.form.to_dict()
    params['cmd'] = '_notify-validate'
    headers = {'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Vulpo-IPN'}
    response = requests.post(VERIFY_URL, params=params, headers=headers, verify=True)
    response.raise_for_status()

    # See if PayPal confirms the validity of the IPN received
    userID = params['custom']
    first_name = params['first_name']
    last_name = params['last_name']
    payer_email = params['payer_email']
    payer_id = params['payer_id']
    txn_id = params['txn_id']
    item_name = params['option_selection1']
    aiomysql_loop.run_until_complete(new_payment(first_name, last_name, payer_email, payer_id, txn_id, userID, item_name, pool))
    return "OK", 200

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

#—————————————————————————————————————————————#
#Backend, das abläuft, wenn bestimmte Routen eingegeben werden.
#Beispiel: vulpo-bot.de/login leitet zum Discord Login weiter.

@app.route("/login")
def login():
    try:
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
        login_url, state = oauth.authorization_url(authorize_url)

        session["state"] = f"{state}"
        return redirect(f"{login_url}")
    except:
        session.clear()
        return redirect("/logout")
    
@app.route("/oauth_callback")
def oauth_callback():
    try:
        discord = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
        url = request.url
        https_url = str(url).replace("http","https")
        token = discord.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=https_url,
        )
        session['discord_token'] = token
        discord1 = OAuth2Session(client_id, token=session['discord_token'])
        response = discord1.get(base_discord_api_url + '/users/@me')
        return render_template('nopremium.html', response=response.json())
    except Exception as e:
        session.clear()
        return redirect("/logout")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
#—————————————————————————————————————————————#
# Starten des Webservers.
if __name__ == "__main__":
    asyncio.run(start_all_tasks(pool))
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(host="0.0.0.0")