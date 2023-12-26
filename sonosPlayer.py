import soco
from soco.data_structures import ExamplePlaylistContainer, ExampeResource
from soco.music_services import MusicService

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


device.next()  # Skip to next track
device.previous()  # Skip to previous track

device.play_mode = 'SHUFFLE' # Enable shuffle


"""