"""
File: matToCoco.py
Author: Benoît Vidotto
Date: Q1/Q2 2022
"""


import json
import pickle
import scipy.io as sc
import os
import shutil
import sys
from tqdm import tqdm
# from PIL import Image
try:
	annotations_path = sys.argv[4]
except:
	print("\n1st arg = path to annotations in mat format\n2nd arg = name of the output file (without extension)\n3rd arg = output file extension (json or pkl), default is .pkl\nExample: "+os.path.basename(__file__)+" ./annotations/val val json\n")
	exit()

if annotations_path == "-h" or annotations_path == "help":
	print("\n1st arg = path to annotations in mat format\n2nd arg = name of the output file (without extension)\n3rd arg = output file extension (json or pkl), default is .pkl\nExample: "+os.path.basename(__file__)+" ./annotations/val val json\n")
	exit()
outputfile = sys.argv[2]
# images_path = sys.argv[2]
annotations = sorted(os.listdir(annotations_path))
# images = os.listdir(images_path)
# input(annotations)

# for image in images:
# 	if image[:-4]+".mat" not in annotations:
# 		os.remove(images_path +"/"+ image)

# 	with Image.open(images_path + "/" + image) as img:
# 		img = img.convert("L")
# 		img.save(images_path + "/" + image)
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

with open("annotations_blank.pkl", 'rb') as fr:
	f = pickle.load(fr)

# sCategories_names = [x['name'] for x in f['categories']]
# sCategories = [x['supercategory'] for x in f['categories']]
k=0
# annotations = annotations[:annotations.index('2008_000776.mat')] 	#2008_000776
# annotations = annotations[annotations.index('2008_005794.mat'):] 	#2008_000776

for annotation in (pbar:=(tqdm(annotations))):

	filename = annotation[:-4]

	pbar.set_description("Processing %s" % filename)
	# print("\n" + filename)
	mat = sc.loadmat(annotations_path + "/" + filename)

	# with open(filename + ".json", 'r') as f:
	# 	f = json.load(f)

	# f['images'].append({
	#            "license": 1,
	#            "file_name": filename + ".jpg",
	#            "id": filename
	#        })

	height=len(mat['anno'][0][0][1][0][0][2])
	width=len(mat['anno'][0][0][1][0][0][2][0])

	f['images'].append({
	            "file_name": filename + ".jpg",
	            "id": int(filename.replace('_', '')),
	            "height" : height,
	            "width" : width
	        })


	# input(f"{height}x{width}")
	for obj in mat['anno'][0][0][1][0]:
		# obj[0] = tag
		# obj[1] = tag id
		# obj[2] = one-hot matrix
		
		tmp1 = []
		tmp2 = []
		tmp = []
		catId  = ""
		maxX = 0
		minX = width
		maxY = 0
		minY = height
		area = 0

		# for y in range(height): #375 = len(obj[2][2]) 		#this line
		# 	# input(f"{i}\n{sum(obj[2][i])}")
		# 	if sum(obj[2][y])!=0:
		# 		maxY = y if y > maxY else maxY
		# 		minY = y if y < minY else minY
		# 		for x in range(width):
		# 			if obj[2][y][x] == 1: 			#first pixel on this line to be 1
		# 				if obj[2][y][x-1]==0:
		# 					tmp.append(x)
		# 					tmp.append(y)
		# 					minX = x if x < minX else minX
		# 					area -= y
		# 			elif obj[2][y][x-1]==1: 			#last pixel on this line to be 1
		# 				tmp.append(x)
		# 				tmp.append(y)
		# 				maxX = x if x > maxX else maxX
		# 				area += y +1

		for x in range(width):
			for y in range(height):
				if obj[2][y][x] == 1 and obj[2][y-1][x]==0:
					tmp.append(x)
					tmp.append(y)
					minY = y if y < minY else minY
					minX = x if x < minX else minX
					maxX = x if x > maxX else maxX
					area -= y
				elif obj[2][y][x] == 0 and obj[2][y-1][x]==1:
					tmp.append(x)
					tmp.append(y)
					maxY = y if y > maxY else maxY
					area += y
		# for item in f['categories']:
		# 	if obj[0] == list(item.values())[0]:
		# 		catId = item['id'] #trouver l'index dans categories pour lequel le "name" == obj[0]
		# 		break
		# if obj[0][0] not in sCategories:
		# 	sCategories.append(obj[0][0])
		# 	catId = 1 if len(f['categories']) == 0 else f['categories'][-1]['id'] +1
		# 	f['categories'].append({"supercategory": obj[0][0], "id": catId,"name": obj[0][0]})
		# else: 
		catId = categories.index(obj[0][0])
			# for item in f['categories']:
			# 	if obj[0][0] == list(item.values())[0]:
			# 		catId = item['id'] #trouver l'index dans categories pour lequel le "name" == obj[0]
			# 		break

		# print("\n")
		# print(minX)
		# print(maxX)
		f["annotations"].append({
	            "segmentation": [tmp],
	            "area": area,
	            "iscrowd": 0,
	            "image_id": int(filename.replace('_', '')),
	            "bbox": [minX, minY, maxX - minX+1, maxY - minY+1], # [tmp[0], minX, tmp[-2] - tmp[0], maxX - minX],
	            "category_id": catId,
	        })

		if obj[0] == "person":
			if len(obj[3])==0:
				continue
			for subObj in obj[3][0]:
				# subObj[0] = tag
				# subObj[1] = one-hot matrix
				tmp = []
				catId  = ""
				maxX = 0
				minX = width
				maxY = 0
				minY = height
				area = 0

				for x in range(width):
					for y in range(height):
						if obj[2][y][x] == 1 and obj[2][y-1][x]==0:
							tmp.append(x)
							tmp.append(y)
							minY = y if y < minY else minY
							minX = x if x < minX else minX
							maxX = x if x > maxX else maxX
							area -= y
						elif obj[2][y][x] == 0 and obj[2][y-1][x]==1:
							tmp.append(x)
							tmp.append(y)
							maxY = y if y > maxY else maxY
							area += y

				# if subObj[0][0] not in sCategories_names:
				# 	sCategories_names.append(subObj[0][0])
				# 	catId = 1 if len(f['categories']) == 0 else f['categories'][-1]['id'] +1
				# 	f['categories'].append({"supercategory": subObj[0][0], "id": catId,"name": subObj[0][0]})
				# else:
				# 	for item in f['categories']:
				# 		if subObj[0][0] == list(item.values())[2]:
				# 			catId = item['id'] #trouver l'index dans categories pour lequel le "name" == obj[0]
				# 			break
				catId = categories.index(subObj[0][0])
				
				if len(tmp)==2:
					tmp.append(tmp[0]-1)
					tmp.append(tmp[1]-1)
					tmp.append(tmp[0]-1)
					tmp.append(tmp[1]+1)
					tmp.append(tmp[0]+1)
					tmp.append(tmp[1]-1)
					tmp.append(tmp[0]+1)
					tmp.append(tmp[1]+1)
					tmp.pop(0)
					tmp.pop(0)
					minX -= 1
					minY -= 1
					maxX += 1
					maxY += 1


				f["annotations"].append({
			            "segmentation": [tmp],
			            "area": area,
			            "iscrowd": 0,
			            "image_id": int(filename.replace('_', '')),
			            "bbox": [minX, minY, maxX - minX+1, maxY - minY+1], # [tmp[0], minX, tmp[-2] - tmp[0], maxX - minX],
			            "category_id": catId,
			        })
		

	k+=1
	if k % 100 == 0:
		with open(outputfile+".pkl", 'wb') as fw:
			pickle.dump(f, fw)
		# if k==500:
		# 	quit()	

with open(outputfile+".pkl", 'wb') as fw:
	pickle.dump(f, fw)

if sys.argv[3] == 'json':
	with open(outputfile + ".json", 'w') as fw:
		json.dump(f, fw)
# with open("annotations.json", 'w') as fw:
# 	json.dump(f, fw, indent=4)
# input("test")