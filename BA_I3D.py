import numpy as np
import os, glob, re
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
from sklearn.utils import shuffle
from joblib import dump, load

dir_I3D = "./bf_kinetics_feat/"
dir_labels = "./PatternTheory_WACV_Original/PatternTheory_WACV_Original/S1_PreProcessFiles/"
dir_labels = '/home/DATASETS/BreakfastII_15fps_qvga_sync/'

def LoadData():
	x_test, y_test = list(), list()
	x_train, y_train = list(), list()
	# x_test, y_test = np.array([]), np.array([])
	# x_train, y_train = np.array([]), np.array([])
	for person in tqdm(os.listdir(dir_labels)):
		# if person == 'P03' or person == 'P43':
		# 	pass
		# else:
		# 	continue
		dir_person = os.path.join(dir_labels,person)
		for cam in os.listdir(dir_person):
			dir_cam = os.path.join(dir_person,cam)
			filesLabelsRegex = os.path.join(
				dir_cam,'*.labels')
			# print(filesLabelsRegex)
			for fileLabels in glob.glob(filesLabelsRegex):
				objectLabel = fileLabels.split('/')[-1].split('.')[0].split('_')[1]
				with open(fileLabels) as fp:
					line = fp.readline()
					# build file path to npy
					camName = cam
					if camName == 'stereo':
						camName = 'stereo01'
					filePath_x = os.path.join(dir_I3D,
						f'{person}_{camName}_{person}_{objectLabel}.npy')
					if not os.path.exists(filePath_x):
						# print(filePath_x)
						continue
					arr_x = np.load(filePath_x)
					while line:
						lineSplit = line.split(' ')
						actionLabel = lineSplit[1]
						# skip SIL
						if actionLabel == 'SIL':
							line = fp.readline()
							continue
						else:
							# extract action out of action-object pair
							actionLabel = actionLabel.split('_')[0]
						frameSplit = lineSplit[0].split('-')
						frameStart = int(frameSplit[0])
						frameEnd = int(frameSplit[1])
						# check if frames are the same
						# and action doesn't matter
						if frameStart == frameEnd:
							# print(frameSplit[0],actionLabel)
							line = fp.readline()
							continue
						frameOffset = 5
						frameStart -= frameOffset
						frameEnd -= frameOffset + 1
						if frameStart < 0:
							frameStart = 0
						if frameEnd < 1:
							# print(f'Warning: frameEnd value {frameEnd}')
							line = fp.readline()
							continue
						# handle ./bf_kinetics_feat/P43_cam02_P43_juice.npy
						if filePath_x == './bf_kinetics_feat/P43_cam02_P43_juice.npy':
							frameEnd = 1618
						# get npy lines
						extend_x = arr_x[frameStart:frameEnd]
						frameCount = frameEnd-frameStart
						# test
						if int(person[1:]) < 16:
							x_test.extend(extend_x)
							y_test.extend([actionLabel] * frameCount)
							# x_test = np.append(x_test, extend_x)
							# y_test = np.append(y_test, [actionLabel] * frameCount)
						#train
						else:
							x_train.extend(extend_x)
							y_train.extend([actionLabel] * frameCount)
							# x_train = np.append(x_train, extend_x)
							# y_train = np.append(y_train, [actionLabel] * frameCount)
						# if np.array(x_train).shape[0] != np.array(y_train).shape[0]:
						# 	print(np.array(x_train).shape[0], np.array(y_train).shape[0])
						# 	print(fileLabels,filePath_y,frameStart,frameEnd,frameCount)
						# 	quit()
						line = fp.readline()
	
	x_test,y_test,x_train,y_train = np.array(x_test),\
		np.array(y_test),np.array(x_train),np.array(y_train)
	print(x_test.shape,y_test.shape,
		x_train.shape,y_train.shape)
	return x_test,y_test,x_train,y_train
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
	x_train,y_train,labels,n_estimators=1):
	clf = RandomForestClassifier(n_estimators=n_estimators)
	clf.fit(x_train,y_train)
	dump(clf, 'output/I3D-01-RF-100.joblib')

	y_true = y_test
	y_pred = clf.predict(x_test)
	print(f'acc: {accuracy_score(y_true,y_pred)}')
	confusionMatrix = confusion_matrix(y_true,y_pred,labels=labels)
	print_cm(confusionMatrix,labels)
	print(f'confusion matrix shape {confusionMatrix.shape}')
	# print(clf.predict_proba(x_test))


def main():
	x_test,y_test,x_train,y_train = LoadData()
	labels = np.unique(y_train)
	
	# use 100% of training data
	n_samples = x_train.shape[0] // 1
	print(f'n_samples: {n_samples}')
	x_train,y_train = shuffle(x_train,y_train, 
		n_samples=n_samples)

	# print('1 tree')
	# ML_Classifier(x_test,y_test,x_train,y_train,labels)
	# print('10 trees')
	# ML_Classifier(x_test,y_test,x_train,y_train,labels,10)
	print('100 trees')
	ML_Classifier(x_test,y_test,x_train,y_train,labels,100)

if __name__ == '__main__':
	main()