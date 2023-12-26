import soco
from soco.data_structures import DidlMusicTrack, DidlResource

device = soco.SoCo('10.0.0.167')
spotify_uri = 'spotify:track:53xI80sTC0D7HaqieVEiDa'

# Test different protocol_info formats
protocol_info_options = [
    "sonos.com-spotify:*:audio/x-spotify:*",
    "x-rincon-mp3radio:*:audio/mpeg:*",
    "http-get:*:audio/*:*",
    "x-rincon-stream:*:audio/*:*",
    "x-sonos-spotify:*:audio/x-spotify:*"
]

for protocol_info in protocol_info_options:
    try:
        resource = DidlResource(uri=spotify_uri, protocol_info=protocol_info)
        track = DidlMusicTrack(title="Test Track", parent_id="0", item_id=spotify_uri, resources=[resource])
        device.add_to_queue(track)
        device.play_from_queue(0)
        print(f"Success with protocol_info: {protocol_info}")
        break
    except Exception as e:
        print(f"Failed with protocol_info: {protocol_info}, Error: {e}")

