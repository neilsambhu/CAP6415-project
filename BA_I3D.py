import numpy as np
import os, glob
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier

dir_I3D = "./bf_kinetics_feat/"
dir_labels = "./PatternTheory_WACV_Original/PatternTheory_WACV_Original/S1_PreProcessFiles/"

def LoadData():
	x, y = list(), list()
	for feature in tqdm(os.listdir(dir_labels)):
		featureSplit = feature.split('_')
		print(featureSplit)
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
		frameStart = int(featureSplit[-2])-frameOffset #need to do the check here
		if frameStart < 0:
			frameStart = 0
		frameEnd = int(featureSplit[-1])-frameOffset+1
		frameCount = frameEnd-frameStart
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
		print([featureSplit[-2]] * frameCount)
		y.extend([featureSplit[-2]] * frameCount)
		break
	return np.array(x), np.array(y)
def ML_Classifier(x,y):
	clf = RandomForestClassifier(n_estimators=2)
	k = 1000
	from collections import Counter
	print(Counter(y[:k]).keys())
	print(Counter(y[:k]).values())
	clf.fit(x[:k,:],y[:k])
	# clf.fit(x,y)
	# print(clf.feature_importances_)
	print(clf.predict(x[:k,:]))

def main():
	x,y = LoadData()
	# ML_Classifier(x,y)

if __name__ == '__main__':
	main()