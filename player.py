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
choosen_device = os.getenv('SPTOTIFY_CONNECTED_DEVICE_ID2') #set preferred device id

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
        return response.json()  # Returns the current playback state information
    elif response.status_code == 204:
        print("nothing is currently playing")
        return None
    else:
        print("Failed to get current playback state:", response.text)
        return exit()
        
#function to START playing uri on SPECIFIC device
def start_play(track_uri,track_type,access_token):
    preferred_device=choosen_device
    if track_type == 'song':
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'uris': [track_uri]
            
        }
        response = requests.put(f'https://api.spotify.com/v1/me/player/play?device_id={preferred_device}', headers=headers, json=data)
        if response.status_code == 204:
            print("Playback started for song.")
        else:
            print("Failed to start playback for song:", response.text)
    elif track_type == 'album' or track_type == 'playlist':
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'context_uri': [track_uri]
            
        }
        response = requests.put(f'https://api.spotify.com/v1/me/player/play?device_id={preferred_device}', headers=headers, json=data)
        if response.status_code == 204:
            print("Playback started for album/playlist.")
        else:
            print("Failed to start playback for album/playlist:", response.text)
    else:
        print("track type not set correctly")
        exit()

def transfer_playback(access_token):
    device_id = choosen_device
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
        print("Playback started.")
    else:
        print("Failed to start playback:", response.text)
        
# Function to play an album/playlist on Spotify using the track's URI
def play_context_uri(track_uri, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'context_uri': [track_uri]
    }
    response = requests.put('https://api.spotify.com/v1/me/player/play', headers=headers, json=data)
    if response.status_code == 204:
        print("Playback started.")
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
   
        
# core logic function that encapsulates sound settings and song playback logic
def sound_settings(track_uri, track_type):
    access_token = get_access_token() # Retrieve a valid access token before proceeding to any further api calls
    print("getting playback state")
    current_playback_state = get_playback_state(access_token) # Return the current playback state data

    #for state where an error was returned (/me/player = {else}) --> it already exited()....
    #for state where nothing is playing (/me/player = 204)
    if current_playback_state is None:
        print("initiating sound")
        start_play(track_uri,track_type,access_token)
    #for state where something is playing ( /me/player = 200) BUT device is NOT correct
    elif current_playback_state and current_playback_state.get('device') and current_playback_state['device']['id'] != choosen_device:
        print("transferring playback before playing")
        transfer_playback(access_token)
        print("now hitting play")
        if track_type == 'song':
            play_song(track_uri, access_token)
        elif track_type == 'album' or track_type == 'playlist':
            play_context_uri(track_uri, access_token)
        else:
            print("new song requested has incorrect track_type")
    #for state where something is playing ( /me/player = 200) BUT device IS correct
    elif current_playback_state and current_playback_state.get('device') and current_playback_state['device']['id'] == choosen_device:
        print("device is already correct")
        print("now hitting play")
        if track_type == 'song':
            play_song(track_uri, access_token)
        elif track_type == 'album' or track_type == 'playlist':
            play_context_uri(track_uri, access_token)
        else:
            print("new song requested has incorrect track_type")
    else:
        print("did not get caught in if else statements inside sound_settings")
        print(current_playback_state)
        

        
# main function loops the call to idToMp3 and checks if new = true before calling sound_settings()
# with potential to stop track if tag id returned = none
def mainRun():
    last_tag_id = None
    while True:
        spotify_URI, URI_type, tag_id = id_to_mp3(last_tag_id)
        if tag_id != last_tag_id:
            if spotify_URI and URI_type:
                # A new tag is detected and it's different from the last tag
                sound_settings(spotify_URI, URI_type)
                last_tag_id = tag_id  # Update the last tag ID
            elif tag_id is None:
                # No tag is detected, potentially stop the music
                stop_music(access_token = get_access_token())
                last_tag_id = None
        sleep(1)  # Sleep to prevent a tight loop
try:
    mainRun()
except KeyboardInterrupt:
    print("Program stopped by user.")
    
#main function loops the call to idToMp3 and checks if new = true before calling sound_settings()
"""def mainRun():
    last_tag_id = None
    while True:  # Infinite loop
        spotify_URI, URI_type, new_tag_id = id_to_mp3(last_tag_id)
        if spotify_URI and URI_type and new_tag_id != last_tag_id:
            last_tag_id = new_tag_id  # Update the last tag ID
            sound_settings(spotify_URI, URI_type)
        sleep(1)  # Add a sleep to prevent an overly tight loop"""


#archived main function loops
"""# main function
def mainRun():
    while True:  # Infinite loop
        spotify_URI, URI_type = id_to_mp3()
        if spotify_URI and URI_type:
            sound_settings(spotify_URI, URI_type)
try:
    mainRun()
except KeyboardInterrupt:
    print("Program stopped by user.")"""
    
"""# main function
def mainRun():
    #while: power is on??
    spotify_URI, URI_type = id_to_mp3()
    if spotify_URI and URI_type:
        sound_settings(spotify_URI, URI_type)

mainRun() # call the main function when player.py is ran"""


# Call `sound_settings` with the track URI
## sound_settings('spotify:track:4zlbKky2yA657Sk5rekZoR')




### NEXT UP ACTIONS / QUESTIONS:
    ## run through the logic ---- yeah just this... needs some code review to handle all cases logically. you've been at it for too long. but hell yeah. it fuckin works!!
    
    
    
        #areas to address
            #how to handle when it is not playing
                #get play backstate = 204 or is_playing = false
            #how to best set the logic flow within sound_settings()
                #what should be checked first? why?
                    #is something playing? y/n
                        #if n->
                            #start playing
                            #check if device is correct
                        #if y->
                            #continue
                    #is it playing on correct device? y/n
                        #if n->
                            #switch to correct device
                        #if y -> 
                            #continue
        
    #then the bigger problem -> dont let it exit after it plays a song "playback started"                
                


## REMEMBER 
# continue to visualizing logic as i create it, it helps!!!


        
        
"""
if current_playback_state and current_playback_state.get('device') and current_playback_state['device']['id'] != choosen_device and current_playback_state.status_code ==200:
        transfer_playback_true(choosen_device, access_token)
        # after ensuring we're on the correct device, play the song
        play_song(track_uri, access_token)
    else:
        start_song(track_uri,choosen_device, access_token)
    #for state where no song is playing
    
"""


"""" archived code
def start_song(spotify_URI, device_id, access_token):
    # Transfer playback to the specified device
    endpoint_transfer = 'https://api.spotify.com/v1/me/player'
    payload_transfer = {
        'device_ids': [device_id],
        'play': False
    }
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response_transfer = requests.put(endpoint_transfer, json=payload_transfer, headers=headers)
    
    if response_transfer.status_code in range(200, 299):
        print("Playback transferred successfully. Starting song.")
        # Start playing the song on the new device
        endpoint_play = f'https://api.spotify.com/v1/me/player/play?device_id={device_id}'
        payload_play = {
            'uris': [spotify_URI]  # List of URIs to play
        }
        response_play = requests.put(endpoint_play, json=payload_play, headers=headers)
        
        if response_play.status_code in range(200, 299):
            print("Song started playing successfully.")
        else:
            print(f"Failed to start song, status code: {response_play.status_code}")
            print(f"Response text: {response_play.text}")
    else:
        print(f"Failed to transfer playback, status code: {response_transfer.status_code}")
        print(f"Response text: {response_transfer.text}")
"""