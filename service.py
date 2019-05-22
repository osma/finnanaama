#!/usr/bin/env python

import os
import os.path
import urllib.parse
import json
import numpy
import face_recognition
import PIL
from flask import Flask, render_template, jsonify, request, redirect

app = Flask(__name__)
faces = numpy.load('faces.npy')
encodings = numpy.array([face[2] for face in faces])
records = {}

FINNA_BASE_URL = 'https://finna.fi'

RECORDDIR = 'records'

MAXDIM = 2048

for recf in os.listdir(RECORDDIR):
    with open(os.path.join(RECORDDIR, recf)) as recs:
        for line in recs:
            rec = json.loads(line)
            records[rec['id']] = rec

def make_record(recid, bbox, distance):
    rec = records[recid]
    ret = {
        'id': recid,
        'location': bbox,
        'imgurl': FINNA_BASE_URL + rec['images'][0],
        'pageurl': FINNA_BASE_URL + '/Record/' + urllib.parse.quote(recid),
        'title': rec.get('title', ''),
        'authors': rec.get('nonPresenterAuthors', None),
        'buildings': rec['buildings'][0]['translated'],
        'distance': distance
    }
    if 'year' in rec:
        ret['year'] = rec['year']
    return ret

def find_similar(file_stream):
    img = PIL.Image.open(file_stream)
    img = img.convert('RGB')
    scale = None
    if img.height > MAXDIM or img.width > MAXDIM:
        origheight = img.height
        img.thumbnail((MAXDIM, MAXDIM))
        scale = origheight / img.height
    img = numpy.array(img)
    face_locations = face_recognition.face_locations(img)
    if not face_locations:
        return None
    input_encodings = face_recognition.face_encodings(img, face_locations)
    face_encoding = input_encodings[0]
    if scale:
        face_locations = [[int(loc * scale) for loc in location] for location in face_locations]
    face_location = face_locations[0]
    distances = face_recognition.face_distance(encodings, face_encoding)
    ranking = distances.argsort()[:10]
    return {'location': face_location,
            'similar': [make_record(faces[idx][0], faces[idx][1], distances[idx])
                        for idx in ranking]}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/similar', methods=['POST'])
def similar():
    if 'imagefile' not in request.files:
        return redirect('/')
    
    imagefile = request.files['imagefile']
    return jsonify(find_similar(imagefile))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
