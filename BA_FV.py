import numpy as np
import os, glob
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
np.set_printoptions(suppress=True)

dir_FV = "./breakfast_data/s1/"

def LoadData():
	x_test, y_test = list(), list()
	x_train, y_train = list(), list()
	for feature in tqdm(os.listdir(dir_FV)):
		dir_objects = os.path.join(dir_FV, feature)
		for fileName in os.listdir(dir_objects):
			fileNameSplit = fileName.split('_')
			file = np.loadtxt(os.path.join(dir_objects,fileName))
			# test
			if int(fileNameSplit[0][1:]) < 16:
				x_test.extend(file[:,1:])
				y_test.extend([feature] * file[:,1:].shape[0])
			else:
				x_train.extend(file[:,1:])
				y_train.extend([feature] * file[:,1:].shape[0])
			# break
		# break
	print(np.array(x_test).shape,np.array(y_test).shape,
		np.array(x_train).shape,np.array(y_train).shape)
	return np.array(x_test), np.array(y_test), \
		np.array(x_train), np.array(y_train)
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
	ML_Classifier(x,y)

if __name__ == '__main__':
	main()