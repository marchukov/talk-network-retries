#!/usr/bin/env python3

# DEMO ONLY. DANGEROUS FOR YOUR MEMORY. DO NOT REPEAT THIS AT HOME.

import requests

URL = 'http://172.17.0.2/2gbfile.bin'
DEST_FILE = '2gbfile.bin'

with open(DEST_FILE, 'wb') as fd:
    r = requests.get(URL)
    r.raise_for_status()
    fd.write(r.content)
