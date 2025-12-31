# Overview

**What**: a “magic record player” device that plays music on a Spotify connected speaker when a song/playlist/album is placed on the record player

**how does device work?**

user places nfc tag on top of the reader → reader scans the id of the tag → python program will match the id with a spotify uri → make call to spotify api to play song on selected speaker


### pi functionalities required

- connect to home wifi
    - username: Wavelength
    - password: meetyouthere82621
- upon powering on the pi…
    - auto-run player.py program (so it runs constantly)
    - auto-start the nfc reader and allow program files to access it

## Katie’s **Record Player**

**For Katie’s Spotify account**

1. Get Spotify credentials
    1. user: **kah.4**
    2. pass: **Flower200!**
2. Create Spotify developer account
    1. project name: **katieRecordPlayer**
    2. app description: **A raspberry pi powered record player to listen to the soundtrack of your memories**
3. Get developer credentials
    1. redirect uri: **http://localhost:8888/callback**
    2. client id: **497654396f2b4724b25afba2a14c2c75**
    3. client secret id: **ba0fdbe39a9a4c1fb7f6cd90f3326a06**

**For Katie’s Amazon account**

email/username: kahelliwell@gmail.com
password: Flower2000!


### **for Spotify connect devices:**

1. **download raspberry pi imager**
2. **option 1:** choose Raspberry PI OS ****(legacy, 32 bit) with **default, unset settings**
    1. CONNECT TO PI OVER WIFI USING WPA_CONFIG FILE
        1. if yes → use below
        2. if no → [option 2:](https://www.notion.so/Setting-up-a-Rasberry-Pi-Project-4017f3c0040045a2a15f10d37e6d5b05?pvs=21) restart with custom settings (same as sonos walkthrough)
3. **write card with blank settings** - no prefilled wifi or hostname
4. **unplug → replug card**
5. **Add SSH file**

```bash
touch /Volumes/bootfs/ssh
```

1. **setup wifi configuration:**
    1. add file wpa_supplicant.conf in root directory
        
        ```bash
        touch /Volumes/bootfs/wpa_supplicant.conf
        sudo nano /Volumes/bootfs/wpa_supplicant.conf
        
        ## **Save and exit:
        	•	Press Control + O to save.
        	•	Press Enter to confirm the filename.
        	•	Press Control + X to exit.**
        ```
        
    2. fill in with wifi details
        
        ```bash
        country=US
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        
        network={
            ssid="NETWORK-NAME" "Buckingham Palace"
            psk="NETWORK-PASSWORD" "Willsmells"
        }
        ```
        
        ```bash
        country=US
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        
        network={
            ssid="The Lighthouse"
            psk="Purdue22"
        }
        ```
        
        ```bash
        country=US
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        
        network={
            ssid="Wavelength"
            psk="meetyouthere82621"
        }
        ```
        
2. **first time connecting to pi over wifi:**
    1. put sd card back into raspberry pi
    2. plug into outlet using power micro usb port
    3. login remotely over wifi

```bash
//enter following command
ssh pi@YOUR.PI.IP.ADDRESS
ssh pi@10.0.0.114

// if error message after changed host key, enter:
ssh-keygen -R "NAME OF PI"
ssh-keygen -R "10.0.0.114" 
ssh-keygen -R "raspberrypi.local" 

//then reconnect

default password for pi user: raspberry
// yes, accept access
```

1. **update systems** 
    
    ```bash
    $ sudo apt update
    $ sudo apt full-upgrade
    ```
    

**option 2:** choose Raspberry PI OS ****(legacy, 32 bit) with **custom settings**

*follow same procedure as sonos version*

1. **choose Raspberry PI OS** (legacy, 32 bit) with custom settings
2. **setup general settings**
    1. set hostname
    2. set username & password
    3. connect to wifi
    4. set wireless LAN country: US
3. **services: check to enable ssh**
    
    ![Screenshot 2024-01-09 at 6.08.44 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/f8153f15-10d2-40c5-be98-42a368e5e86b/98e49051-fd7c-491d-96da-73dfa83062c3/Screenshot_2024-01-09_at_6.08.44_PM.png)
    
    ```bash
    hostname: **katiepi
    //**to connect
    if plugged in: ssh pi@**katiepi**.local
    if not: ssh pi@10.0.0.114
    //credentials
    username: pi
    password: raspberry -> use $passwd to change it (not needed)
    
    ```
    
4. **write settings to card sbfhost**
5. **first time connecting to pi over wifi**
    1. put sd card back into raspberry pi
    2. plug into outlet using power micro usb port
    3. login remotely over wifi
    
    ```bash
    //enter into terminal
    ssh pi@YOUR.PI.IP.ADDRESS
    ssh pi@10.0.0.114
    
    // if error message after changed host key, enter:
    ssh-keygen -R "10.0.0.114" 
    //then reconnect
    
    default password for pi user:raspberry
    // yes, accept access
    ```
    
6. **update systems**
    
    ```bash
    $ sudo apt update
    $ sudo apt full-upgrade
    ```

## Walkthrough

### Setup Package.json

1. go to project folder: `cd **/Users/macbook/Code/raspberryPiRecordPlayer**`
2. `npm init`
3. `npm install nfc-pcsc` 
4. save

### Get Spotify API credentials

1. create Spotify developer account
2. setup initial .env with Spotify client id, secret id, and redirect URI
3. run authorize.py
    1. capture authorization code
    2. update it in .env
4. run getTokens.py: sets up and updates the tokens.json file
5. Ready to go

### Setup pi

1. **initialize pi**
    1. see: [(2) **for Spotify connect devices:** ](https://www.notion.so/2-for-Spotify-connect-devices-8d9ef6cb24d44d8fa982755f6e436ea3?pvs=21) 
2. **connect to pi via ssh:** `ssh pi@10.0.0.114`
3. **Update Raspberry Pi:**`sudo apt update` `sudo apt full-upgrade`
- [did not work, but not a blocker] ***Install Python** ~~3.11.6~~ **3.9.7 using** `pyenv`*
    1. **Install the dependencies for pyenv**. Run the following command:
        
        ```bash
        sudo apt-get update; sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
        libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
        xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
        ```
        
    2. **Install pyenv**. You can use the following command to clone **`pyenv`** from its GitHub repository:
        
        ```bash
        git clone https://github.com/pyenv/pyenv.git ~/.pyenv
        ```
        
    3. **Set up the environment for pyenv**. Add the following lines to your **`.bashrc`** or **`.profile`** file:
        
        ```bash
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
        ```
        
    4. **Restart the Terminal** or source the **`.bashrc`** file to apply the changes:`source ~/.bashrc`
    5. **Install Python and set as global version: (stopped here)**
        - error i received
            
            **pi@katiepi**:**~ $** pyenv install 3.9.7
            
            Downloading Python-3.9.7.tar.xz...
            
            - > https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tar.xz
            
            Installing Python-3.9.7...
            
            patching file Misc/NEWS.d/next/Build/2021-10-11-16-27-38.bpo-45405.iSfdW5.rst
            
            patching file configure
            
            patching file configure.ac
            
            Traceback (most recent call last):
            
            File "<string>", line 1, in <module>
            
            File "/home/pi/.pyenv/versions/3.9.7/lib/python3.9/bz2.py", line 18, in <module>
            
            from _bz2 import BZ2Compressor, BZ2Decompressor
            
            ModuleNotFoundError: No module named '_bz2'
            
            **WARNING**: The Python bz2 extension was not compiled. Missing the bzip2 lib?
            
            Traceback (most recent call last):
            
            File "<string>", line 1, in <module>
            
            File "/home/pi/.pyenv/versions/3.9.7/lib/python3.9/curses/__init__.py", line 13, in <module>
            
            from _curses import *
            
            ModuleNotFoundError: No module named '_curses'
            
            **WARNING**: The Python curses extension was not compiled. Missing the ncurses lib?
            
            Traceback (most recent call last):
            
            File "<string>", line 1, in <module>
            
            File "/home/pi/.pyenv/versions/3.9.7/lib/python3.9/ctypes/__init__.py", line 8, in <module>
            
            from _ctypes import Union, Structure, Array
            
            ModuleNotFoundError: No module named '_ctypes'
            
            **WARNING**: The Python ctypes extension was not compiled. Missing the libffi lib?
            
            Traceback (most recent call last):
            
            File "<string>", line 1, in <module>
            
            ModuleNotFoundError: No module named 'readline'
            
            **WARNING**: The Python readline extension was not compiled. Missing the GNU readline lib?
            
            Traceback (most recent call last):
            
            File "<string>", line 1, in <module>
            
            File "/home/pi/.pyenv/versions/3.9.7/lib/python3.9/ssl.py", line 98, in <module>
            
            import _ssl             # if we can't import it, let the error propagate
            
            ModuleNotFoundError: No module named '_ssl'
            
            **ERROR**: The Python ssl extension was not compiled. Missing the OpenSSL lib?
            
            Please consult to the Wiki page to fix the problem.
            
            https://github.com/pyenv/pyenv/wiki/Common-build-problems
            
            **BUILD FAILED** (Raspbian 11 using python-build 2.3.35-7-g6e3b91a8)
            
            Inspect or clean up the working tree at /tmp/python-build.20240110013238.8123
            
            Results logged to /tmp/python-build.20240110013238.8123.log
            
            Last 10 log lines:
            
            Installing collected packages: setuptools, pip
            
            WARNING: Value for scheme.headers does not match. Please report this to <https://github.com/pypa/pip/issues/10151>
            
            distutils: /home/pi/.pyenv/versions/3.9.7/include/python3.9/setuptools
            
            sysconfig: /tmp/python-build.20240110013238.8123/Python-3.9.7/Include/setuptools
            
            WARNING: Value for scheme.headers does not match. Please report this to <https://github.com/pypa/pip/issues/10151>
            
            distutils: /home/pi/.pyenv/versions/3.9.7/include/python3.9/pip
            
            sysconfig: /tmp/python-build.20240110013238.8123/Python-3.9.7/Include/pip
            
            WARNING: The scripts pip3 and pip3.9 are installed in '/home/pi/.pyenv/versions/3.9.7/bin' which is not on PATH.
            
            Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
            
        
        ```bash
        pyenv install 3.9.7 ~~3.11.6~~
        //then
        pyenv global 3.9.7 ~~3.11.6~~
        ```
        
        **Clear Temporary Files (Optional):** If the build directory is cluttered due to previous failed attempts, you might want to clean it up before retrying:
        
        ```bash
        rm -rf /tmp/python-build.*
        ```
        
    6. **Verify version:** `python --version`
1. **Install Node.js v21.2.0**
    1. **Use the NodeSource repository to install the specific Node.js version required:**
        
        ```bash
        curl -fsSL https://deb.nodesource.com/setup_21.x | sudo -E bash -
        sudo apt-get install -y nodejs
        ```
        
    2. **Verify Node.js and npm version:** `node --version` `npm --version`

### Transfer files and install dependencies

1. **Proceed with File Transfer** on a different terminal window for macbook’s SSH: 
    1. navigate to: `cd /Users/macbook/Code`
    2. `scp -r raspberryPiRecordPlayer pi@10.0.0.114:/home/pi/`
    3. **Verify transfer** on pi’s SSH terminal:
        
        `cd /home/pi/raspberryPiRecordPlayer
        ls`
        
2. **Install Dependencies** using pi’s SSH terminal**:**
    1. **Python Dependencies:** `pip install requests`
    2. **Install Node.js Dependencies**: `npm install`
        1. Your project should have a package.json file which lists all Node.js dependencies. This command will read package.json and install all the listed packages.
    3. **Install NFC Library Dependencies**: 
        1. install the PC/SC Lite development libraries: `sudo apt-get install pcscd libpcsclite1 libpcsclite-dev`
        2. verify:
            
            ```bash
            // Start the PC/SC daemon:
            sudo systemctl enable pcscd
            sudo systemctl start pcscd
            // After instaling, restart:
            sudo systemctl restart pcscd
            ```
            

### Configure Auto-Start

1. **Auto-Run player.py:**
    - Use **`crontab`** to run **`player.py`** on startup.
    
    ```bash
    //Open the Crontab Configuration:
    	//Access the crontab file for the current user with the command:
    crontab -e
    //Add a Cron Job to Run on Reboot:
    	/Add the following line to the end of the crontab file:
    @reboot python /home/pi/raspberryPiRecordPlayer/player.py >> /home/pi/raspberryPiRecordPlayer/player.log 2>&1
    
    //This command will run player.py every time the Raspberry Pi reboots and will log the output to player.log in the project directory.
    ```
    
2. ***NFC Reader Setup [did not work]:***
    - Ensure the NFC reader starts automatically and is accessible to the program
    - Using crontab to Restart `pcscd` at Reboot:
        
        ```bash
        //Open the Crontab Configuration and edit:
        crontab -e 
        
        //Add a Cron Job to Restart pcscd on Reboot:
        	//Add the following line to the end of the crontab file:
        @reboot sudo systemctl restart pcscd
        
        //Save the changes and exit the editor
        ```
        

### Additional requirements

**When testing python script:**

`python3 /home/pi/raspberryPiRecordPlayer/player.py`

**Install `python-dotenv`**:

```bash
pip3 install python-dotenv
```

**Use absolute paths in code files**

*before transferring over on macbook’s SSH: `cd` `/Users/macbook/Code/raspberryPiRecordPlayer`*

1. in refreshTokens.py: when calling for tokens.json:
    
    '/home/pi/raspberryPiRecordPlayer/tokens.json’
    
    `scp refreshTokens.py pi@10.0.0.114:/home/pi/raspberryPiRecordPlayer/`
    
2. in idToMp3.py: when calling vinylCollection.json:
'/home/pi/raspberryPiRecordPlayer/vinylCollection.json’
    
    `scp idToMp3.py pi@10.0.0.114:/home/pi/raspberryPiRecordPlayer/`
    
3. in idToMp3.py: when calling subprocess for readNfcTag.js:
    
    '/home/pi/raspberryPiRecordPlayer/readNfcTag.js’
    `scp idToMp3.py pi@10.0.0.114:/home/pi/raspberryPiRecordPlayer/`
    
4. in player.py: when calling for tokens.json in read_tokens_from_file:
    
    '/home/pi/raspberryPiRecordPlayer/tokens.json’
    
    `scp player.py pi@10.0.0.114:/home/pi/raspberryPiRecordPlayer/`
    

**Manually install ‘nfc-pcsc’:** `npm install nfc-pcsc`