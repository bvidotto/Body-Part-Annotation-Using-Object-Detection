"""
File: yoloviewer.py
Author: Benoît Vidotto
Date: Q1/Q2 2022
"""


import cv2
import numpy as np
import os, random

# file = random.choice(os.listdir("./sitcom scene/labels"))[:-4]
file = "001_1425c206"
with open(f'./dataset/labels/{file}.txt', 'r') as f:
	data = f.readlines()

im = cv2.imread(f'./dataset/images/{file}.jpg')
height, width, channels = im.shape

for line in data:
	sp1 = line.index(' ')
	sp2 = line.index(' ', sp1+1)
	sp3 = line.index(' ', sp2+1)
	sp4 = line.index(' ', sp3+1)
	w = float(line[sp3:sp4])
	h = float(line[sp4:])
	x = float(line[sp1:sp2])-w/2
	y = float(line[sp2:sp3])-h/2

	start = (int(x*width), int(y*height))
	end = (int((x + w)*width), int((y+h)*height))
	print(start)
	print(end)
	im = cv2.rectangle(im, start, end, (255, 0, 0), 2)
cv2.imshow('Image', im)
cv2.waitKey()