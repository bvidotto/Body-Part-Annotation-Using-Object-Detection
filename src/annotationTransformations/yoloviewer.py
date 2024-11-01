"""
File: yoloviewer.py
Author: Benoît Vidotto
Date: Q1/Q2 2022
"""


import cv2
import numpy as np
import os, random

file = random.choice(os.listdir("./labels"))[:-4]
with open(f'./labels/{file}.txt', 'r') as f:
	data = f.readlines()

im = cv2.imread(f'./images/{file}.jpg')
height, width, channels = im.shape

for line in data:
	sp1 = line.index(' ')
	sp2 = line.index(' ', sp1+1)
	sp3 = line.index(' ', sp2+1)
	sp4 = line.index(' ', sp3+1)
	start = (int(float(line[sp1:sp2])*width), int(float(line[sp2:sp3])*height))
	end = (int((float(line[sp1:sp2]) + float(line[sp3:sp4]))*width), int((float(line[sp2:sp3]) + float(line[sp4:]))*height))
	# print(start)
	# print(end)
	im = cv2.rectangle(im, start, end, (255, 0, 0), 2)
cv2.imshow('Image', im)
cv2.waitKey()