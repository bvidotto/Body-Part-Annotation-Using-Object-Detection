"""
File: quadrange.py
Author: Benoît Vidotto
Date: Q1/Q2 2022
"""


import json
import numpy as np

with open("annotations.json", 'r') as fr:
	f = json.load(fr)

idx = 32
seg = f['annotations'][idx]['segmentation'][0]

bbox = f['annotations'][idx]['bbox']
print(bbox)
arr = []
minX = bbox[0]
arr.append(minX)
arr.append(seg[seg.index(minX)+1])
minY = bbox[1]
arr.append(seg[seg.index(minY)-1])
arr.append(minY)

maxX = bbox[2]+minX-1
arr.append(maxX)
arr.append(seg[seg.index(maxX)+1])
maxY = bbox[3]+minY-1
arr.append(seg[seg.index(maxY)-1])
arr.append(maxY)


f['annotations'][idx]['segmentation'] = [arr]

with open("annotations.json", 'w') as fw:
	json.dump(f, fw)