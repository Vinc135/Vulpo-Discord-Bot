import os
from flask import Flask, redirect, request, render_template, session, jsonify
from requests_oauthlib import OAuth2Session
from credentials import client_id, client_secret, base_discord_api_url, authorize_url, token_url, redirect_uri, scope
import aiomysql
import asyncio
from datetime import datetime
import requests
import math
VERIFY_URL_PROD = 'https://ipnpb.paypal.com/cgi-bin/webscr'
VERIFY_URL_TEST = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'
VERIFY_URL = VERIFY_URL_PROD
baseURL = {
    'sandbox': 'https://api-m.sandbox.paypal.com',
    'production': 'https://api-m.paypal.com'
}
urls = ['https://api-m.sandbox.pypal.com','https://api-m.paypal.com']





# use the orders api to capture payment


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
                
                await cursor.execute("UPDATE premium SET endtime = (%s) WHERE userID = (%s)", (neue_endzeit_timestamp, userID))
                
                # Vorhandene Task mit dem Namen userID suchen und um x Monate verlängern
                existing_task = asyncio.all_tasks()
                for task in existing_task:
                    if str(task.get_name()) == str(userID):
                        task.cancel()
                        break
                
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
                
                await cursor.execute("INSERT INTO premium(endtime, userID, status) VALUES(%s, %s, %s)", (neue_endzeit_timestamp, userID, 1))
                await addcookies(userID, p)

from datetime import datetime
import base64

async def get_all_tickets(p, id):
    async with p.acquire() as conn:
        async with conn.cursor() as cursor:
            team = [897641092697186336, 981898944017739836, 976156443675873361, 824378909985341451]
            if int(id) not in team:
                await cursor.execute("SELECT autorname, autorID, ticketID, titel, status, letztes_update FROM w_tickets WHERE autorID = (%s)", (id))
                rows = await cursor.fetchall()

                tickets_dict = {}
                for row in rows:
                    autorname, autorID, ticketID, titel, status, letztes_update = row
                    tickets_dict[ticketID] = {'autorname': autorname, 'autorID': autorID, 'ticketID': ticketID, 'titel': titel, 'status': status, "team": "nein", "letztes_update": letztes_update}

                sorted_tickets = dict(sorted(tickets_dict.items(), key=lambda x: sort_key_function(x[1]), reverse=True))
                return sorted_tickets
            else:
                await cursor.execute("SELECT autorname, autorID, ticketID, titel, status, letztes_update FROM w_tickets")
                rows = await cursor.fetchall()

                tickets_dict = {}
                for row in rows:
                    autorname, autorID, ticketID, titel, status, letztes_update = row
                    tickets_dict[ticketID] = {'autorname': autorname, 'autorID': autorID, 'ticketID': ticketID, 'titel': titel, 'status': status, "team": "ja", "letztes_update": letztes_update}

                sorted_tickets = dict(sorted(tickets_dict.items(), key=lambda x: sort_key_function(x[1]), reverse=True))
                return sorted_tickets

def sort_key_function(ticket):
    # Erst nach Status, dann nach Zeit sortieren
    if ticket["status"] != "Geschlossen":
        return (1, datetime.strptime(ticket["letztes_update"], "%d.%m.%Y %H:%M:%S"))
    else:
        return (0, datetime.strptime(ticket["letztes_update"], "%d.%m.%Y %H:%M:%S"))


async def new_ticket(p, autorID, autorname, titel):
    async with p.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM w_tickets WHERE autorID = (%s) AND titel = (%s)", (autorID, titel))
            result = await cursor.fetchone()
            if result != None:
                return

            await cursor.execute("SELECT MAX(ticketID) FROM w_tickets")
            row = await cursor.fetchone()
            if row and row[0] is not None:
                max_ticketID = row[0]
            else:
                max_ticketID = 0
            
            ticketid = max_ticketID + 1


            now = datetime.now()
            time_format = "%d.%m.%Y %H:%M:%S"
            time_string = now.strftime(time_format)

            await cursor.execute("INSERT INTO w_tickets(autorID, ticketID, titel, status, autorname, letztes_update) VALUES(%s, %s, %s, %s, %s, %s)", (autorID, ticketid, titel, "Offen", autorname, time_string))
            return ticketid
        
async def open_ticket(p, ticketID):
    async with p.acquire() as conn:
        async with conn.cursor() as cursor:
            # Datenbankabfrage, um alle Nachrichten für eine bestimmte ticketID zu erhalten
            query = "SELECT autorID, zeit, autorname, nachricht FROM w_ticketmsg WHERE ticketID = %s"
            await cursor.execute(query, (ticketID,))
            rows = await cursor.fetchall()

            # Dictionary zum Speichern der Nachrichten nach Zeit
            messages_dict = {}

            for row in rows:
                autorID, zeit_str, autorname, nachricht = row
                zeit = datetime.strptime(zeit_str, "%d.%m.%Y %H:%M:%S")

                team = [897641092697186336, 981898944017739836, 976156443675873361, 824378909985341451]
                if int(autorID) not in team:
                    messages_dict[zeit] = {
                        "autorID": autorID,
                        "zeit": zeit_str,
                        "autorname": autorname,
                        "nachricht": nachricht,
                        "team": "nein"
                    }
                else:
                    messages_dict[zeit] = {
                        "autorID": autorID,
                        "zeit": zeit_str,
                        "autorname": autorname,
                        "nachricht": nachricht,
                        "team": "ja"
                    }

            # Dictionary nach Zeit sortieren und das sortierte Dictionary zurückgeben
            sorted_messages = dict(sorted(messages_dict.items(), reverse=True))
            return sorted_messages

async def send_message(p, ticketID, message, autorID, autorname, status):
    async with p.acquire() as conn:
        async with conn.cursor() as cursor:
            query = "SELECT autorID, zeit, autorname, nachricht FROM w_ticketmsg WHERE ticketID = %s AND nachricht = %s"
            await cursor.execute(query, (ticketID, message,))
            result = await cursor.fetchone()
            if result != None:
                return

            now = datetime.now()
            time_format = "%d.%m.%Y %H:%M:%S"
            time_string = now.strftime(time_format)
            await cursor.execute("INSERT INTO w_ticketmsg(autorID, ticketID, zeit, autorname, nachricht) VALUES(%s, %s, %s, %s, %s)", (autorID, ticketID, time_string, autorname, message))
            await cursor.execute("UPDATE w_tickets SET status = (%s) WHERE ticketID = (%s)", (status, ticketID))

async def close_ticket(p, ticketID):
    async with p.acquire() as conn:
        async with conn.cursor() as cursor:
            query = "SELECT * FROM w_tickets WHERE ticketID = %s AND status != %s"
            await cursor.execute(query, (ticketID, "Geschlossen"))
            result = await cursor.fetchone()
            if result != None:
                await cursor.execute("UPDATE w_tickets SET status = (%s) WHERE ticketID = (%s)", ("Geschlossen", ticketID))

async def alle_ohne_premium_jemals(p):
    async with p.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT userID FROM zahlungen")
            result = await cursor.fetchall()
            liste = []
            for r in result:
                if int(r[0]) not in liste:
                    liste.append(int(r[0]))

            return liste

#—————————————————————————————————————————————#
#Flask Webserver App erstellen.
app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PAYPAL_MODE'] = 'live'


CLIENT_ID = 'AdNZxDHdmW7iJebIw1XY-YuwXHhI5VN7sGeuL-GfgSekyNw93QzQnsCin5A6BjWzE_SGOog1AnH-Id1t'
APP_SECRET = 'EATcxSp0L9b6-W7QyuoOE7pYzbmI3RkFstVuDG1_B4imPa2qRLhHEC6bezP-2rck9FSmmM-ZgYUES_Bx'

aiomysql_loop = asyncio.new_event_loop()
asyncio.set_event_loop(aiomysql_loop)
pool = aiomysql_loop.run_until_complete(create_pool(aiomysql_loop))

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

@app.route("/ticketsystem", methods=["POST"])
def ticketsystem():
    """Umleitung zur Ticketsystem Seite."""
    try:
        id = request.form.get('id', '')
        username = request.form.get('username', '')
        avatar = request.form.get('avatar', '')
        if id and username and avatar:
            task = aiomysql_loop.create_task(get_all_tickets(pool, id))
            all_tickets = aiomysql_loop.run_until_complete(task) or None
            return render_template('tickets.html', id=id, username=username, avatar=avatar, all_tickets=all_tickets)
        else:
            return redirect("/logout")
        
    except Exception as e:
        return redirect("/logout")
    
@app.route("/premiumkauf", methods=["POST"])
def premiumkauf():
    """Umleitung zur Premiumkauf Seite."""
    try:
        id = request.form.get('id', '')
        username = request.form.get('username', '')
        avatar = request.form.get('avatar', '')
        if id and username and avatar:
            task = aiomysql_loop.create_task(alle_ohne_premium_jemals(pool))
            liste = aiomysql_loop.run_until_complete(task)
            if int(id) == 824378909985341451:
                return render_template('lol.html', id=id, username=username, avatar=avatar)
            if int(id) in liste:
                return render_template('nopremium.html', id=id, username=username, avatar=avatar)
            if int(id) not in liste:
                return render_template('nopremium_rabatte.html', id=id, username=username, avatar=avatar)
        else:
            return redirect("/logout")
        
    except Exception as e:
        return redirect("/logout")
    
@app.route("/new_ticket", methods=["POST"])
def new_tickt():
    """Umleitung zur Ticket Seite."""
    try:
        autorID = request.form.get('autorID', '')
        autorname = request.form.get('autorname', '')
        titel = request.form.get('titel', '')
        avatar = request.form.get('avatar', '')
        if autorID and autorname and titel and avatar:
            task = aiomysql_loop.create_task(new_ticket(pool, autorID, autorname, titel))
            ticketID = aiomysql_loop.run_until_complete(task)
            return render_template('ticket.html', id=autorID, username=autorname, avatar=avatar, thema=titel, ticketID=ticketID)
        else:
            return redirect("/logout")
        
    except Exception as e:
        return redirect("/logout")
    
@app.route("/open_ticket", methods=["POST"])
def open_tickt():
    """Umleitung zur Ticket Seite."""
    try:
        id = request.form.get('userID', '')
        username = request.form.get('username', '')
        thema = request.form.get('thema', '')
        ticketID = request.form.get('ticketID', '')
        avatar = request.form.get('avatar', '')
        status = request.form.get('status', '')
        if id and username and thema:
            task = aiomysql_loop.create_task(open_ticket(pool, ticketID))
            messages = aiomysql_loop.run_until_complete(task)
            return render_template('ticket.html', id=id, username=username, ticketID=ticketID, thema=thema, messages=messages, avatar=avatar, status=status)
        else:
            return redirect("/logout")
        
    except Exception as e:
        return redirect("/logout")

@app.route("/send_message", methods=["POST"])
def send_msg():
    """Umleitung zur Ticket Seite."""
    try:
        id = request.form.get('userID', '')
        username = request.form.get('username', '')
        thema = request.form.get('thema', '')
        ticketID = request.form.get('ticketID', '')
        avatar = request.form.get('avatar', '')
        message = request.form.get('message', '')
        status = request.form.get('status', '')
        if id and username and thema:
            task1 = aiomysql_loop.create_task(send_message(pool, ticketID, message, id, username, status))
            aiomysql_loop.run_until_complete(task1)

            task = aiomysql_loop.create_task(open_ticket(pool, ticketID))
            messages = aiomysql_loop.run_until_complete(task)
            return render_template('ticket.html', id=id, username=username, ticketID=ticketID, thema=thema, messages=messages, avatar=avatar)
        else:
            return redirect("/logout")
        
    except Exception as e:
        return redirect("/logout")

@app.route('/close_ticket', methods=['POST'])
def close_tickt():
    ticketID = request.form.get('ticketID', '')
    id = request.form.get('id', '')
    username = request.form.get('username', '')
    avatar = request.form.get('avatar', '')
    if id and username and avatar and ticketID:
        task1 = aiomysql_loop.create_task(close_ticket(pool, ticketID))
        aiomysql_loop.run_until_complete(task1)

        task = aiomysql_loop.create_task(get_all_tickets(pool, id))
        all_tickets = aiomysql_loop.run_until_complete(task) or None
        return render_template('tickets.html', id=id, username=username, avatar=avatar, all_tickets=all_tickets)

@app.route("/create-paypal-order",methods=['POST'])
def create_paypal_order():
    order = create_order()

    return jsonify(order)

@app.route('/capture-paypal-order',methods=['POST'])
def capture_paypal_order():
    data =  request.get_json()
    order_id = data.get('orderID')

    capture_data = capturePayment(order_id)

    return jsonify(capture_data)

def generateAccessToken():
    auth = base64.b64encode(f'{CLIENT_ID}:{APP_SECRET}')
    url = f'{urls[0]}/v1/oauth2/token'
    send = 'grant_type=client_credentials'
    headers = {"Authorization": f'Basic {auth}'}

    r = requests.post(url,headers=headers,data=send)

    if r.status_code == 200:
        data = r.json()

        return data['access_token']
    else:
        return 'error'
    
async def create_order():
    access_token = await generateAccessToken()

    if access_token != 'error':
        url = f'{urls[0]}/v2/checkout/orders'
        json = {'intent': 'CAPTURE','purchase_units': [{'amount': {'currency_code': "EUR",'value':'10.00'}}]}
        headers = {'Content-Type': 'application/json','Authorization': f'Bearer {access_token}'}

        r = requests.post(url,headers=headers,data=str(json))

        if r.status_code == 200:
            return r.json()
        else:
            return 'error'
    else:
        return 'error'
    
async def capturePayment(orderId):
    access_token = await generateAccessToken()

    if access_token != 'error':
        url = f'{urls[0]}/v2/checkout/orders/{orderId}/capture'
        headers = {'Content-Type': 'application/json','Authorization': f'Bearer {access_token}'}

        r = requests.post(url,headers=headers)

        if r.status_code == 200:
            return r.json()
        else:
            return 'error'
    else:
        return 'error'



@app.errorhandler(404)
def page_not_found(error):
    """Diese Seite kommt, wenn eine Seite nicht gefunden wird."""
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    return redirect("https://vulpo-bot.de/login", code=307)



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
        return render_template('choose_after_login.html', response=response.json())
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
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(host='0.0.0.0', port=5000)