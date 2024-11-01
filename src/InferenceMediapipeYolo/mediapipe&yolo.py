"""
File: mediapipe&yolo.py
Author: Benoît Vidotto
Date: Q1/Q2 2022
"""


import torch
import cv2
import mediapipe as mp
import numpy as np
import sys
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom

# Images
file = '2008_0000' + sys.argv[1] + '.jpg'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(file)
results.show()
# Results
df = results.pandas().xyxy[0]
# input(df)
print(df)
image = cv2.imread(file)
image_height, image_width, _ = image.shape
annotated_image = image.copy()
BG_COLOR = (192, 192, 192) # gray
mpresults={} #{<PoseLandmark.NOSE: 0>: 0, <PoseLandmark.LEFT_EYE_INNER: 1>: 0, <PoseLandmark.LEFT_EYE: 2>: 0, <PoseLandmark.LEFT_EYE_OUTER: 3>: 0, <PoseLandmark.RIGHT_EYE_INNER: 4>: 0, <PoseLandmark.RIGHT_EYE: 5>: 0, <PoseLandmark.RIGHT_EYE_OUTER: 6>: 0, <PoseLandmark.LEFT_EAR: 7>: 0, <PoseLandmark.RIGHT_EAR: 8>: 0, <PoseLandmark.MOUTH_LEFT: 9>: 0, <PoseLandmark.MOUTH_RIGHT: 10>: 0, <PoseLandmark.LEFT_SHOULDER: 11>: 0, <PoseLandmark.RIGHT_SHOULDER: 12>: 0, <PoseLandmark.LEFT_ELBOW: 13>: 0, <PoseLandmark.RIGHT_ELBOW: 14>: 0, <PoseLandmark.LEFT_WRIST: 15>: 0, <PoseLandmark.RIGHT_WRIST: 16>: 0, <PoseLandmark.LEFT_PINKY: 17>: 0, <PoseLandmark.RIGHT_PINKY: 18>: 0, <PoseLandmark.LEFT_INDEX: 19>: 0, <PoseLandmark.RIGHT_INDEX: 20>: 0, <PoseLandmark.LEFT_THUMB: 21>: 0, <PoseLandmark.RIGHT_THUMB: 22>: 0, <PoseLandmark.LEFT_HIP: 23>: 0, <PoseLandmark.RIGHT_HIP: 24>: 0, <PoseLandmark.LEFT_KNEE: 25>: 0, <PoseLandmark.RIGHT_KNEE: 26>: 0, <PoseLandmark.LEFT_ANKLE: 27>: 0, <PoseLandmark.RIGHT_ANKLE: 28>: 0, <PoseLandmark.LEFT_HEEL: 29>: 0, <PoseLandmark.RIGHT_HEEL: 30>: 0, <PoseLandmark.LEFT_FOOT_INDEX: 31>: 0, <PoseLandmark.RIGHT_FOOT_INDEX: 32>: 0}
# mpresults = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0, "28": 0, "29": 0, "30": 0, "31": 0, "32": 0}
mpresults = [0 for x in range(33)]
for idx, row in df.iterrows():
        # print(row['name'])
    # with mp_pose.Pose(
    # static_image_mode=True,
    # model_complexity=2,
    # min_detection_confidence=0.01) as pose:

    with mp_pose.Pose(
        model_complexity=2,
        # smooth_landmarks=True,
        static_image_mode=True,
        enable_segmentation=True,
        # refine_face_landmarks=False,
        min_detection_confidence=0.1) as pose:



        if row['name']=='person' and row['confidence']>0.8:
            cropped = image[int(row['ymin']):int(row['ymax']), int(row['xmin']):int(row['xmax'])]
            cropped_height, cropped_width, _ = cropped.shape
            # cv2.imshow(row['name'], image)
            # cv2.waitKey(0)
            # Convert the BGR cropped to RGB before processing.
            # cropped1 = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
            # cv2.imshow(file,cropped1)
            # cv2.waitKey(0)
            results = pose.process(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
            # results = pose.process(cropped)

            if not results.pose_landmarks:
                print('continue')
                continue
            print(
                f'Nose coordinates: ('
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * cropped_width}, '
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * cropped_height})'
            )
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
                landmark_list.landmark[k].x=(landmark_list.landmark[k].x*cropped_width+float(row['xmin']))/image_width
                landmark_list.landmark[k].y=(landmark_list.landmark[k].y*cropped_height+float(row['ymin']))/image_height

            mp_drawing.draw_landmarks(
                annotated_image,
                landmark_list,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
print(mpresults)
cv2.imshow(file,annotated_image)
cv2.waitKey(0)
        #     cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
        #     # Plot pose world landmarks.
        #     mp_drawing.plot_landmarks(
        #         results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)