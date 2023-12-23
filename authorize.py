import webbrowser

from dotenv import load_dotenv
load_dotenv()  # load environment variables from .env

# Now you can import os and safely use the environment variables
import os


## Request user authorization variables
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_SECRET_ID') 
scope = os.getenv('SPOTIFY_SCOPE')
redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

auth_url = 'https://accounts.spotify.com/authorize'
response_type = 'code'

## Send auth request url
def get_auth_url():
    url = f"{auth_url}?client_id={client_id}&response_type={response_type}&redirect_uri={redirect_uri}&scope={scope}"
    return url

print("Visit this URL to authorize:", get_auth_url())

## visit auth url to get auth code
webbrowser.open(get_auth_url())

