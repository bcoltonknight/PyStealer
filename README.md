# PyStealer
A kinda messy Python infostealer I made for fun on and off over the course of a few weeks. A lot of the code is based on existing open source tooling that has been published online. The main original implementation is the WinSCP decrypter.

To set up your environment just run ``pip install -r requirements.txt`` and in order to set up an actual payload you run ```python builder.py``` which will create an interactive builder to create a dropper binary.

## Scraped Data:
* Discord Token/Account Information
* WinSCP saved login
* Chromium based saved browser information
* OBS Stream keys
* WPA Saved passwords