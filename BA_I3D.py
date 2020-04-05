import numpy as np
import os
from enum import Enum

dir_I3D = "./bf_kinetics_feat/"
dir_labels = "./PatternTheory_WACV_Original/PatternTheory_WACV_Original/S1_PreProcessFiles/"

class Actions(Enum):
	put=0
	# cut=0
	# walk_in
	# put
	# ","spoon","peel","stir","walk_out", "smear","squeeze", "butter", "pour", "fry", "crack", "take", "add"]

def LoadData():
	X, y = np.array([]), np.array([])
	for feature in os.listdir(dir_labels):
		featureSplit = feature.split('_')
		if len(featureSplit) > 1:
			print(Actions[featureSplit[4]])
		# break

def main():
	LoadData()

if __name__ == '__main__':
	main()