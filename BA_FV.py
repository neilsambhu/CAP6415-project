import numpy as np
import os, glob
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from joblib import dump, load
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
			#train
			else:
				x_train.extend(file[:,1:])
				y_train.extend([feature] * file[:,1:].shape[0])
			# break
		# break
	# print(np.array(x_test).shape,np.array(y_test).shape,
	# 	np.array(x_train).shape,np.array(y_train).shape)
	return np.array(x_test), np.array(y_test), \
		np.array(x_train), np.array(y_train)
def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """pretty print for confusion matrixes"""
    columnwidth = max([len(x) for x in labels] + [5])  # 5 is value length
    empty_cell = " " * columnwidth
    # Print header
    print("    " + empty_cell, end=" ")
    for label in labels:
        print("%{0}s".format(columnwidth) % label, end=" ")
    print()
    # Print rows
    for i, label1 in enumerate(labels):
        print("    %{0}s".format(columnwidth) % label1, end=" ")
        for j in range(len(labels)):
            cell = "%{0}.1f".format(columnwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print(cell, end=" ")
        print()
def ML_Classifier(x_test,y_test,
	x_train,y_train,n_estimators=1):
	clf = RandomForestClassifier(n_estimators=n_estimators)
	clf.fit(x_train,y_train)
	dump(clf, f'output/FV-01-RF-{n_estimators}.joblib')

	y_true = y_test
	y_pred = clf.predict(x_test)
	print(f'acc: {accuracy_score(y_true,y_pred)}')
	confusionMatrix = confusion_matrix(y_true,y_pred)
	print_cm(confusionMatrix,labels)
	print(f'confusion matrix shape {confusionMatrix.shape}')

def main():
	x_test,y_test,x_train,y_train = LoadData()
	# print('10 trees')
	# ML_Classifier(x_test,y_test,x_train,y_train,10)
	print('100 trees')
	ML_Classifier(x_test,y_test,x_train,y_train,100)

if __name__ == '__main__':
	main()