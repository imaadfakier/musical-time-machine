import os

# --- spotipy: client credentials flow > authorization code flow
os.environ['SPOTIPY_CLIENT_ID'] = 'enter client id'
SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
#   client secret key
os.environ['SPOTIPY_CLIENT_SECRET'] = 'enter secret key'
SPOTIPY_SECRET_KEY = os.environ.get('SPOTIPY_CLIENT_SECRET')
#   redirect uri
os.environ['SPOTIPY_REDIRECT_URI'] = 'enter redirect uri'
SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')
# ---
