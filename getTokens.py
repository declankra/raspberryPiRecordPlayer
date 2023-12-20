import requests
import base64
import json
from dotenv import load_dotenv
load_dotenv()  # load environment variables from .env
import os

def get_tokens(code):
    # fetch variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_SECRET_ID')
    redirect_uri = 'http://localhost:8888/callback'
   
    # create the header
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # create the arguments
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }
    # make POST request to Spotify's API
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    
    if response.ok: # check response
        # Save the tokens to a json file in current directory
        tokens = response.json()
        with open('tokens.json', 'w') as f:
            json.dump(tokens, f, indent=4)
        print("Tokens stored in 'tokens.json'")
    else:
        print("Failed to retrieve tokens")
        print("Response Code:", response.status_code)
        print("Response Text:", response.text)


code = os.getenv('SPOTIFY_AUTH_CODE') # newly retrieved auth code stored in .env
get_tokens(code) # run the function
