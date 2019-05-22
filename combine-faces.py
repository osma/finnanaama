#!/usr/bin/env python

import os
import os.path
import numpy
import json

FACEDIR='faces'

faces = []

datafiles = os.listdir(FACEDIR)
files_with_faces = 0

print("Combining {} data files".format(len(datafiles)))

for fn in datafiles:
    with open(os.path.join(FACEDIR, fn)) as f:
        has_face = False
        for line in f:
            has_face = True
            row = json.loads(line)
            faces.append([row['id'], row['location'], numpy.array(row['encoding'])])
        if has_face:
            files_with_faces += 1

print("Found {} faces in {} data files, writing dump".format(len(faces), files_with_faces))

numpy.save('faces', faces)
