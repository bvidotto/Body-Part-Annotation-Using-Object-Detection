"""
File: fileUtils.py
Authors: Benoît Vidotto
Date: Q1/Q2 2022
"""


import os
import shutil
import random

def moveImagesLabels(imagePath, labelsPath, directory, threshold):
	while len(os.listdir(imagePath + "/" + directory)) < int(threshold):
		file = random.choice(os.listdir(imagePath))

		if file[-4:]=='.jpg':
			shutil.move(imagePath + "/" + file, imagePath + "/" + directory + "/" + file)
			#YOLO
			shutil.move(f"{labelsPath}/{file[:-4]}.txt", f"{labelsPath}/{directory}/{file[:-4]}.txt")


def train_test_split(yoloDataset, DBSize, perTrain, perVal):
	print("\nSplitting images into train and validation directories\n")

	imagePath = yoloDataset+"/images" 
	labelsPath = yoloDataset+"/labels"
	os.makedirs(imagePath + "/train")
	os.makedirs(labelsPath + "/train")
	os.makedirs(imagePath + "/val")
	os.makedirs(labelsPath + "/val")

	moveImagesLabels(imagePath, labelsPath, "train", perTrain*DBSize)
	moveImagesLabels(imagePath, labelsPath, "val", perVal*DBSize)

	# percentages = {"train" : perTrain, "val" : perVal}
	# for directory, percentage in percentages.items():
		# if not (os.path.exists(imagePath + "/" + dir)):

 		# while len(os.listdir(imagePath + "/" + directory)) < int(percentage*DBSize):
			# file = random.choice(os.listdir(imagePath))

			# if file[-4:]=='.jpg':
			# 	shutil.move(imagePath + "/" + file, imagePath + "/" + directory + "/" + file)
			# 	#YOLO
			# 	shutil.move(f"{labelsPath}/{file[:-4]}.txt", f"{labelsPath}/{directory}/{file[:-4]}.txt")
			# 	# shutil.move(labelsPath + "/" + file[:-4]+".txt", labelsPath + "/" + directory + "/" + file[:-4]+".txt")
	return

def mixData(yoloDataset, DBSize, perTrain, perVal, newLabels):

	imagePath = yoloDataset+"/images" 
	labelsPath = yoloDataset+"/labels" 

	for file in os.listdir(imagePath + "/train"): 		#move train out of its dir
		shutil.move(imagePath + "/train/" + file, imagePath + "/" + file)
		shutil.move(f"{labelsPath}/train/{file[:-4]}.txt", f"{labelsPath}/{file[:-4]}.txt")

#	for file in os.listdir(imagePath + "/val"):			# move val to train
#		if os.path.exists(f"{newLabels}/{file[:-4]}.txt"):
#			shutil.move(imagePath + "/val/" + file, imagePath + "/train/" + file)
#			shutil.copy(f"{newLabels}/{file[:-4]}.txt", f"{labelsPath}/train/{file[:-4]}.txt")
		# shutil.move(f"{labelsPath}/val/{file[:-4]}.txt", f"{labelsPath}/train/{file[:-4]}.txt") 			# old labels
#		else:
#			os.remove(imagePath + "/val/" + file)

	for file in os.listdir(newLabels):
		shutil.copy(f"{newLabels}/{file[:-4]}.txt", f"{labelsPath}/train/{file[:-4]}.txt")
		shutil.move(f"{imagePath}/val/{file[:-4]}.jpg", f"{imagePath}/train/{file[:-4]}.jpg")

	moveImagesLabels(imagePath, labelsPath, "val", perVal*DBSize)
	return
