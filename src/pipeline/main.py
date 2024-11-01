"""
File: main.py
Author: Benoît Vidotto
Date: Q1/Q2 2022
"""


# from GoogleScrap import get_images_data
from dkdk import *
from annotate_mediapipeyolo import annotate
import os, shutil
import coco2yolo
import fileUtils


if __name__ == "__main__":

	query = "sitcom scene"
	minDBSize = 1000
	yoloPath = 'yolov5'
	dataset = "datasets/" + query
	yoloDataset = f"{yoloPath}/{dataset}"
	valDataset = "/home/VidottoB/data/pascalColor"
	valName = "pascalColor"


	# if os.path.exists(query):
		# shutil.rmtree(query)
	if os.path.exists(yoloDataset):
		shutil.rmtree(yoloDataset)
	if not os.path.exists(query):
		os.makedirs(query)

	while(len(os.listdir(query))<=minDBSize):
		downloaded = duckduckgo_search(os.getcwd(), query, query, max_results=20, img_layout = ImgLayout.All)
		print(f"downloaded = {downloaded}")
		if downloaded == 0: break
		annotate(0.0, 0.333, 0.333, "yolov5x", query, "categories.json", 0.6)
		# os.system('python cocoviewer.py -a x.json -i  \"sitcom scene\"')

	# # shutil.copytree("sitcom scene", "dataset")
	DBSize = len(os.listdir(query))
	coco2yolo.annotations(query +".json", yoloDataset)
	coco2yolo.config(query +".json", yoloPath, dataset)

	fileUtils.train_test_split(yoloDataset, DBSize, 0.3, 0.3)

	training = f"python {yoloPath}/train.py --img 640 --batch 16 --epochs 200  --data \"{query}.yaml\" --noval --cfg yolov5x.yaml"
	print(training)
	os.system(training)

	for i in range(5):
            runsTrain = f"{yoloPath}/runs/train"
            weights = f"{runsTrain}/{sorted(os.listdir(runsTrain))[-1]}/weights/best.pt"
            detect =f"python {yoloPath}/detect.py --weights {weights} --source \"{yoloDataset}/images/val\" --save-txt"
            print(detect)
            os.system(detect)
            runsDetect = f"{yoloPath}/runs/detect"
            newLabels = f"{runsDetect}/{sorted(os.listdir(runsDetect))[-1]}/labels"
            fileUtils.mixData(yoloDataset, DBSize, 0.3, 0.3, newLabels)


            training = f"python {yoloPath}/train.py --img 640 --batch 16 --epochs 200 --data \"{query}.yaml\" --weights {weights} --cfg yolov5x.yaml"
            print(training)
            os.system(training)



	weights = f"{runsTrain}/{sorted(os.listdir(runsTrain))[-1]}/weights/best.pt"
	config("categories.json", yoloPath, valDataset, valName)
	validation = "python yolov5/val.py --weights {weights} --data \"{valName}.yaml\" --save-json"
	print(validation)
	os.system(validation)