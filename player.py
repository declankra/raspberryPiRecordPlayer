import requests
import json
import base64
import os
from datetime import datetime, timedelta

####### ACCESS TOKEN AND REFRESH TOKEN MECHANISM ########

# access tokens from 'tokens.json'
TOKENS_FILE = 'tokens.json'
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_SECRET_ID')

def read_tokens_from_file():
    with open(TOKENS_FILE, 'r') as file:
        tokens = json.load(file)
    return tokens

def write_tokens_to_file(tokens):
    with open(TOKENS_FILE, 'w') as file:
        json.dump(tokens, file, indent=4)

# setup request for access token, using refresh token
def refresh_access_token(refresh_token):
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    
    if response.ok: # check if response works, to re-write tokens.json
        new_tokens = response.json()
        new_tokens['refresh_token'] = refresh_token  # Reuse the same refresh token
        write_tokens_to_file(new_tokens)
        return new_tokens['access_token'], datetime.now() + timedelta(seconds=new_tokens['expires_in'])
    else:
        raise Exception("Could not refresh token")

# function to request to new access token
def get_access_token():
    tokens = read_tokens_from_file()
    access_token = tokens['access_token'] # fetch current access token data
    expiration = datetime.fromisoformat(tokens['expires_at'])
    if datetime.now() >= expiration: # check if access token has expired
        access_token, expiration = refresh_access_token(tokens['refresh_token'])
        tokens['access_token'] = access_token
        tokens['expires_at'] = expiration.isoformat()
        write_tokens_to_file(tokens)
    return access_token # return valid access token

# now use 'access_token = get_access_token()' at the beginning of any requests to the Spotify API

####### player.py logic - requests to Spotify API ########


