import requests
import base64
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env


def refresh_access_token(refresh_token):
    print("refresh_access_token function called")
    
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_SECRET_ID')
    
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    
    if response.ok:
        new_tokens = response.json()
        expires_in = new_tokens['expires_in']
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        
        # Update the token data with the new access token and expiration time
        token_data = {
            'access_token': new_tokens['access_token'],
            'token_type': 'Bearer',
            'expires_in': expires_in,
            'expires_at': expires_at.isoformat(),
            'refresh_token': refresh_token,  # Keep the same refresh token
            'scope': os.getenv('SPOTIFY_SCOPE')
        }
        
        with open('/home/pi/raspberryPiRecordPlayer/tokens.json', 'w') as f: #absolute path
            json.dump(token_data, f, indent=4)

        print("New access token stored with expiration time.")
        return token_data
    else:
        print(f"Failed to refresh token, status code: {response.status_code}")
        print(f"Response text: {response.text}")
        raise Exception("Could not refresh token", response.text)

# Read the existing refresh token from tokens.json
with open('tokens.json', 'r') as f:
    token_data = json.load(f)

# Refresh the access token using the existing refresh token
# refresh_access_token(token_data['refresh_token']) #!!! do not need to run right now
