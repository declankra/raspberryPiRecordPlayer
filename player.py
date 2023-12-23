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
        return None
        
def transfer_playback_true(device_id, access_token):
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
        print(f"Failed to transfer playback, status code: {response.status_code}")
        print(f"Response text: {response.text}")
        

        
# Main function that encapsulates sound settings and song playback
def sound_settings(track_uri, track_type): #set preferred device id
    preferred_device_id=choosen_device
    access_token = get_access_token() # Retrieve a valid access token
    """CHOOSDEVICE???"""
    
    print("getting playback state")
    current_playback_state = get_playback_state(access_token) # Return the current playback state data

    #for state where song is playing
    if current_playback_state and current_playback_state.get('device') and current_playback_state['device']['id'] != preferred_device_id and current_playback_state.status_code ==200:
        transfer_playback_true(preferred_device_id, access_token)
        # after ensuring we're on the correct device, play the song
        play_song(track_uri, access_token)
    else:
        start_song(track_uri,"3e051197-ec49-4da9-94f7-82914d92b4f6_amzn_1", access_token)
    #for state where no song is playing
    
    

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
        
        
def mainRun():
    #while: power is on??
    spotify_URI, URI_type = id_to_mp3()
    if spotify_URI and URI_type:
        sound_settings(spotify_URI, URI_type)

mainRun() # call the main function when player.py is ran


# Call `sound_settings` with the track URI
## sound_settings('spotify:track:4zlbKky2yA657Sk5rekZoR')




### NEXT UP ACTIONS / QUESTIONS:
    ## run through the logic ---- yeah just this... needs some code review. you've been at it for too long. but hell yeah. it fuckin works!!
    
    
    
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