"""
File: polygoncentroid.py
Author: Benoît Vidotto
Date: Q1/Q2 2022
"""


import numpy as np
import json
import pickle
import cv2
from math import sqrt



def polygon_area(xs, ys):
    """https://en.wikipedia.org/wiki/Centroid#Of_a_polygon"""
    # https://stackoverflow.com/a/30408825/7128154
    return 0.5 * (np.dot(xs, np.roll(ys, 1)) - np.dot(ys, np.roll(xs, 1)))

def polygon_centroid(xs, ys):
    """https://en.wikipedia.org/wiki/Centroid#Of_a_polygon"""
    xy = np.array([xs, ys])
    c = np.dot(xy + np.roll(xy, 1, axis=1),
               xs * np.roll(ys, 1) - np.roll(xs, 1) * ys
               ) / (6 * polygon_area(xs, ys))
    return c


with open("2008_000041.json", 'r') as fr:
      f = json.load(fr)

idx = 32
pol = f['annotations'][idx]['segmentation'][0]
bbox=f['annotations'][idx]['bbox']


im = cv2.imread(f'2008_000041.jpg')
height, width, channels = im.shape
im = cv2.rectangle(im, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (255, 0, 0), 2)

point = [bbox[0]+bbox[2]/2, bbox[1]+bbox[3]/2]
point = tuple([int(round(x,0)) for x in point])

print(point)

im=cv2.circle(im, point, radius=0, color=(0, 255, 0), thickness=3)

point = polygon_centroid(pol[0::2], pol[1::2])
point = tuple([int(round(x,0)) for x in point])

print(point)

im=cv2.circle(im, point, radius=0, color=(0, 255, 0), thickness=3)

cornersMax = {'qul': {'x':'', 'y':'', 'd':0},'qur':{'x':'', 'y':'', 'd':0}, 'qll':{'x':'', 'y':'', 'd':0}, 'qlr':{'x':'', 'y':'', 'd':0}}
cornersMin = {'qul': {'x':'', 'y':'', 'd':999},'qur':{'x':'', 'y':'', 'd':999}, 'qll':{'x':'', 'y':'', 'd':999}, 'qlr':{'x':'', 'y':'', 'd':999}}

def assignCorner(quadrant, j):
      assignCornerMax(quadrant, j)
      assignCornerMin(quadrant, j)

def assignCornerMax(quadrant, j):
      cornersMax[quadrant]={'x':pol[j], 'y':pol[j+1], 'd':dist} if dist > cornersMax[quadrant]['d'] else cornersMax[quadrant]

def assignCornerMin(quadrant, j):
      cornersMin[quadrant]={'x':pol[j], 'y':pol[j+1], 'd':dist} if dist < cornersMin[quadrant]['d'] else cornersMin[quadrant]

for i in range(0,len(pol),2):
      dist = sqrt((pol[i] - point[0])**2 + (pol[i+1] - point[1])**2 )         #distance between point and centroid
      if pol[i]>point[0]:
            if pol[i+1]<point[1]:   #upper left quadrant
                  assignCorner('qul', i)
            else:                   #upper right quadrant
                  assignCorner('qur', i)
      if pol[i]<=point[0]:
            if pol[i+1]<point[1]:   #lower left quadrant
                  assignCorner('qll', i)
            else:                   #lower right quadrant
                  assignCorner('qlr', i)

# for item in corners:
#       im=cv2.circle(im, (corners[item]['x'], corners[item]['y']), radius=0, color=(0, 0, 255), thickness=1)

im=cv2.line(im, (cornersMax['qul']['x'], cornersMax['qul']['y']), (cornersMax['qll']['x'], cornersMax['qll']['y']), color=(0, 255, 0), thickness=1)
im=cv2.line(im, (cornersMax['qll']['x'], cornersMax['qll']['y']), (cornersMax['qlr']['x'], cornersMax['qlr']['y']), color=(0, 255, 0), thickness=1)
im=cv2.line(im, (cornersMax['qlr']['x'], cornersMax['qlr']['y']), (cornersMax['qur']['x'], cornersMax['qur']['y']), color=(0, 255, 0), thickness=1)
im=cv2.line(im, (cornersMax['qur']['x'], cornersMax['qur']['y']), (cornersMax['qul']['x'], cornersMax['qul']['y']), color=(0, 255, 0), thickness=1)

im=cv2.line(im, (cornersMin['qul']['x'], cornersMin['qul']['y']), (cornersMin['qll']['x'], cornersMin['qll']['y']), color=(255,0, 0), thickness=1)
im=cv2.line(im, (cornersMin['qll']['x'], cornersMin['qll']['y']), (cornersMin['qlr']['x'], cornersMin['qlr']['y']), color=(255,0, 0), thickness=1)
im=cv2.line(im, (cornersMin['qlr']['x'], cornersMin['qlr']['y']), (cornersMin['qur']['x'], cornersMin['qur']['y']), color=(255,0, 0), thickness=1)
im=cv2.line(im, (cornersMin['qur']['x'], cornersMin['qur']['y']), (cornersMin['qul']['x'], cornersMin['qul']['y']), color=(255,0, 0), thickness=1)




for i in range(0,len(pol),2):
      dist = sqrt((pol[i] - point[0])**2 + (pol[i+1] - point[1])**2 )         #distance between point and centroid
      if pol[i]>point[0]:
            if pol[i+1]<point[1]:   #upper left quadrant
                  assignCorner('qul', i)
            else:                   #upper right quadrant
                  assignCorner('qur', i)
      if pol[i]<=point[0]:
            if pol[i+1]<point[1]:   #lower left quadrant
                  assignCorner('qll', i)
            else:                   #lower right quadrant
                  assignCorner('qlr', i)

# for item in corners:
#       im=cv2.circle(im, (corners[item]['x'], corners[item]['y']), radius=0, color=(0, 0, 255), thickness=1)

arr = []
minX = bbox[0]
arr.append(minX)
arr.append(pol[pol.index(minX)+1])
minY = bbox[1]
arr.append(pol[pol.index(minY)-1])
arr.append(minY)

maxX = bbox[2]+minX-1
arr.append(maxX)
arr.append(pol[pol.index(maxX)+1])
maxY = bbox[3]+minY-1
arr.append(pol[pol.index(maxY)-1])
arr.append(maxY)
for i in range(0,len(arr),2):
      im=cv2.line(im, (arr[i-8], arr[i+1-8]), (arr[i+2-8], arr[i+3-8]), color=(0, 0, 255), thickness=1)

im = cv2.resize(im, (im.shape[1]*2, im.shape[0]*2))
cv2.imshow('Image', im)
cv2.waitKey()


# print(polygon_centroid(xs=[0, 1, 1, 0], ys=[0, 0, 1, 1]),
#       'expect: [.5, .5]')
# print(polygon_centroid(xs=[0, 0, 2], ys=[1, -1, 0]),
#       'expect: [2/3, 0]')
# print(polygon_centroid(xs=[0, 0, 2], ys=[-1, 1, 0]),
#       'expect: [2/3, 0]')

# # https://wolfram.com/xid/0e5bspgmqyj9a5-cfx5ps
# print(polygon_centroid(xs=[0, 1, 1.5, 1, 0, -.5], ys=[0, 0, .5, 1, 1, .5]),
#       'expect: [.5, .5]')