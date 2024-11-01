"""
File: result.py
Author: Benoît Vidotto
Date: Q1/Q2 2022
"""


mp2c = {0 : 27, 1 : '', 2 : 18, 3 : '', 4 : '', 5 : 30, 6 : '', 7 : 16, 8 : 28, 9 : 25, 10 : 25, 11 : [], 12 : , 13 : , 14 : , 15 : , 16 : , 17 : , 18 : , 19 : , 20 : , 21 : , 22 : , 23 : , 24 : , 25 : , 26 : , 27 : , 28 : , 29 : , 30 : , 31 : }

mpresults = [2755, 2755, 2752, 2750, 2756, 2758, 2758, 2749, 2758, 2756, 2757, 2648, 2699, 2331, 2461, 2208, 2356, 2104, 2266, 2191, 2308, 2250, 2356, 1979, 1993, 1531, 1670, 1198, 1226, 1127, 1144, 960, 987]


c2mp = {16:[7], 18:[2], 19:[27, 29, 31], 20:[15, 17, 19, 21], 21:[13, 15], 22: [25, 27], 23:[11, 13], 24:[23, 27], 25:[9, 10], 27:[0], 28:[8], 30:[5], 31:[28, 30, 32], 32:[15, 18, 20, 22], 33:[14, 16], 34:[26, 28], 35:[12, 14], 36:[24, 26], 37:[11, 12, 24, 23]}
import json
with open("train.json", "r") as f:
	data = json.load(f)
cnt=[0 for x in range(len(data["categories"]))]
for anno in data["annotations"]:
	cnt[anno["category_id"]]+=1

# cnt = [599, 518, 837, 691, 869, 417, 1502, 795, 2013, 388, 1005, 538, 509, 6830, 4646, 6442, 2388, 3032, 3610, 1996, 3228, 3875, 2832, 4325, 3351, 4022, 3183, 4387, 2284, 2965, 3524, 1971, 3265, 3894, 2743, 4332, 3322, 6443, 706, 481, 467, 510, 429, 575]

# results2c=[0 for x in range(len(categories))]
c2mp = {16:[7], 18:[2], 19:[27, 29, 31], 20:[15, 17, 19, 21], 21:[13, 15], 22: [25, 27], 23:[11, 13], 24:[23, 27], 25:[9, 10], 27:[0], 28:[8], 30:[5], 31:[28, 30, 32], 32:[15, 18, 20, 22], 33:[14, 16], 34:[26, 28], 35:[12, 14], 36:[24, 26], 37:[11, 12, 24, 23]}
mpresults = [2755, 2755, 2752, 2750, 2756, 2758, 2758, 2749, 2758, 2756, 2757, 2648, 2699, 2331, 2461, 2208, 2356, 2104, 2266, 2191, 2308, 2250, 2356, 1979, 1993, 1531, 1670, 1198, 1226, 1127, 1144, 960, 987]
results2c=[0 for x in range(43)]
for key, value in c2mp.items():
	if len(value)==1:
		results2c[key]=mpresults[value[0]]
	else:
		results2c[key] = min([mpresults[x] for x in value])
		# vals=[]
		# for each in value:
		# 	vals.append(mpresults[each])

# results2c = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2749, 0, 2752, 960, 2104, 2208, 1198, 2331, 1198, 2756, 0, 2755,2758, 0, 2758, 987, 2208, 2356, 1226, 2461, 1670, 1979, 0, 0, 0,0, 0, 0]
															# lear    leye  lfoot lhand llarm llleg luam luleg mouth    nose rear     reye  rfoot rhand rlarm rlleg ruarm ruleg torso
acc=[]
for i in range(len(cnt)):
	if results2c[i]!=0:
		acc.append(results2c[i]/cnt[i])

avg = sum(acc)/len(acc) # = 62.35%
# acc =  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.1511725293132329, 0.0, 0.7623268698060942, 0.48096192384769537, 0.6517967781908303, 0.5698064516129032, 0.4230225988700565, 0.5389595375722543, 0.357505222321695, 0.6852312282446544, 0.0, 0.627991793936631, 1.2075306479859895, 0.0, 0.782633371169126, 0.5007610350076104, 0.6762633996937213, 0.6050333846944016, 0.44695588771418154, 0.5680978762696214, 0.5027092113184829, 0.30715505199441256, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# acc = [1.1511725293132329, 0.7623268698060942, 0.48096192384769537, 0.6517967781908303, 0.5698064516129032, 0.4230225988700565, 0.5389595375722543, 0.357505222321695, 0.6852312282446544, 0.627991793936631, 1.2075306479859895, 0.782633371169126, 0.5007610350076104, 0.6762633996937213, 0.6050333846944016, 0.44695588771418154, 0.5680978762696214, 0.5027092113184829, 0.30715505199441256]
#		lear				 leye 				 lfoot 				  lhand 			  llarm 			  llleg 			   luam   			  luleg 			mouth    			nose 				rear     			reye  				rfoot 				rhand 				rlarm 				rlleg 				ruarm 				ruleg 				torso
categories = ['aeroplane',
1'bicycle',
2'bird',
3'boat',
4'bottle',
5'bus',
6'car',
7'cat',
8'chair',
9'cow',
10'dog',
11'horse',
12'motorbike',
13'person',
14'hair',
15'head',
16'lear',
17'lebrow',
18'leye',
19'lfoot',
20'lhand',
21'llarm',
22'llleg',
23'luarm',
24'luleg',
25'mouth',
26'neck',
27'nose',
28'rear',
29'rebrow',
30'reye',
31'rfoot',
32'rhand',
33'rlarm',
34'rlleg',
35'ruarm',
36'ruleg',
37'torso',
38'pottedplant',
39'sheep',
40'sofa',
41'table',
42'train',
43'tvmonitor']

class_names : ['aeroplane',
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

# 13'person',
# 14'hair',
# 15'head',
# 16'lear', = 7
# 17'lebrow',
# 18'leye', = 2
# 19'lfoot', = 29 27 31 or
# 20'lhand', 15 21 17 19 or
# 21'llarm', 13 & 15 and
# 22'llleg', 25 & 27 and
# 23'luarm', 11 & 13 and
# 24'luleg', 23 & 27 and
# 25'mouth', = 9 = 10 or
# 26'neck',
# 27'nose', = 0
# 28'rear', = 8
# 29'rebrow',
# 30'reye', = 5
# 31'rfoot', 28 32 30 or
# 32'rhand', 16 18 20 22 or
# 33'rlarm', 14 & 16 and
# 34'4rlleg', 26 & 28 and
# 35'ruarm', 12 & 14 and
# 36'ruleg', 24 & 26 and
# 37'torso', 24 23 12 11 and