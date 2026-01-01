# NFC Record Player Debugging Session - December 31, 2025

## Initial Problem
- First NFC chip worked, then subsequent chips didn't work
- Raspberry Pi became unresponsive (SSH hanging, only ping worked)
- NFC reader showing "ghost" card IDs even when no card was present

---

## Issues Discovered & Fixed

### 1. pcscd Ghost Card Caching
**Problem:** The PC/SC daemon (pcscd) was caching old card IDs and returning them even when no card was present on the reader.

**Root Cause:** The old architecture spawned a new Node.js process every second to read NFC tags. When processes were killed (via timeout), pcscd's internal state became corrupted, causing it to return stale card data.

**Fix:** Refactored to use a persistent NFC reader process (see Architecture Changes below).

---

### 2. Wrong Spotify Device ID
**Problem:** Spotify API returning 404 errors - device not found.

**Root Cause:** The configured device ID `6026c126-8d57-4ed5-a173-a9240c99b43b_amzn_3` no longer existed. Amazon Echo device IDs can change when the Spotify skill is reinstalled or the device is reset.

**Fix:** Updated `.env` on the Pi with the correct "Everywhere" device ID:
```
SPTOTIFY_CONNECTED_DEVICE_ID_REAL=33b8fa83-f10e-41c8-83a2-9dba872793b9_amzn_3
SPTOTIFY_CONNECTED_DEVICE_ID_TRIMMED=33b8fa83-f10e-41c8-83a2-9dba872793b9
```

---

### 3. Echo Device Sleep Mode
**Problem:** Spotify API returning 404 even with correct device ID when Echo was asleep.

**Root Cause:** Amazon Echo devices go to sleep when not in use. Spotify's play endpoint fails if the device isn't "awake".

**Fix:** Added `wake_device()` function in `player.py` that calls the transfer playback endpoint before attempting to play:
```python
def wake_device(access_token, device_id):
    requests.put(
        'https://api.spotify.com/v1/me/player',
        headers=headers,
        json={'device_ids': [device_id], 'play': False}
    )
```

---

### 4. Log File Permissions
**Problem:** Log files weren't being written - service running as `pi` but logs owned by `root`.

**Fix:** `sudo chown pi:pi /home/pi/raspberryPiRecordPlayer/logs/*.log`

---

### 5. Python Output Buffering
**Problem:** Logs not appearing in real-time due to Python's stdout buffering.

**Fix:** Updated systemd service to use `python3 -u` for unbuffered output.

---

### 6. USB/pcscd Communication Failures
**Problem:** pcscd getting `LIBUSB_ERROR_TIMEOUT` when communicating with the NFC reader, even though the reader hardware was detecting cards (LED turning green).

**Root Cause:** USB power/communication instability on the Raspberry Pi. The dwc_otg USB driver on Pi can be unreliable with power-hungry devices.

**Symptoms in pcscd debug logs:**
```
ccid_usb.c:897:ReadUSB() read failed (1/5): -7 LIBUSB_ERROR_TIMEOUT
ifdhandler.c:202:CreateChannelByNameOrChannel() failed
```

**Workaround:** Unplug and replug the USB reader, then restart pcscd. For long-term stability, consider using a powered USB hub.

---

## Architecture Changes

### Old Architecture (Fragile)
```
Every 1 second:
  Python spawns new Node.js process
    → Node.js connects to pcscd
    → Reads card (or times out after 2s)
    → Node.js exits
    → Python kills process if timeout
```

**Problems:**
- 3,600+ process spawns per hour
- Each spawn opens/closes pcscd connection
- Timeout kills corrupt pcscd state
- Eventually causes ghost card reads or complete failure

### New Architecture (Robust)
```
On startup:
  Python spawns ONE persistent Node.js process
    → Node.js maintains continuous connection to pcscd
    → Outputs "CARD:<uid>" when card detected
    → Outputs "CARD_REMOVED" when card removed
  Python reads stdout via background thread
  Python polls current card state each second
```

**Benefits:**
- Single pcscd connection (no constant open/close)
- No zombie process accumulation
- Immediate card detection (event-driven)
- Auto-restart if Node.js process dies
- Proper card removal detection

---

## Files Changed

| File | Change |
|------|--------|
| `nfcReaderPersistent.js` | **NEW** - Persistent NFC reader that outputs card events |
| `idToMp3.py` | Refactored to use `NFCReader` class managing persistent process |
| `player.py` | Added `wake_device()` function, proper cleanup on exit |

---

## Testing Verification

After fixes, the system correctly:
- Detects NFC cards immediately when placed
- Plays the correct Spotify content
- Stops playback when card is removed
- Handles multiple different cards in succession
- Wakes sleeping Echo devices automatically
- Shows heartbeat logs every 30 seconds confirming reader is alive

---

## Remaining Considerations

1. **USB Stability:** If USB timeout errors recur, consider:
   - Using a powered USB hub
   - Disabling USB autosuspend: `echo -1 | sudo tee /sys/bus/usb/devices/1-1/power/autosuspend`

2. **Device ID Changes:** If Spotify stops working in the future, device IDs may have changed again. Check with:
   ```python
   requests.get('https://api.spotify.com/v1/me/player/devices', headers={'Authorization': f'Bearer {token}'})
   ```
