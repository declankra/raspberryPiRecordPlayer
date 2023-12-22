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
# Function to read NFC tags with ACR122U reader.
# The function should return the tag's unique ID with detailed print statements
def read_nfc_tag():
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


def get_vinyl_info(tag_id, vinyl_collection):
    for vinyl in vinyl_collection:
        if vinyl['tag_id'] == tag_id:
            return vinyl['spotify_URI'], vinyl['URI_type']
    return None, None

def id_to_mp3():
    last_tag_id = None
    vinyl_collection = json.load(open('vinylCollection.json'))

    while True:
        print("successfully inside id_to_mp3() while loop")
        tag_id = read_nfc_tag()
        if tag_id and tag_id != last_tag_id:
            print("new tag recieved")
            last_tag_id = tag_id
            spotify_URI, URI_type = get_vinyl_info(tag_id, vinyl_collection)
            if spotify_URI and URI_type:
                return spotify_URI, URI_type
        sleep(1)  # Prevent tight loop if you want to continually check

# testing call
## spotify_URI, URI_type = id_to_mp3()