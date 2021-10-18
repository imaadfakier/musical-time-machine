import requests
import bs4
# import lxml
import datetime
import calendar
import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# from spotipy.oauth2 import SpotifyClientCredentials
import config
import pprint

# --------------------------------------------- STEP 1: ---------------------------------------------
# ---
BASE_URL = 'enter base url'
is_sunday = False
travel_back_to = input('Which year do you want to travel back to? Type the date in this format: YYYY-MM-DD\n')
year = int(travel_back_to.split('-')[0])
month = int(travel_back_to.split('-')[1])
day = int(travel_back_to.split('-')[2])
if calendar.day_name[datetime.date(year=year, month=month, day=day).weekday()] == 'Sunday':
    day -= 1
    is_sunday = True
travel_back_to = datetime.date(year=year, month=month, day=day).strftime('%Y-%m-%d')
URL_ADD_ON = f'/{travel_back_to}'
url = BASE_URL + URL_ADD_ON
response = requests.get(url=url)
response.raise_for_status()
website_html = response.text
# ---

# ---
soup = bs4.BeautifulSoup(markup=website_html, features='lxml')
all_song_tags = soup.find_all(name='span', class_='chart-element__information__song')
top_100_songs = [song_tag.text for song_tag in all_song_tags]
# ---

# --------------------------------------------- STEP 2: ---------------------------------------------
# spotipy documentation link: https://spotipy.readthedocs.io/en/2.19.0/
# ---
# --- spotipy
#                                           authorization code flow
scope = 'playlist-modify-private'
sp = spotipy.Spotify(
    auth_manager=spotipy.oauth2.SpotifyOAuth(
        scope=scope,
    )
)
user_id = sp.current_user()['id']
# ---
# ---

# --------------------------------------------- STEP 3: ---------------------------------------------
# ---
all_song_uris = list()

for song_name in top_100_songs:
    track = sp.search(q=f'track: {song_name} year: {year}', type='track', limit=1)
    pprint.pprint(track)

    try:
        the_uri = track['tracks']['items'][0]['uri']
        print(track['tracks']['items'][0]['uri'])
        all_song_uris.append(the_uri)
    # except IndexError, TypeError as e:  # parenthesis are required
    except (IndexError, TypeError) as e:
        print('The song, {song_name}, is not on Spotify - moving on to the next.'.format(song_name=song_name))
# ---

# --------------------------------------------- STEP 4: ---------------------------------------------
if is_sunday:
    day += 1
    travel_back_to = datetime.date(year=year, month=month, day=day).strftime('%Y-%m-%d')

playlist_id = sp.user_playlist_create(user=user_id, name=f'{travel_back_to} Billboard 100', public=False)['id']

sp.playlist_add_items(
    playlist_id=playlist_id,
    items=all_song_uris
)
