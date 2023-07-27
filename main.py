from bs4 import BeautifulSoup
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
date = input("Tell me the date where you want to travel to? I will find top 100 music for you. Try this format "
             "YYYY-MM-DD: ")
person = input("For who do you want to create a spotify playlist ? ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"

# Get a response
response = requests.get(url=URL)
music_hits = response.text

song_list = []
# Lets make some soup
soup = BeautifulSoup(music_hits, "html.parser")
Spotify_ID = os.environ["SPOTIPY_CLIENT_ID"]
Spotify_Secret = os.environ["SPOTIPY_CLIENT_SECRET"]

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=Spotify_ID,
        client_secret=Spotify_Secret,
        redirect_uri="http://localhost:9000",
        scope="playlist-modify-private",
        cache_path="token,txt",
        show_dialog=True

    )
)
user_id = spotify.current_user()["id"]


music_title = soup.find_all("h3", class_="a-no-trucate")

for title in music_title[3:103]:
    name = title.get_text()
    song_list.append(name)


cleaned_list = [name.strip() for name in song_list]
print(cleaned_list)

song_uris = []
year = date.split("-")[0]

for song in cleaned_list:
    final = spotify.search(q=f"track:{song} year: {year}")

    try:
        uri = final["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"This song ({song}) didn't exist in Spotify. Skipped")


# Create a playlist
new_playlist = spotify.user_playlist_create(user=user_id, name=f"Top 100 music of {year} year for {person}", public=False)

add_music = spotify.playlist_add_items(playlist_id=new_playlist["id"], items=song_uris)
