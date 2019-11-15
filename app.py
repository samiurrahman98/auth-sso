import os
import flask
import requests_oauthlib

CLIENT_ID = os.environ.get("SIMPLE_LOGIN_APP_ID")
CLIENT_SECRET = os.environ.get("SIMPLE_LOGIN_APP_SECRET")
AUTHORIZATION_BASE_URL = "https://app.simplelogin.io/oauth2/authorize"
TOKEN_URL = "https://app.simplelogin.io/oauth2/token"
USERINFO_URL ="https://app.simplelogin.io/oauth2/userinfo"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = flask.Flask(__name__)

@app.route("/")
def index():
    return """
    <a href="/login">Login with SimpleLogin</a>
    """

@app.route("/login")
def login():
    simplelogin = requests_oauthlib.OAuth2Session(
        CLIENT_ID, redirect_uri="http://localhost:5000/callback"
    )
    authorization_url, _ = simplelogin.authorization_url(AUTHORIZATION_BASE_URL)
    return flask.redirect(authorization_url)

@app.route("/callback")
def callback():
    simplelogin = requests_oauthlib.OAuth2Session(CLIENT_ID)
    simplelogin.fetch_token(
        TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=flask.request.url
    )
    user_info = simplelogin.get(USERINFO_URL).json()
    return f"""
    USER INFORMATION: <br>
    NAME: {user_info["name"]} <br>
    EMAIL: {user_info["email"]} <br>
    AVATAR <img src="{user_info.get('avatar_url')}"> <br>
    <a href="/">Home</a>
    """

if __name__ == '__main__':
    app.run(debug=True)