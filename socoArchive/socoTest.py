import soco

# Discover all Sonos devices on the network
devices = soco.discover()

# Print out each device's information
for device in devices:
    print(f"Device: {device.player_name}, IP: {device.ip_address}")


from soco.data_structures import DidlMusicTrack, DidlResource

device = soco.SoCo('10.0.0.167')
spotify_uri = 'spotify:track:53xI80sTC0D7HaqieVEiDa'
resource = DidlResource(uri=spotify_uri, protocol_info="sonos.com-spotify:*:audio/x-spotify:*")
track = DidlMusicTrack(title="Test Track", parent_id="0", item_id=spotify_uri, resources=[resource])

device.add_to_queue(track)
device.play_from_queue(0)
