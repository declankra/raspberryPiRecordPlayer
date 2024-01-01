from time import sleep
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
choosen_device = os.getenv('SPTOTIFY_CONNECTED_DEVICE_ID_REAL') #set preferred device id
choosen_device_trimmed = os.getenv('SPTOTIFY_CONNECTED_DEVICE_ID_TRIMMED') #set preferred device id


def read_tokens_from_file():
    with open(TOKENS_FILE, 'r') as file:
        tokens = json.load(file)
    return tokens

def write_tokens_to_file(tokens):
    with open(TOKENS_FILE, 'w') as file:
        json.dump(tokens, file, indent=4)

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
        token_data = refresh_access_token(tokens['refresh_token'])
        access_token = token_data['access_token']  # Update the access token
        expiration = token_data['expires_at']  # Update the expiration time
        tokens['access_token'] = access_token
        tokens['expires_at'] = expiration
        write_tokens_to_file(tokens)
        return access_token
    else:
        print("Access token accepted")
        return access_token # return valid access token

# !!! now use 'access_token = get_access_token()' at the beginning of any requests to the Spotify API

####### player.py logic - requests to Spotify API ########

# Function to get the current playback state and device ID 
def get_playback_state(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.spotify.com/v1/me/player', headers=headers)
    if response.status_code == 200:
        print("something is playing")
        json_response = response.json()  # Convert to JSON
        device_id = json_response["device"]["id"]
        print(device_id)  # Print the device ID        
        return json_response  # Return the playback state information
    elif response.status_code == 204:
        print("nothing is currently playing")    
        return None
    elif response.status_code == 500:
        print("500 server error")
        return None
    else:
        print("Failed to get current playback state:", response.text)
        return exit()
        
#function to START playing uri on SPECIFIC device
def start_play(uri, access_token):
    
    shuffleStatus = False # initiate shuffle status
    preferred_device=choosen_device_trimmed
    print("choosed trimmed device")
    headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
    if 'track' in uri:
        track_type = "song"
        print("uri type = " + track_type)
        shuffleStatus = False # set shuffle status
        data = {'uris': [uri]}  # For tracks
    elif 'album' in uri or 'playlist' in uri:
        track_type = "album/playlist"
        print("uri type = " + track_type)
        shuffleStatus = True # set shuffle status
        data = {'context_uri': uri}  # For albums or playlists
    else:
        print("URI type not recognized")
        return
    
    # make request to /player/play/ with device id
    response = requests.put(f'https://api.spotify.com/v1/me/player/play?device_id={preferred_device}', headers=headers, json=data)
    if response.status_code == 204:
        print("Playback started successfully for " + track_type)
    else:
        print(f"Failed to start playback: {response.status_code} - {response.text}")
    
    get_playback_state(access_token)

   
    ### ??? TRY SHUFFLE BEFORE VOLUME REQUEST???
     # Check and set shuffle 
    if shuffleStatus == True:
        shuffleModeOn(access_token) # activate shuffle
    elif shuffleStatus == False:
        shuffleModeOff(access_token) # ensure shuffle mode is off
    
    get_playback_state(access_token)

    # Function to set the volume to 30%
    def set_volume(volume_percent, device_id, token):
        volume_endpoint = f'https://api.spotify.com/v1/me/player/volume?volume_percent={volume_percent}&device_id={device_id}'
        volume_headers = {
            'Authorization': f'Bearer {token}'
        }
        volume_response = requests.put(volume_endpoint, headers=volume_headers)
        return volume_response.status_code == 204
    # Check and set volume
    if not set_volume(30, preferred_device, access_token):
        print("Failed to set volume")
        return

    get_playback_state(access_token)

""""
    if track_type == 'song':
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'uris': [uri]
        }
        response = requests.put(f'https://api.spotify.com/v1/me/player/play?device_id={preferred_device}', headers=headers, json=data)
        if response.status_code == 204:
            print("Playback started for song.")
            shuffleModeOff(access_token) # ensure shuffle mode is off
            # Check and set volume
            if not set_volume(30, preferred_device, access_token):
                print("Failed to set volume")
                return
            get_playback_state(access_token)
        else:
            print("Failed to start playback for song:", response.text)
    elif track_type == 'album' or track_type == 'playlist':
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        data = {
        "context_uri": uri
        }
        response = requests.put(f'https://api.spotify.com/v1/me/player/play?device_id={preferred_device}', headers=headers, json=data)
        if response.status_code == 204:
            print("Playback started for album/playlist.")
            shuffleModeOn(access_token) # activate shuffle
             # Check and set volume
            if not set_volume(30, preferred_device, access_token):
                print("Failed to set volume")
                return
            get_playback_state(access_token)
        else:
            print("Failed to start playback for album/playlist:", response.text)
    else:
        print("track type not set correctly")
        exit()
"""

def transfer_playback(access_token):
    device_id = choosen_device
    print("transferring to real device")
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'device_ids': [device_id],
        'play': True  # This ensures playback continues immediately after transfer
    }
    response = requests.put('https://api.spotify.com/v1/me/player', headers=headers, json=data)
    if response.status_code == 204:
        print("Playback transferred to device with ID:", device_id)
    else:
        print(f"Failed to transfer playback, status code: {response.status_code}")
        print(f"Response text: {response.text}")

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
        print("Playing song")
        shuffleModeOff(access_token) # ensure shuffle mode is off
    else:
        print("Failed to start playback:", response.text)

        
        
# Function to play an album/playlist on Spotify using the track's URI
def play_context_uri(track_uri, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "context_uri": track_uri
    }
    response = requests.put('https://api.spotify.com/v1/me/player/play', headers=headers, json=data)
    if response.status_code == 204:
        print("Playing playlist/album")
        shuffleModeOn(access_token) # activate shuffle
    else:
        print("Failed to start playback:", response.text)    
        
def stop_music(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.put('https://api.spotify.com/v1/me/player/pause', headers=headers)
    if response.status_code in [200, 204]:
        print("Playback stopped.")
    else:
        print("Failed to stop playback:", response.status_code, response.text)
        
def shuffleModeOn(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = f'https://api.spotify.com/v1/me/player/shuffle?state=true&device_id={choosen_device}'  # Use f-string for URL
    response = requests.put(url, headers=headers)
    if response.status_code == 204:
        print("Shuffle = TRUE")
    else:
        print("Failed to shuffle playback:", response.text)
        
def shuffleModeOff(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = f'https://api.spotify.com/v1/me/player/shuffle?state=false&device_id={choosen_device}'  # Use f-string for URL
    response = requests.put(url, headers=headers)
    if response.status_code == 204:
        print("Shuffle = FALSE")
    else:
        print("Failed to NOT shuffle playback:", response.text)
        
# core logic function that encapsulates sound settings and song playback logic
def sound_settings(track_uri, track_type):
    access_token = get_access_token() # Retrieve a valid access token before proceeding to any further api calls
    print("getting playback state")
    current_playback_state = get_playback_state(access_token) # Return the current playback state data

    #for state where an error was returned (/me/player = {else}) --> it already exited()....
    #for state where nothing is playing (/me/player = 204)
    if current_playback_state is None:
        print("initiating sound")
        #transfer_playback(access_token) # FIX!!! this ensures playback is transferred to correct device AND play = TRUE, BEFORE making a play call (should resolve amazon device going to sleep issue)
        start_play(track_uri, access_token) # !!! ON TRIMMED
        transfer_playback(access_token) # transfer to REAL
    #for state where something is playing ( /me/player = 200) BUT device is NOT correct
    elif current_playback_state and current_playback_state.get('device') and current_playback_state['device']['id'] != choosen_device:
        print("transferring playback before playing")
        transfer_playback(access_token)
        print("now hitting play")
        if track_type == 'song':
            print("type = song")
            play_song(track_uri, access_token)
        elif track_type == 'album' or track_type == 'playlist':
            print("type = album/playlist")
            play_context_uri(track_uri, access_token)
        else:
            print("new song requested has incorrect track_type")
    #for state where something is playing ( /me/player = 200) BUT device IS correct
    elif current_playback_state and current_playback_state.get('device') and current_playback_state['device']['id'] == choosen_device:
        print("device is already correct")
        if track_type == 'song':
            print("hitting play & type = song")
            play_song(track_uri, access_token)
        elif track_type == 'album' or track_type == 'playlist':
            print("hitting play & type = playlist/album")
            play_context_uri(track_uri, access_token)
        else:
            print("new song requested has incorrect track_type")
    else:
        print("did not get caught in if else statements inside sound_settings")
        print(current_playback_state) # print playback state for debugging
        

        
# main function loops the call to idToMp3 and checks if new id = true before calling sound_settings()
# with potential to stop track if tag id returned = none
def mainRun():
    last_tag_id = None # set initial state
    while True: # infinite loop
        spotify_URI, URI_type, tag_id = id_to_mp3(last_tag_id) # call function with last tag id
        if tag_id != last_tag_id: # check if tag id returned is new
            if spotify_URI and URI_type: # check if other variables are valid i.e. != none >>> if tag_id = none then these should be valid
                # A new tag is detected and it's different from the last tag
                sound_settings(spotify_URI, URI_type) # call sound settings with uri & type
                last_tag_id = tag_id  # Update last tag id to the valid tag id that was just used
            elif tag_id is None: # validation check that tag_id is none (given it is already different)
                # No tag is detected >> stop the music
                stop_music(access_token = get_access_token())
                last_tag_id = None # set last tag id to the none tag id that was just used
        sleep(1)  # Sleep to prevent a tight loop
try:
    mainRun()
except KeyboardInterrupt:
    print("Program stopped by user.")
