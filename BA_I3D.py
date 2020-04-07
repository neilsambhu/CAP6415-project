import numpy as np
import os, glob
from tqdm import tqdm

dir_I3D = "./bf_kinetics_feat/"
dir_labels = "./PatternTheory_WACV_Original/PatternTheory_WACV_Original/S1_PreProcessFiles/"

def LoadData():
	x, y = list(), list()
	for feature in tqdm(os.listdir(dir_labels)):
		featureSplit = feature.split('_')
		# print(featureSplit)
		if len(featureSplit) <= 1:
			continue
		# replace 'salad' with 'salat'
		if featureSplit[2] == 'salad':
			featureSplit[2] = 'salat'
		filePath_x = os.path.join(dir_I3D,
			featureSplit[1] + '_' + 
			featureSplit[3] + '_' +
			featureSplit[1] + '_' + 
			featureSplit[2] + '.npy')
		if not os.path.exists(filePath_x):
			print(f'File not found: {filePath_x}')
			continue
		featureVideo = np.load(filePath_x)
		# print(featureVideo.shape)
		frameOffset = 5
		frameStart = int(featureSplit[-2])-frameOffset
		frameEnd = int(featureSplit[-1])-frameOffset+1
		frameCount = frameEnd-frameStart
		if frameStart < 0:
			print(f'Error: frameStart value {frameStart}', 
				f'featureVideo.shape[0] {featureVideo.shape[0]}')
			print(featureSplit)
			quit()
			continue
		if frameEnd > featureVideo.shape[0]:
			print(f'Error: frameEnd value {frameEnd}', 
				f'featureVideo.shape[0] {featureVideo.shape[0]}')
			print(featureSplit)
			quit()
			continue
		# print(frameEnd,frameStart,featureSplit[7],featureSplit[6],
		# 	frameEnd-frameStart,int(featureSplit[7])-int(featureSplit[6]))
		feature_x = featureVideo[frameStart:frameEnd,:]
		# print(feature_x.shape)
		x.extend(feature_x)
		y.extend([featureSplit[-2]] * frameCount)
	print(np.array(x).shape, np.array(y).shape)

def main():
	LoadData()

if __name__ == '__main__':
	main()