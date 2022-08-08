# run this file with spotify_auth.py in the same folder
# or, just provide access token on next line and remove the #
# access_token = "(token here)"

import re
import time

import requests as rq
from requests.structures import CaseInsensitiveDict

from spotify_auth import get_code

# might not need to
access_token = get_code()

spotiurl = "https://api.spotify.com/v1"
playlist_id = input("enter URL for playlist (open.spotify.com/playlist/...)")
playlist_id = re.sub("https://open.spotify.com/playlist/", "", playlist_id)
# dont quite understand why i need the next line
# all i know is i copied it from somewhere and it works so here it is
headers = CaseInsensitiveDict()
headers["Authorization"] = "Bearer " + access_token


def search(song_name):
    params = {
        "q": song_name,
        "type": "track",
        "limit": 1,
        "include_external": "audio"
    }
    req = rq.get(spotiurl + "/search", headers=headers, params=params)
    json = req.json()
    return json


def get_uri(song_name):
    json = search(song_name)
    uri = json['tracks']['items'][0]['uri']
    return uri


def add_to_playlist(song_name):
    params = {
        "playlist_id": playlist_id,
        "uris": get_uri(song_name)
    }
    req = rq.post(spotiurl + "/playlists/" + playlist_id + "/tracks", params=params, headers=headers)
    #     not working (yet)
    print(req.status_code)
    print(req.text)


songs = input("file location of list of songs seperated by newlines (ex 'songs.txt')")
songs = open(songs)

for i in songs:
    add_to_playlist(i)
    time.sleep(0.5)
