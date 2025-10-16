import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

BILLBOARD_URL = os.getenv("BILLBOARD_URL1")
USERNAME = os.getenv("USERNAME1")
SPOTIFY_ENDPOINT = os.getenv("SPOTIFY_ENDPOINT1")
CLIENT_ID = os.getenv("CLIENT_ID1")
CLIENT_SECRET = os.getenv("CLIENT_SECRET1")
REDIRECT_URI = os.getenv("REDIRECT_URI1")


date_input = input("Write your desired date in the format YYYY-MM-DD: ")

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
response = requests.get(BILLBOARD_URL, headers=header)
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")
song_names_spans = soup.select("li ul li h3")
songs = [song.getText().strip() for song in song_names_spans]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope="playlist-modify-public",
                                                show_dialog=True,
                                                cache_path="token.txt",
                                                username=USERNAME))

user_id = sp.current_user()["id"]

song_uris = []
year = date_input.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist_name = f"Billboard Hot 100 when you were born"
description = f"Top 100 songs on Billboard songs on {date_input}"

playlist = sp.user_playlist_create(user=user_id,
                                   name=playlist_name,
                                   description=description,
                                   public=True)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)