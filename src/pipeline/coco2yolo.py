"""
File: coco2Yolo.py
Author: Benoît Vidotto
Date: Q1/Q2 2022
"""


import json
import yaml
import os, shutil

def bbox2yolo(bbox, w, h):
	return [
		(bbox[0]+bbox[2]/2)/w,
		(bbox[1]+bbox[3]/2)/h,
		bbox[2]/w,
		bbox[3]/h
	]

def config(cocoFile, yoloPath, yoloDataset, yoloDatasetName=''):

	if not yoloDatasetName:
		yoloDatasetName=cocoFile[:-5]

	with open(cocoFile, "r") as f:
		coco = json.load(f)

	names = [x["name"] for x in coco["categories"]]
	names.insert(0, "background")
	cfg = {
		"path" : yoloDataset,
		"train" : "images/train",
		"val" : "images/val",
		"nc" : len(names),
		"names" : names,
	}

	with open(yoloPath + "/data/" + yoloDatasetName +".yaml", "w") as f:
		yaml.dump(cfg, f)	
	return

def annotations(cocoFile, yoloDataset):

	query = cocoFile[:-5]
	labelsPath = yoloDataset + "/labels"

	os.makedirs(yoloDataset+"/images")
	for file in os.listdir(query):
		shutil.copy(query+"/"+file, yoloDataset+"/images/" + file)

	os.makedirs(labelsPath)

	with open(cocoFile, "r") as f:
		coco = json.load(f)

	imgIDs = {}
	for image in coco['images']:
		imgIDs[image["id"]] = {
			"width":image["width"],
			"height":image["height"],
			"file_name":image["file_name"]
		}

	yolo = {}
	print(len(coco['annotations']))
	for ann in coco['annotations']:
		image_id = ann["image_id"]
		file_name = imgIDs[image_id]["file_name"][:-4]
		width = imgIDs[image_id]["width"]
		height = imgIDs[image_id]["height"]
		bbox = bbox2yolo(ann["bbox"], width, height)
		bbox = [x if x <=1.0 else 1.0 for x in bbox]
		bbox = [x if x >=0.0 else 0.0 for x in bbox]

		if file_name not in yolo:
			yolo[file_name] = " "

		yolo[file_name] = yolo[file_name] + f"{ann['category_id']} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n"
	print(len(coco['images']))
	print(len(yolo))
	for image in coco["images"]:
		file_name = image['file_name'][:-4]
		if file_name not in yolo:
			yolo[file_name] = "  "
	print(len(yolo))
	# os.makedirs(labelsPath)
	for file, ann in yolo.items():
		with open(f"{labelsPath}/{file}.txt", 'w') as f:
			f.write(ann)

	return

# def config():

# 	return

# def coco2yolo(coco, labelsPath):


# 	return

	# with open(f"{labelsPath}/{file_name[:-4]}.txt", 'a') as f:
	# 	f.write(f"{ann["category_id"]} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")

if __name__ == "__main__":
	keyword = "sitcom scene"
	coco2yolo(keyword + ".json", keyword+"/labels")
