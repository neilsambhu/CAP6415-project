import numpy as np
import os

dir_I3D = "./bf_kinetics_feat/"
dir_labels = "./PatternTheory_WACV_Original/PatternTheory_WACV_Original/S1_PreProcessFiles/"

def LoadData():
	X, y = np.array([]), np.array([])
	for feature in os.listdir(dir_labels):
		print(feature)
		break

def main():
	LoadData()

if __name__ == '__main__':
	main()