import subprocess
import json
from time import sleep


#defunct function that used nfcpy library :(
"""def read_nfc_tag():
    clf = nfc.ContactlessFrontend('usb')
    
    print("Waiting for an NFC tag...")
    tag = clf.connect(rdwr={'on-connect': lambda tag: False})

    if tag.ndef:
        # NFC Data Exchange Format (NDEF) is a standardized data format that can be used to exchange information.
        ndef_records = tag.ndef.records
        if ndef_records:
            # Assuming the first record is text and contains the tag ID
            tag_id = ndef_records[0].text
            print(f"NFC Tag ID: {tag_id}")
            return tag_id
        else:
            print("No NDEF records found.")
            return None
    else:
        print("Tag is not NDEF formatted.")
        return None
    pass """
#failed read_nfc_tag() function trying readNfcTag.js 
"""def read_nfc_tag():
    ## tracking_tag_id = None
    try:
        print("Starting NFC Tag read process...")
        # Run the Node.js script and capture its output
        output = subprocess.check_output(['node', 'readNfcTag.js'], universal_newlines=True)
        tag_id = output.strip()  # Remove any extra whitespace
        print(f"NFC Tag ID read successfully: {tag_id}")

        
        return tag_id
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while reading the NFC tag: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
"""
# Function to read NFC tags with ACR122U reader.
# The function should return the tag's unique ID with detailed print statements
def read_nfc_tag():
    try:
        print("Starting NFC Tag read process...")
        # Run the Node.js script and capture its output
        process = subprocess.Popen(['node', 'readNfcTag.js'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate(timeout=10)  # Wait for 10 seconds for NFC read
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
        print("NFC Tag read process timed out.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while reading the NFC tag: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_vinyl_info(tag_id, vinyl_collection):
    print(f"Looking for tag_id: {tag_id}")
    for vinyl in vinyl_collection:
       # print(f"Checking tag_id: {vinyl['tag_id']}") #if you would like check each one
        if vinyl['tag_id'] == tag_id:
            return vinyl['spotify_URI'], vinyl['URI_type']
    return None, None

def id_to_mp3(last_tag_id):
    vinyl_collection = json.load(open('vinylCollection.json'))
    while True:
        print("inside id_to_mp3() while loop")
        tag_id = read_nfc_tag()
        if tag_id and tag_id != last_tag_id:
            print("new tag recieved")
            last_tag_id = tag_id
            spotify_URI, URI_type = get_vinyl_info(tag_id, vinyl_collection)
            print("URI: " + str(spotify_URI) + " Type:" + str(URI_type))
            if spotify_URI and URI_type:
                return spotify_URI, URI_type
        sleep(1)  # Prevent tight loop if you want to continually check

def id_to_mp3(last_tag_id):
    vinyl_collection = json.load(open('vinylCollection.json'))
    print("inside id_to_mp3()")
    tag_id = read_nfc_tag()
    if tag_id and tag_id != last_tag_id:
        print("new tag received")
        spotify_URI, URI_type = get_vinyl_info(tag_id, vinyl_collection)
        print("URI: " + str(spotify_URI) + " Type: " + str(URI_type))
        if spotify_URI and URI_type:
            return spotify_URI, URI_type, tag_id
    return None, None, last_tag_id



# testing call
# spotify_URI, URI_type = id_to_mp3()