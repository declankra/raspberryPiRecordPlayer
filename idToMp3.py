import subprocess
import json
from time import sleep

# Function to read NFC tags with ACR122U reader.
# The function should return the tag's unique ID with detailed print statements
def read_nfc_tag():
    process = None
    try:
        print("Starting NFC Tag read process...")
        # Run the Node.js script and capture its output
        process = subprocess.Popen(['node', '/home/pi/raspberryPiRecordPlayer/readNfcTag.js'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #absolute path
        output, error = process.communicate(timeout=2)  # Wait for 2 seconds for NFC read, then timeout
        if error:
            print(f"Error while reading NFC tag: {error.decode().strip()}")
            return None
        tag_id = output.decode().strip()  # Decode and strip whitespace from the output
        if tag_id:
            print(f"NFC Tag ID read successfully: {tag_id}")
            return tag_id
        else:
            print("No NFC Tag ID found.")
            return None
    except subprocess.TimeoutExpired:
        # CRITICAL: Kill the process to prevent zombie accumulation
        if process:
            process.kill()
            process.wait()  # Reap the zombie process
        print("NFC Tag read process timed out.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while reading the NFC tag: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    finally:
        # Ensure process is cleaned up in all cases
        if process and process.poll() is None:
            process.kill()
            process.wait()


def get_vinyl_info(tag_id, vinyl_collection):
    print(f"Looking for tag_id: {tag_id}")
    for vinyl in vinyl_collection:
       # print(f"Checking tag_id: {vinyl['tag_id']}") #if you would like check each one
        if vinyl['tag_id'] == tag_id:
            return vinyl['spotify_URI'], vinyl['URI_type']
    return None, None


def id_to_mp3(last_tag_id):
    # Use context manager to prevent file descriptor leak (was causing crash after ~1 hour)
    with open('/home/pi/raspberryPiRecordPlayer/vinylCollection.json') as f:
        vinyl_collection = json.load(f)
    print("inside id_to_mp3()")
    tag_id = read_nfc_tag()  #use the read_nfc_tag function to get the tag ID
    if tag_id and tag_id != last_tag_id:
        print("new tag received")
        spotify_URI, URI_type = get_vinyl_info(tag_id, vinyl_collection)
        print("URI: " + str(spotify_URI) + " Type: " + str(URI_type))
        if spotify_URI and URI_type:
            return spotify_URI, URI_type, tag_id
    elif tag_id == None and tag_id != last_tag_id:
        return None, None, None
   ## print(last_tag_id)
    return None, None, last_tag_id

# testing call
# spotify_URI, URI_type = id_to_mp3()