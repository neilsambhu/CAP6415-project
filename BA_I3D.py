import numpy as np
import os, glob
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

dir_I3D = "./bf_kinetics_feat/"
dir_labels = "./PatternTheory_WACV_Original/PatternTheory_WACV_Original/S1_PreProcessFiles/"
dir_labels = '/home/DATASETS/BreakfastII_15fps_qvga_sync/'
def LoadData():
	x_test, y_test = list(), list()
	x_train, y_train = list(), list()
	for feature in tqdm(os.listdir(dir_labels)):
		featureSplit = feature.split('_')
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
		# test
		if int(featureSplit[1][1:]) < 16:
			x_test.extend(feature_x)
			y_test.extend([featureSplit[4]] * frameCount)
		# train
		else:
			x_train.extend(feature_x)
			y_train.extend([featureSplit[4]] * frameCount)
	print(np.array(x_test).shape,np.array(y_test).shape,
		np.array(x_train).shape,np.array(y_train).shape)
	return np.array(x_test),np.array(y_test), \
		np.array(x_train),np.array(y_train)
def LoadData2():
	x_test, y_test = list(), list()
	x_train, y_train = list(), list()
	for person in tqdm(os.listdir(dir_labels)):
		dir_person = os.path.join(dir_labels,person)
		print(dir_person)
		quit()
		featureSplit = feature.split('_')
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
		# test
		if int(featureSplit[1][1:]) < 16:
			x_test.extend(feature_x)
			y_test.extend([featureSplit[4]] * frameCount)
		# train
		else:
			x_train.extend(feature_x)
			y_train.extend([featureSplit[4]] * frameCount)
	print(np.array(x_test).shape,np.array(y_test).shape,
		np.array(x_train).shape,np.array(y_train).shape)
	return np.array(x_test),np.array(y_test), \
		np.array(x_train),np.array(y_train)
def ML_Classifier(x_test,y_test,
	x_train,y_train,n_estimators=1):
	clf = RandomForestClassifier(n_estimators=n_estimators)
	k = 1000
	# from collections import Counter
	# print(Counter(y).keys())
	# print(Counter(y).values())
	# clf.fit(x[:k,:],y[:k])
	clf.fit(x_train,y_train)
	# for item in clf.feature_importances_:
	# 	print(item, end=" ")
	
	# y_true = y[:k]
	# y_pred = clf.predict(x[:k,:])
	y_true = y_test
	y_pred = clf.predict(x_test)
	print(accuracy_score(y_true,y_pred))
	print(confusion_matrix(y_true,y_pred))

def main():
	x_test,y_test,x_train,y_train = LoadData2()
	ML_Classifier(x_test,y_test,x_train,y_train)
	# print('10 trees')
	# ML_Classifier(x,y,10)
	# print('100 trees')
	# ML_Classifier(x,y,100)

if __name__ == '__main__':
	main()