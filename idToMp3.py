import json
import nfc
from time import sleep

# Function to read NFC tags with your ACR122U reader.
# The function should return the tag's unique ID.

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

def get_vinyl_info(tag_id, vinyl_collection):
    for vinyl in vinyl_collection:
        if vinyl['tag_id'] == tag_id:
            return vinyl['spotify_URI'], vinyl['URI_type']
    return None, None

def id_to_mp3():
    last_tag_id = None
    vinyl_collection = json.load(open('vinylCollection.json'))

    while True:
        tag_id = read_nfc_tag()
        if tag_id and tag_id != last_tag_id:
            print("new tag recieved")
            last_tag_id = tag_id
            spotify_URI, URI_type = get_vinyl_info(tag_id, vinyl_collection)
            if spotify_URI and URI_type:
                return spotify_URI, URI_type
        sleep(1)  # Prevent tight loop if you want to continually check
