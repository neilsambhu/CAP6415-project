import numpy as np
import os, glob

dir_I3D = "./bf_kinetics_feat/"
dir_labels = "./PatternTheory_WACV_Original/PatternTheory_WACV_Original/S1_PreProcessFiles/"

def LoadData():
	x, y = list(), list()
	for feature in os.listdir(dir_labels):
		featureSplit = feature.split('_')
		print(featureSplit)
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
				feature_x = np.load(filePath_x)
				print(feature_x.shape)
				# y.append()
				# print(f'{filePath_x}')
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