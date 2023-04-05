import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv("config.env")

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

URL = "https://www.billboard.com/charts/hot-100"
SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")

response = requests.get(f"{URL}/{date}")
top_song_html = response.text
soup = BeautifulSoup(top_song_html, "html.parser")
song_title = soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")

songs_list = [song.getText().strip() for song in song_title]
song_uris = []

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri="http://example.com", scope="playlist-modify-private"))
user_id = sp.current_user()["id"]
year = date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
print(song_uris)

new_playlist = sp.user_playlist_create(user=user_id, name=f"{date} 100 Billboard", public=False)
sp.playlist_add_items(playlist_id=new_playlist["id"], items=song_uris)
