import requests
import json
import base64
import os
from datetime import datetime, timedelta
from refreshTokens import refresh_access_token # Import the refresh_access_token function from refreshTokens.py
from idToMp3 import id_to_mp3 # import the main function id_to_mp3 from other .py file to run in mainRun() function

####### ACCESS TOKEN AND REFRESH TOKEN MECHANISM ########

# access tokens from 'tokens.json'
TOKENS_FILE = 'tokens.json'
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_SECRET_ID')
choosen_device = os.getenv('SPTOTIFY_CONNECTED_DEVICE_ID')

def read_tokens_from_file():
    with open(TOKENS_FILE, 'r') as file:
        tokens = json.load(file)
    return tokens

def write_tokens_to_file(tokens):
    with open(TOKENS_FILE, 'w') as file:
        json.dump(tokens, file, indent=4)

# setup request for access token, using refresh token ** no longer needed -> it now references refresh_access_token() in refreshTokens.py
"""def refresh_access_token(refresh_token):
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
        print(f"Failed to refresh token, status code: {response.status_code}")
        print(f"Response text: {response.text}")
        raise Exception("Could not refresh token")
    """

# function to request a new access token
def get_access_token():
    tokens = read_tokens_from_file()
    access_token = tokens['access_token'] # fetch current access token data
    expiration = datetime.fromisoformat(tokens['expires_at'])
    current_time = datetime.now()
    print(f"Current time: {current_time}")
    print(f"Expiration time: {expiration}")
    if current_time >= expiration: # check if access token has expired
        print("Access token expired")
        access_token, expiration = refresh_access_token(tokens['refresh_token'])
        tokens['access_token'] = access_token
        tokens['expires_at'] = expiration.isoformat()
        write_tokens_to_file(tokens)
        return access_token
    else:
        return access_token # return valid access token

# !!! now use 'access_token = get_access_token()' at the beginning of any requests to the Spotify API


####### player.py logic - requests to Spotify API ########


# Function to get the current playback state and device ID 
def get_playback_state(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.spotify.com/v1/me/player', headers=headers)
    if response.ok:
        return response.json()  # Returns the current playback state information
    else:
        print("Failed to get current playback state:", response.text)
        return None

# Function to transfer playback to a different device ** not called if playback state = preferred
def transfer_playback(device_id, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'device_ids': [device_id],
        'play': True  # This ensures playback happens immediately after transfer
    }
    response = requests.put('https://api.spotify.com/v1/me/player', headers=headers, json=data)
    if response.status_code == 204:
        print("Playback transferred to device with ID:", device_id)
    else:
        print("Failed to transfer playback:", response.text)
        
# Main function that encapsulates sound settings and song playback
def sound_settings(track_uri, preferred_device_id=choosen_device): #set preferred device id
    access_token = get_access_token() # Retrieve a valid access token
    """CHOOSDEVICE???"""
    current_playback_state = get_playback_state(access_token) # Return the current playback state data
    if current_playback_state and current_playback_state.get('device') and current_playback_state['device']['id'] != preferred_device_id:
        transfer_playback(preferred_device_id, access_token)
    # After ensuring we're on the correct device, play the song
    play_song(track_uri, access_token)

# Function to play a song on Spotify using the track's URI
def play_song(track_uri, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'uris': [track_uri]
    }
    response = requests.put('https://api.spotify.com/v1/me/player/play', headers=headers, json=data)
    if response.status_code == 204:
        print("Playback started.")
    else:
        print("Failed to start playback:", response.text)



def mainRun():
    id_to_mp3()

mainRun() # call the main function when player.py is ran


# Call `sound_settings` with the track URI
## sound_settings('spotify:track:4zlbKky2yA657Sk5rekZoR')




### NEXT UP ACTIONS / QUESTIONS:



## REMEMBER 
# continue to visualizing logic as i create it, it helps!!!