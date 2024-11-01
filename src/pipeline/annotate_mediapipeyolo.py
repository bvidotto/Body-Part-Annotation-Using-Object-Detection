"""
File: annotate_mediapipeyolo.py
Author: Benoît Vidotto
Date: Q1/Q2 2022
"""


import torch
import cv2
import mediapipe as mp
import numpy as np
import sys
from tqdm import tqdm
import os
import json
from statistics import mean


def preprocessing(file):
    with open(file, 'r') as f:
        data = json.load(f)

    categoryId={}
    for cat in data["categories"]:
            categoryId[cat["name"]]=cat["id"]
    return categoryId, data["info"], data["categories"], data["licenses"]

class image:
    def __init__(self, file, path):
        self.file_name = file
        self.cv2 = cv2.imread(path + '/' + file)
        self.height, self.width, _ = self.cv2.shape
        self.id = self.digitsOnly(file)
        self.ann = []
        self.score = 0

    def digitsOnly(self, txt):
        s = ''
        for char in txt:
            s+= char if char.isdigit() else ''
        return int(s)

    def xyxy2xywhNormalize(self, bbox, normX, normY):

        bbox[0] = bbox[0]*normX[0] + normX[1]
        bbox[2] = bbox[2]*normX[0] + normX[1]
        bbox[1] = bbox[1]*normY[0] + normY[1]
        bbox[3] = bbox[3]*normY[0] + normY[1]
        return [
            int(bbox[0]),
            int(bbox[1]),
            int(bbox[2] - bbox[0]),
            int(bbox[3] - bbox[1])
        ]

    def bboxHands(self, landmarks, name, normalize, categoryId, bpConf):
        try:
            if name=="lhand":
                hand = [15, 17, 19, 21]
                conf = [landmarks.pose_landmarks.landmark[k].visibility for k in hand]

                x = [coord.x for coord in landmarks.left_hand_landmarks.landmark]
                y = [coord.y for coord in landmarks.left_hand_landmarks.landmark]
                # conf = [landmarks.face_landmarks.landmark[k].visibility for k in hand]
            else:
                hand=[16, 18, 20, 22]
                conf = [landmarks.pose_landmarks.landmark[k].visibility for k in hand]

                x = [coord.x for coord in landmarks.right_hand_landmarks.landmark]
                y = [coord.y for coord in landmarks.right_hand_landmarks.landmark]
            for i in conf:
                if i <=bpConf:
                    return


        except:
            conf = [landmarks.pose_landmarks.landmark[k].visibility for k in hand]
            for i in conf:
                if i <=bpConf:
                    return

            x = [landmarks.pose_landmarks.landmark[k].x for k in hand]
            y = [landmarks.pose_landmarks.landmark[k].y for k in hand]
#"segmentation" : [[min(x), min(y), max(x), min(y), min(x), max(y), max(x), max(y)]],
        bbox=self.xyxy2xywhNormalize([min(x), min(y), max(x), max(y)], normalize[0], normalize[1])
        self.ann.append({
            "id" : self.ann[-1]["id"] +1,
            "image_id":self.id,
            "category_id":categoryId[name],
            "bbox":bbox,
            # "segmentation" : [[bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1], bbox[0], bbox[1]+bbox[3], bbox[0]+bbox[2], bbox[1]+bbox[3]]],
            "area":bbox[2]*bbox[3],
            "iscrowd":0
        })
        self.score+=mean(conf)

    def bboxFace(self, landmarks, name, normalize, categoryId, bpConf):
        face = [x for x in range(11)]
        try:
            conf = [landmarks.pose_landmarks.landmark[k].visibility for k in face]

            for i in conf:
                if i <=bpConf:
                    return

            x  = [coord.x for coord in landmarks.face_landmarks.landmark]
            y  = [coord.y for coord in landmarks.face_landmarks.landmark]

        except:
            conf = [landmarks.pose_landmarks.landmark[k].visibility for k in face]
            
            for i in conf:
                if i <=bpConf:
                    return

            x = [landmarks.pose_landmarks.landmark[k].x for k in face]
            y = [landmarks.pose_landmarks.landmark[k].y for k in face]

        bbox=self.xyxy2xywhNormalize([min(x), min(y), max(x), max(y)], normalize[0], normalize[1])
        self.ann.append({
            "id" : self.ann[-1]["id"] +1,
            "image_id":self.id,
            "category_id":categoryId[name],
            "bbox":bbox,
            # "segmentation" : [[bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1], bbox[0], bbox[1]+bbox[3], bbox[0]+bbox[2], bbox[1]+bbox[3]]],
            "area":bbox[2]*bbox[3],
            "iscrowd":0
        })
        self.score+=mean(conf)

    def bboxLimb(self, landmarks, bodypart, name, normalize, categoryId, bpConf):
        # try:
        conf = [landmarks.landmark[bodypart].visibility, landmarks.landmark[bodypart+2].visibility]
        for i in conf:
            if i <=bpConf:
                return
        x = landmarks.landmark[bodypart].x, landmarks.landmark[bodypart+2].x
        y = landmarks.landmark[bodypart].y, landmarks.landmark[bodypart+2].y

        bbox=self.xyxy2xywhNormalize([min(x), min(y), max(x), max(y)], normalize[0], normalize[1])

        # widen limbs that are too thin to be human
        if bbox[2] < 0.333*bbox[3]:
            width = 0.333*bbox[3]
            bbox[2] = width
            bbox[0] -= width/2
        
        if bbox[3] < 0.333*bbox[2]:
            height = 0.333*bbox[2]
            bbox[3] = height
            bbox[1] -= height/2

        self.ann.append({
            "id" : self.ann[-1]["id"] +1,
            "image_id":self.id,
            "category_id":categoryId[name],
            "bbox":bbox,
            # "segmentation" : [[bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1], bbox[0], bbox[1]+bbox[3], bbox[0]+bbox[2], bbox[1]+bbox[3]]],
            "area":bbox[2]*bbox[3],
            "iscrowd":0
        })
        self.score+=mean(conf)
        # except:
            # return

    def bboxTorso(self, landmarks, name, normalize, categoryId, bpConf):
        # try:
        torso = [11, 12, 23, 24]
        conf = [landmarks.landmark[k].visibility for k in torso]
        for i in conf:
            if i <=bpConf:
                return
        x = [landmarks.landmark[k].x for k in torso]
        y = [landmarks.landmark[k].y for k in torso]

        bbox=self.xyxy2xywhNormalize([min(x), min(y), max(x), max(y)], normalize[0], normalize[1])
        self.ann.append({
            "id" : self.ann[-1]["id"] +1,
            "image_id":self.id,
            "category_id":categoryId[name],
            "bbox":bbox,
            # "segmentation" : [[bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1], bbox[0], bbox[1]+bbox[3], bbox[0]+bbox[2], bbox[1]+bbox[3]]],
            "area":bbox[2]*bbox[3],
            "iscrowd":0
        })
        self.score+=mean(conf)
        # except:
            # return

    def bboxFoot(self, landmarks, foot, name, normalize, categoryId, bpConf):
        # try:
        conf = [landmarks.landmark[foot+k].visibility for k in [0, 2, 4]]

        for i in conf:
            if i <=bpConf:
                return
        x = [landmarks.landmark[foot+k].x for k in [0, 2, 4]]
        y = [landmarks.landmark[foot+k].y for k in [0, 2, 4]]

        bbox=self.xyxy2xywhNormalize([min(x), min(y), max(x), max(y)], normalize[0], normalize[1])
        self.ann.append({
            "id" : self.ann[-1]["id"] +1,
            "image_id":self.id,
            "category_id":categoryId[name],
            "bbox":bbox,
            # "segmentation" : [[bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1], bbox[0], bbox[1]+bbox[3], bbox[0]+bbox[2], bbox[1]+bbox[3]]],
            "area":bbox[2]*bbox[3],
            "iscrowd":0
        })
        self.score+=mean(conf)
        # except:
            # return

def keepGoodImages(threshold, images, path):
    cocoImg = []
    cocoAnn = []
    scores = []

    with open("scores.json", 'r') as f:
        scores = json.load(f)

    for image in images:
        scores.append(image.score)
        if float(image.score) >= float(threshold):
            cocoImg.append({ "id": image.id,
                    "width": image.width,
                    "height":image.height,
                    "file_name": image.file_name
                })
            cocoAnn = cocoAnn + image.ann
        else:
            print(path + "/" + image.file_name)
            os.remove(path + "/" + image.file_name)

    with open("scores.json", 'w') as f:
        json.dump(scores, f)

    return cocoImg, cocoAnn


def annotate(yoloConf, mpConf, bpConf, yoloModel, imagePath, categoriesJson, scoreThreshold):
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_holistic = mp.solutions.holistic

    categoryId, cocoInfo, cocoCat, cocoLic = preprocessing(categoriesJson)

    # Model
    model = torch.hub.load('ultralytics/yolov5', yoloModel)  # yolov5s, yolov5m, yolov5l, yolov5x, custom
    images = []
    annotatedImages = []

    annotationJson = imagePath + ".json"
    if os.path.exists(annotationJson):
        with open(annotationJson, 'r') as f:
            annotated = json.load(f)

        annotatedImages = [x["file_name"] for x in annotated["images"]]
    k=0
    nmFiles=len(os.listdir(imagePath))
    for file in tqdm(os.listdir(imagePath)):

        if file[-4:]!= ".jpg":
            continue
        if annotatedImages and file in annotatedImages:
            continue
        
        filepath = imagePath + '/' + file

    #______yolo_____
        # Inference
        yolo = model(filepath)
        # results.show()
        # Results
        df = yolo.pandas().xyxy[0]

    #______yolo_____

        imgInfo = image(file, imagePath)
        # cv2image = imgInfo.cv2
        # image_id = image.id

        for idx, row in df.iterrows(): # for each element detected by yolo
            if row['name']=='person' and row['confidence']>=yoloConf :
                bbox = [int(row['xmin']), int(row['ymin']), int(row['xmax'] - row['xmin']), int(row['ymax'] - row['ymin'])]

                imgInfo.ann.append({
                        "id" : 0 if (len(images)==0 or len(images[-1].ann) == 0) else images[-1].ann[-1]["id"]+1,
                        "image_id": imgInfo.id,
                        "category_id": categoryId["person"],
                        "bbox": bbox,
                        "area": bbox[3]*bbox[2]
                    })
                imgInfo.score += row["confidence"]
                with mp_holistic.Holistic(
                    static_image_mode=True,
                    model_complexity=2,
                    min_detection_confidence=mpConf) as holistic:

                    cropped = imgInfo.cv2[int(row['ymin']):int(row['ymax']), int(row['xmin']):int(row['xmax'])]
                    cropped_height, cropped_width, _ = cropped.shape

                    # Convert the BGR cropped to RGB before processing.
                    mpresults = holistic.process(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

                    normX = [cropped_width, float(row['xmin'])]
                    normY = [cropped_height , float(row['ymin'])]
                    normalize = (normX, normY)

                                        # limbs = [11, 12, 13, 14, 23, 24, 25, 26]
                    if mpresults.pose_landmarks:
                        for key, value in {"luarm":11, "llarm":13, "ruarm":12, "rlarm":14, "ruleg":24, "rlleg":26, "luleg":23, "llleg":25}.items():
                            imgInfo.bboxLimb(mpresults.pose_landmarks, value, key, normalize, categoryId, bpConf)
                            # bboxLimb(results, landmarks, bodypart, name, image_id, height, width, categoryId)
                        imgInfo.bboxTorso(mpresults.pose_landmarks, "torso", normalize, categoryId, bpConf)

                        imgInfo.bboxFoot(mpresults.pose_landmarks, 28, "rfoot", normalize, categoryId, bpConf)
                        imgInfo.bboxFoot(mpresults.pose_landmarks, 27, "lfoot", normalize, categoryId, bpConf)
                        imgInfo.bboxFace(mpresults, "head", normalize, categoryId, bpConf)
                    # if mpresults.left_hand_landmarks:
                        imgInfo.bboxHands(mpresults, "lhand", normalize, categoryId, bpConf)
                    # if mpresults.right_hand_landmarks:
                        imgInfo.bboxHands(mpresults, "rhand", normalize, categoryId, bpConf)

        if len(imgInfo.ann)>0:
            imgInfo.score = imgInfo.score/len(imgInfo.ann)
            images.append(imgInfo)
        else:
            os.remove(imagePath+"/"+imgInfo.file_name)


        if k%100==0 or k == nmFiles:
            cocoImg, cocoAnn = keepGoodImages(scoreThreshold, images, imagePath)
            # print(len(cocoImg))

            if not os.path.exists(annotationJson):
                coco = {
                    "info" : cocoInfo,
                    "licenses" : cocoLic,
                    "categories" : cocoCat,
                    "images" : cocoImg,
                    "annotations": cocoAnn
                }

                with open(annotationJson, 'w') as f:
                    json.dump(coco, f) #, indent = 4)
            else:
                with open(annotationJson, 'r') as f:
                    data = json.load(f)

                data["images"] = data["images"] + cocoImg
                data["annotations"] = data["annotations"] + cocoAnn

                with open(annotationJson, 'w') as f:
                    json.dump(data, f) #, indent = 4)
    
if __name__ == "__main__":

    if len(sys.argv)==1:
        print(f"python {sys.argv[0]} yoloConf mpConf bpConf [yolov5s, yolov5m, yolov5l, yolov5x, custom] imagesPath categoriesJson")
        quit()
    else:
        print(sys.argv)
        yoloConf = float(sys.argv[1]) # yolo confidence threshold
        mpConf = float(sys.argv[2]) # mediapipe confidence threshold
        bpConf = float(sys.argv[3])   # bodypart confidence or visibility
        yoloModel = sys.argv[4]
        imagePath = sys.argv[5]
        CategoriesJson = sys.argv[6]
        scoreThreshold = sys.argv[7]
    annotate(yoloConf, mpConf, bpConf, yoloModel, imagePath, categoriesJson, scoreThreshold)
