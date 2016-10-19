#!/usr/bin/env python3

import requests

URL = 'http://172.17.0.2:/randomfile.bin'
DEST_FILE = 'randomfile.bin'
CHUNK_SIZE = 4096

with open(DEST_FILE, 'wb') as fd, requests.Session() as session:
    stream = session.get(URL, stream=True)
    for chunk in stream.iter_content(chunk_size=CHUNK_SIZE):
        fd.write(chunk)
