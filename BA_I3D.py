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
	x, y = np.array([]), np.array([])
	for feature in os.listdir(dir_labels):
		featureSplit = feature.split('_')
		if len(featureSplit) > 1:
			print(featureSplit)
			pass
		dir_x = os.path.join(dir_I3D[1], '_', 
			dir_I3D[3], dir_I3D[1], '_', dir_I3D[2],
			'.npy')
		print(dir_x)
		# glob.glob()
		# break

def main():
	LoadData()

if __name__ == '__main__':
	main()