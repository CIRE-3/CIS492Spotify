from dotenv import load_dotenv
import os
import base64
from requests import post
import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read playlist-modify-public playlist-modify-private"

load_dotenv()

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost/",
    scope=scope
))

#method to get users liked songs

def get_liked_songs(sp):
    
    liked_songs = []
    results = sp.current_user_saved_tracks()
    while results:
        for item in results['items']:
            track = item['track']
            liked_songs.append({
                'name': track['name'],
                'id': track['id'],
                'artist': track['artists'][0]['name']
            })
        # Check if there are more liked songs to retrieve
        results = sp.next(results) if results['next'] else None
    return liked_songs

'''def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type":  "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

token = get_token()'''