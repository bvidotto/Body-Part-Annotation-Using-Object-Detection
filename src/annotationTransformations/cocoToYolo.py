"""
File: cocoToYolo.py
Author: Benoît Vidotto
Date: Q1/Q2 2022
"""


import pickle
from tqdm import tqdm
import scipy.io as sc

categories = ['aeroplane',
'bicycle',
'bird',
'boat',
'bottle',
'bus',
'car',
'cat',
'chair',
'cow',
'dog',
'horse',
'motorbike',
'person',
'hair',
'head',
'lear',
'lebrow',
'leye',
'lfoot',
'lhand',
'llarm',
'llleg',
'luarm',
'luleg',
'mouth',
'neck',
'nose',
'rear',
'rebrow',
'reye',
'rfoot',
'rhand',
'rlarm',
'rlleg',
'ruarm',
'ruleg',
'torso',
'pottedplant',
'sheep',
'sofa',
'table',
'train',
'tvmonitor']

with open(r'C:\Users\bevid\Documents\ProjetTFE\S5\annotations100.pkl', 'rb') as f:
	data = pickle.load(f)

dcat = {}
for cat in data['categories']:
	dcat[cat['id']]=cat['name']

# print(dcat)

mat_path = r"C:\Users\bevid\Documents\ProjetTFE\S4\Annotations"
cat=''

for anno in tqdm(data['annotations']):
	file = anno['image_id']
	mat = sc.loadmat(mat_path + "/" + file+".mat")
	height=len(mat['anno'][0][0][1][0][0][2])
	# print(height)
	width=len(mat['anno'][0][0][1][0][0][2][0])
	# input(width)
	# cat = dcat[anno['category_id']]
	bbox=['', '', '', '']
	bbox[0::2]=[round(x/width, 4) for x in anno['bbox'][0::2]]
	bbox[1::2]=[round(x/height, 4) for x in anno['bbox'][1::2]]

	with open(f"./AnnoYolo/{file}.txt", 'a+') as f:
		f.write(f"{categories.index(dcat[anno['category_id']])} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")
	# input('wait')
