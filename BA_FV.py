import numpy as np
import os, glob
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

dir_FV = "./breakfast_data/s1/"

def LoadData():
	x, y = list(), list()
	for feature in tqdm(os.listdir(dir_FV)):
		dir_objects = os.path.join(dir_FV, feature)
		for file in os.listdir(dir_objects):
			print(file)
			temp = np.loadtxt(os.path.join(dir_objects,file))
			print(temp)
			print(temp.shape)
			break
		break
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
		y.extend([featureSplit[4]] * frameCount)
	return np.array(x), np.array(y)
def ML_Classifier(x,y,n_estimators=1):
	clf = RandomForestClassifier(n_estimators=n_estimators)
	k = 1000
	# from collections import Counter
	# print(Counter(y).keys())
	# print(Counter(y).values())
	# clf.fit(x[:k,:],y[:k])
	clf.fit(x,y)
	# for item in clf.feature_importances_:
	# 	print(item, end=" ")
	
	# y_true = y[:k]
	# y_pred = clf.predict(x[:k,:])
	y_true = y
	y_pred = clf.predict(x)
	print(accuracy_score(y_true,y_pred))
	print(confusion_matrix(y_true,y_pred))

def main():
	x,y = LoadData()

if __name__ == '__main__':
	main()