import soco
from soco.music_services import MusicService
from soco.data_structures import DidlMusicTrack, DidlResource

# Function to create a DIDL object for a Spotify track
def create_spotify_track(uri):
    resource = DidlResource(uri=uri, protocol_info="sonos.com-spotify:*:audio/x-spotify:*")
    return DidlMusicTrack(title="Spotify Track", parent_id="0", item_id=uri, resources=[resource])

# Function to play a track from Spotify URI
def play_spotify_uri_on_sonos(uri):
    # Connect to your Sonos speaker
    device = soco.SoCo('10.0.0.167')  # Replace with your device's IP

    # Clear the current queue
    device.clear_queue()

    # Create and add the track to the queue
    track = create_spotify_track(uri)
    device.add_to_queue(track)

    # Play the first track in the queue
    device.play_from_queue(0)

# Example usage: Replace this part with your NFC tag scanning logic
# This is where you would receive the Spotify URI from the NFC tag
scanned_uri = 'spotify:track:53xI80sTC0D7HaqieVEiDa'
play_spotify_uri_on_sonos(scanned_uri)





""""
# set device to your sonos speaker
device = soco.SoCo('10.0.0.167') #Device: Family Room, IP: 10.0.0.167 
# Get the Spotify music service
spotify_service = MusicService('Spotify')


# Adjust volume
device.volume = 20  # Set volume to 20%


# Spotify URI
spotify_uri = 'spotify:track:53xI80sTC0D7HaqieVEiDa'


# Add the playlist to the queue and play it

queue = device.add_to_queue(spotify_uri)
device.play_from_queue(queue)
"""""

"""
device.play() # Play
device.pause() # Pause
device.stop()

device.volume = 10  # Set volume to 10%

device.mute = True  # Mute the speaker
device.mute = False  # Unmute the speaker

device.add_uri_to_queue('TRACK_URI')  # Add track to queue
device.remove_from_queue(index)  # Remove track from queue

device.get_current_track_info() # get playback info

queue = device.get_queue() # retreive current queue
for item in queue:
    print(item.title)

device.clear_queue() # clear queue

device.next()  # Skip to next track
device.previous()  # Skip to previous track

device.play_mode = 'SHUFFLE' # Enable shuffle


"""