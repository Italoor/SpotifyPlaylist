import requests as req
from bs4 import BeautifulSoup as bs
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
URL = "https://www.billboard.com/charts/hot-100"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
        show_dialog=True,
        cache_path="token.txt",
    )
)

user_id = sp.current_user()["id"]

date = input("Year to travel to (YYYY-MM-DD):")
year = int(date.split("-")[0])

response = req.get(f"{URL}/{date}")
site = response.text

soup = bs(site, 'html.parser')

song_data = soup("h3", id="title-of-a-story", class_="a-no-trucate")

songs = [songs.getText().strip("\n\t") for songs in song_data]

song_uris = []

for song in songs:
    result = sp.search(q=f'track:{song} year:{year}', limit=1, type='track')
    try:
        for item in result['tracks']['items']:
            song_uris.append(item['uri'])
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user_id, name=f"Top100 from {year}", public="False")

sp.user_playlist_add_tracks(user_id, playlist_id=playlist['id'], tracks=song_uris)