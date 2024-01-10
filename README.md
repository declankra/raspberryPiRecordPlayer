# raspberryPiRecordPlayer
tldr: A raspberry pi controlled spotify player connected to your spotify connect device

!!! Visit notion page for project details and setup: https://www.notion.so/declankramper/raspberryPiRecordPlayer-bc59312559bd4569a0f717fc6efae722?pvs=4 
 
NFC Record player main page: https://www.notion.so/declankramper/NFC-Record-Player-Build-bf95a606cc474c11a626b50821fb12d4?pvs=4

variation for playing through a sonos speaker: https://www.notion.so/declankramper/raspberryPiRecordPlayerSonos2-64432a48ffa44c0f861dc3d75144c6e3?pvs=4


**GENERAL OVERVIEW**

**what**
a “magic record player” device that plays music on a Spotify connected speaker when a song/playlist/album is placed on the record player

**how does device work?**
user places nfc tag on top of the reader → reader scans the id of the tag → python program will match the id with a spotify uri → make call to spotify api to play song on selected speaker

**disclaimer**: in order for playback to work, the output device always has to be connected to Spotify i.e. showing up on ‘Spotify Connect’ devices
    **how does that happen?**
    1. same wifi network
    2. device always stays “on/connected”
        or not, found work-around for amazon echo dot 4 device

### SCRIPTs
**authorize.py:** pre-work. uses manually provided spotify developer account credentials from .env  to get authorization code.

**getTokens.py:** pre-work. uses authorization code and spotify credentials to recieve a refresh token. saves the response to a json file with necessary variables for refreshTokens.py to function.

**tokens.json:** stores tokens and variables for refreshing tokens when needed

**refreshTokens.py:** makes request to api/token/ to get new access token. stores response in tokens.json. called by get_access_token() inside player.py

**player.py:** the powerhouse. infinite mainRun() logic checks tag id response and acts accordingly. if a new, valid tag is detected that is different from the last tag, it calls sound_settings() which facilitates the other functions and ensures that the track is played.

**idToMp3.py:** called by mainRun(). input is the last tag id. output is either (1) a new tag id and corresponding uri info or (2) none if no new tag is scanned. calls readNfcTag.js in read_nfc_tag(). 

**readNfcTag.js:** js file to read the response from the nfc card reader. output is error/none/uid.

**vinylCollection.json:** list of “records” with both tag ids and corresponding spotify uris. plus uri type.


### Dependencies and downloads required for program
- python3
    - `python3 —version:` Python 3.11.6
- node.js
    - `node —version:` v21.2.0
- npm
- requests (python dependency)
- nfc-pcsc js library for communicating with scanner (node.js dependency)
    - PC/SC Lite development libraries