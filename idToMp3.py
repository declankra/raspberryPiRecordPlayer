import subprocess
import json
import threading
import os
from time import sleep

# Persistent NFC Reader class
class NFCReader:
    def __init__(self, script_path='/home/pi/raspberryPiRecordPlayer/nfcReaderPersistent.js'):
        self.script_path = script_path
        self.process = None
        self.current_card = None
        self.lock = threading.Lock()
        self.reader_thread = None
        self.running = False

    def start(self):
        """Start the persistent NFC reader process"""
        if self.running:
            return

        self.running = True
        self.process = subprocess.Popen(
            ['node', self.script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,  # Line buffered
            universal_newlines=True
        )

        # Start thread to read stdout
        self.reader_thread = threading.Thread(target=self._read_output, daemon=True)
        self.reader_thread.start()

        # Start thread to log stderr (for debugging)
        self.stderr_thread = threading.Thread(target=self._read_stderr, daemon=True)
        self.stderr_thread.start()

        print("[NFCReader] Persistent reader started")

    def _read_output(self):
        """Continuously read stdout from the Node.js process"""
        while self.running and self.process and self.process.poll() is None:
            try:
                line = self.process.stdout.readline()
                if line:
                    line = line.strip()
                    with self.lock:
                        if line.startswith('CARD:'):
                            self.current_card = line[5:]  # Extract UID after "CARD:"
                            print(f"[NFCReader] Card detected: {self.current_card}")
                        elif line == 'CARD_REMOVED':
                            print(f"[NFCReader] Card removed (was: {self.current_card})")
                            self.current_card = None
            except Exception as e:
                print(f"[NFCReader] Error reading output: {e}")
                break

        # Process died - try to restart
        if self.running:
            print("[NFCReader] Process died, restarting in 2 seconds...")
            sleep(2)
            self._restart()

    def _read_stderr(self):
        """Read stderr for debugging info"""
        while self.running and self.process and self.process.poll() is None:
            try:
                line = self.process.stderr.readline()
                if line:
                    print(f"[NFCReader-debug] {line.strip()}")
            except:
                break

    def _restart(self):
        """Restart the reader process"""
        self.stop()
        sleep(1)
        self.start()

    def stop(self):
        """Stop the NFC reader process"""
        self.running = False
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None

    def get_current_card(self):
        """Get the currently detected card UID, or None if no card"""
        with self.lock:
            return self.current_card


# Global reader instance
_nfc_reader = None

def get_nfc_reader():
    """Get or create the global NFC reader instance"""
    global _nfc_reader
    if _nfc_reader is None:
        _nfc_reader = NFCReader()
        _nfc_reader.start()
        # Give it a moment to initialize
        sleep(1)
    return _nfc_reader


def get_vinyl_info(tag_id, vinyl_collection):
    """Look up vinyl info by tag ID"""
    print(f"Looking for tag_id: {tag_id}")
    for vinyl in vinyl_collection:
        if vinyl['tag_id'] == tag_id:
            return vinyl['spotify_URI'], vinyl['URI_type']
    return None, None


def id_to_mp3(last_tag_id):
    """
    Get current NFC tag and look up its Spotify info.
    Returns (spotify_URI, URI_type, tag_id)
    """
    # Use context manager to prevent file descriptor leak
    with open('/home/pi/raspberryPiRecordPlayer/vinylCollection.json') as f:
        vinyl_collection = json.load(f)

    # Get current card from persistent reader
    reader = get_nfc_reader()
    tag_id = reader.get_current_card()

    if tag_id and tag_id != last_tag_id:
        print("new tag received")
        spotify_URI, URI_type = get_vinyl_info(tag_id, vinyl_collection)
        print("URI: " + str(spotify_URI) + " Type: " + str(URI_type))
        if spotify_URI and URI_type:
            return spotify_URI, URI_type, tag_id
    elif tag_id is None and tag_id != last_tag_id:
        return None, None, None

    return None, None, last_tag_id
