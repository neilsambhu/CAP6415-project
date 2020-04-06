import numpy as np
import os, glob
from enum import Enum

dir_I3D = "./bf_kinetics_feat/"
dir_labels = "./PatternTheory_WACV_Original/PatternTheory_WACV_Original/S1_PreProcessFiles/"

# class Actions(Enum):
# 	put=0
	# cut=0
	# walk_in
	# put
	# ","spoon","peel","stir","walk_out", "smear","squeeze", "butter", "pour", "fry", "crack", "take", "add"]

def LoadData():
	x, y = list(), list()
	for feature in os.listdir(dir_labels):
		featureSplit = feature.split('_')
		if len(featureSplit) > 1:
			# print(featureSplit)
			# replace 'salad' with 'salat'
			if featureSplit[2] == 'salad':
				featureSplit[2] = 'salat'
			filePath_x = os.path.join(dir_I3D,
				featureSplit[1] + '_' + 
				featureSplit[3] + '_' +
				featureSplit[1] + '_' + 
				featureSplit[2] + '.npy')
			if os.path.exists(filePath_x):
				# np.load(filePath_x)
				# y.append()
				print(f'{filePath_x}')
			else:
				print(f'File not found: {filePath_x}')
			break
		# glob.glob()
		# break
	print(len(y))

def main():
	LoadData()

if __name__ == '__main__':
	main()