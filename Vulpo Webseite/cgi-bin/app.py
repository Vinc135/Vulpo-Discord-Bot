import os
from flask import Flask, redirect, request, render_template, session
from requests_oauthlib import OAuth2Session
from credentials import client_id, client_secret, base_discord_api_url, authorize_url, token_url, redirect_uri, scope

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

        # Zugriff auf die verbundenen Server des Benutzers
        guilds = []
        guilds_response = discord1.get(base_discord_api_url + '/users/@me/guilds')
        for guild in guilds_response.json():
            if int(guild["permissions"]) & 0x00000008:
                members_response = discord1.get(base_discord_api_url + f'/guilds/{guild["id"]}/members')
                for member in members_response.json():
                    if str(member['user']['id']) == '925799559576322078':
                        guilds.append(guild["name"])
        
        guilds.append()

        return render_template('dashboard.html', guilds=guilds, response=response.json())

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