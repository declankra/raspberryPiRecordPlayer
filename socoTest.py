import soco

# Discover all Sonos devices on the network
devices = soco.discover()

# Print out each device's information
for device in devices:
    print(f"Device: {device.player_name}, IP: {device.ip_address}")

