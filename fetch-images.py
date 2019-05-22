#!/usr/bin/env python3

import requests
import json
import sys
import os
import os.path

IMG_BASEURL='https://api.finna.fi'

OUTDIR='images'

if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)

for line in sys.stdin:
    rec = json.loads(line.strip())
    if 'images' not in rec or not rec['images']:
        continue  # skip if we don't have the image URL
    recid = rec['id']
    imgpath = os.path.join(OUTDIR, recid)
    if os.path.exists(imgpath) and os.path.getsize(imgpath) > 0:
        continue  # we already have the file
    imgurl = IMG_BASEURL + rec['images'][0]
    print("Downloading {} from {}...".format(recid, imgurl), file=sys.stderr)
    try:
        req = requests.get(imgurl)
    except:
        continue
    if len(req.content) < 10240:
        continue  # too small (just an icon?)
    with open(imgpath, 'wb') as imgf:
        imgf.write(req.content)

    
