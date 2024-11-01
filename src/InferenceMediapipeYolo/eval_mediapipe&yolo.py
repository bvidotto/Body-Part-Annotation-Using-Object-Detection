"""
File: eval_mediapip&yolo.py
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
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
# mp_holistic = mp.solutions.holistic

# annotations = sus.argv[4]
# Model
model = torch.hub.load('ultralytics/yolov5', sys.argv[1])  # yolov5s yolov5m, yolov5l, yolov5x, custom
mpresults = [0 for x in range(33)] # number of connections in mediapipe

for file in tqdm(os.listdir(sys.argv[2])):
    if file[-4:]!= ".jpg":
        continue
    # Images
    # file = '2008_0000' + sys.argv[1] + '.jpg'  # or file, Path, PIL, OpenCV, numpy, list
    filepath = sys.argv[2] + '/' + file
    # print(filepath)
    # Inference
    results = model(filepath)
    # results.show()
    # Results
    df = results.pandas().xyxy[0]

    image = cv2.imread(filepath)
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    BG_COLOR = (192, 192, 192) # gray

    for idx, row in df.iterrows():
            # print(row['name'])
        # with mp_pose.Pose(
        # static_image_mode=True,
        # model_complexity=2,
        # min_detection_confidence=0.01) as pose:
        print(row)
        with mp_pose.Pose(
            model_complexity=2,
            # smooth_landmarks=True,
            static_image_mode=True,
            enable_segmentation=True,
            min_detection_confidence=0.5) as pose:



            if row['name']=='person':
                cropped = image[int(row['ymin']):int(row['ymax']), int(row['xmin']):int(row['xmax'])]
                cropped_height, cropped_width, _ = cropped.shape
                # cv2.imshow(row['name'], image)
                # cv2.waitKey(0)
                # Convert the BGR cropped to RGB before processing.
                results = pose.process(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

                if not results.pose_landmarks:
                    # print('continue')
                    continue
                # print(
                #     f'Nose coordinates: ('
                #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * cropped_width}, '
                #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * cropped_height})'
                # )

                # Draw segmentation on the image.
                # To improve segmentation around boundaries, consider applying a joint
                # bilateral filter to "results.segmentation_mask" with "image".
                # condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
                # bg_image = np.zeros(cropped.shape, dtype=np.uint8)
                # bg_image[:] = BG_COLOR
                # annotated_image = np.where(condition, annotated_image, bg_image)

                # Draw pose landmarks on the image.
                landmark_list = results.pose_landmarks
                g=0

                for k in mp_pose.PoseLandmark:
                    if landmark_list.landmark[k].x < 1 and landmark_list.landmark[k].y < 1:
                        mpresults[k]+=1
                        # landmark_list.landmark[k].x=(landmark_list.landmark[k].x*cropped_width+float(row['xmin']))/image_width
                        # landmark_list.landmark[k].y=(landmark_list.landmark[k].y*cropped_height+float(row['ymin']))/image_height

                mp_drawing.draw_landmarks(
                    annotated_image,
                    landmark_list,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # cv2.imshow(file,annotated_image)
    # cv2.waitKey(0)
        #     cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
        #     # Plot pose world landmarks.
        #     mp_drawing.plot_landmarks(
        #         results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
print(mpresults)