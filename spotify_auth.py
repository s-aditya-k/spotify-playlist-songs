# this file isnt really meant to be called directly, bc it just auths with spotify
import re
import webbrowser
import requests as rq

redirect_uri = "http://localhost:8888/callback" 
client_id = "" # fill in
client_secret = "" #fill in
spotiuri = "https://accounts.spotify.com"


def get_code():
    # probably don't need all of them, just threw all of them in here cause i had issues and was lazy
    auth_scope = "ugc-image-upload user-modify-playback-state user-read-playback-state user-read-currently-playing user-follow-modify user-follow-read user-read-recently-played user-read-playback-position user-top-read playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private app-remote-control streaming user-read-email user-read-private user-library-modify user-library-read"
    auth_params = {
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "response_type": "code",
        "scope": auth_scope,
    }
    initial_auth = rq.get(spotiuri + "/authorize", params=auth_params)
    print("go to following link: ")
    print(initial_auth.url)
    webbrowser.open_new_tab(initial_auth.url)

    code = input("give callback after auth (http://localhost ...) :        ")
    code = re.sub(redirect_uri + "\?code=", "", code)

    token_params = {
        "grant_type": 'authorization_code',
        "code": code,
        "redirect_uri": redirect_uri
    }
    get_token = rq.post(
        spotiuri + "/api/token",
        params=token_params,
        auth=(client_id, client_secret),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    code = get_token.json()["access_token"]
    print("final access code is: \n" + code)
    return code
