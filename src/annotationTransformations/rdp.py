"""
File: rdp.py
Author: Benoît Vidotto
Date: Q1/Q2 2022
"""


from rdp.__init__ import rdp
import json
import numpy as np

with open("annotations.json", 'r') as fr:
	f = json.load(fr)

arr = f['annotations'][31]['segmentation']



length = len(arr[0])
print(length)
arr=np.array(arr[0]).reshape(int(length/2), 2).tolist()

arr2 = arr[int(length/2):]
arr2.reverse()
arr1 = arr[:int(length/2)] 
# arr = arr[:int(length/2)] + arr2

# arr=np.array(arr[0]).reshape(int(length/2), 2).tolist()

# arr2=[]
# arr3 = []
# for i in range(len(arr)):
#     if i%2==0:
#        arr2.append(arr[i])
#     else:
#        arr3.append(arr[i])
# arr = arr2 + arr3


# mask = rdp(arr, epsilon=10, algo="iter", return_mask=True)

# input(mask)
# print(mask)
# arr = arr[mask]
# length = len(arr)
# arr = [np.reshape(arr, int(length*2)).tolist()]
ep = 30
# arr1 = rdp(arr1, epsilon=ep, algo="iter", return_mask=False)
# arr2 = rdp(arr2, epsilon=ep, algo="iter", return_mask=False)

# arr = arr1+arr2
arr = rdp(arr, epsilon=ep, algo="iter", return_mask=False)
length = len(arr)
arr = [np.reshape(arr, int(length*2)).tolist()]

print(len(arr[0]))

x = input("ok ? ")


f['annotations'][31]['segmentation'] = arr

with open("annotations.json", 'w') as fw:
	json.dump(f, fw)

# arr = np.array([1, 1, 2, 2, 3, 3, 4, 4]).reshape(4, 2)
# mask = rdp(arr, algo="iter", return_mask=True)
# print(mask)
# print(arr[mask])