import nfc

def on_connect(tag):
    print(f"Connected to {tag}")
    return True  # Return True to keep the tag connected, False to disconnect

def test_reader_connection():
    with nfc.ContactlessFrontend('usb') as clf:
        if clf:
            print("NFC reader is connected!")
            clf.connect(rdwr={'on-connect': on_connect})
        else:
            print("Unable to connect to the NFC reader.")

if __name__ == "__main__":
    test_reader_connection()
