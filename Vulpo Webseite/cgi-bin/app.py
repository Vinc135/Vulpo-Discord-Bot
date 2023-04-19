import os
from flask import Flask, redirect, request, render_template, session
from requests_oauthlib import OAuth2Session
from credentials import client_id, client_secret, base_discord_api_url, authorize_url, token_url, redirect_uri, scope
import requests
import aiomysql
import asyncio

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

loop = asyncio.get_event_loop()
pool = loop.run_until_complete(create_pool(loop))

#—————————————————————————————————————————————#
#Flask Webserver App erstellen.
app = Flask(__name__)
app.secret_key = os.urandom(24)

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

# @app.route('/premium')
# def premium():
#     """Umleitung zur Premium Seite."""
#     return render_template('premium.html')

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

@app.route('/authorizehallotest', methods=['POST'])
def server():
    return render_template('server.html')

#—————————————————————————————————————————————#
#Backend, das abläuft, wenn bestimmte Routen eingegeben werden.
#Beispiel: vulpo-bot.de/login leitet zum Discord Login weiter.

@app.route("/login")
def login():
    try:
        discord_authorization = OAuth2Session(client_id, token=session['discord_token'])
        discord_authorization.get(base_discord_api_url + '/users/@me')
        return redirect("/")
    except:
        pass

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
        task = loop.create_task(checkpremium(response, pool))
        premium_status = loop.run_until_complete(task)
        if premium_status == False:
            return render_template('nopremium.html', response=response.json())
        
        # Zugriff auf die verbundenen Server des Benutzers
        guilds = []
        guilds_response = discord1.get(base_discord_api_url + '/users/@me/guilds')
        for guild in guilds_response.json():
            if int(guild["permissions"]) & 0x00000008:
                headers = {
                    'Authorization': 'Bot OTI1Nzk5NTU5NTc2MzIyMDc4.GyWCpe.S8URCDJm8wlKVztJRYf_Njjy8NsfUU7iIK5nXk',
                }

                members_response = requests.get(base_discord_api_url + f'/guilds/{guild["id"]}/members/925799559576322078', headers=headers)
                if "Unknown Guild" in str(members_response.json()):
                    continue
                else:
                    guilds.append(guild)

        return render_template('dashboard.html', guilds=guilds, response=response.json())

    except:
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