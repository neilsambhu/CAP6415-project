import numpy as np
import os, glob, re
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
from sklearn.utils import shuffle
from joblib import dump, load
np.set_printoptions(suppress=True)

dir_HOF_HOG = "./PatternTheory_WACV_Original/PatternTheory_WACV_Original/S1_PreProcessFiles/labels/"

def labelAccuracy(filepathRegex):
	for filepath in glob.glob(filepathRegex):
		with open(filepath, "r") as f:
			fileContents = f.read().split('\n')
			# remove last line character
			if fileContents[-1]=='':
				fileContents = fileContents[:-1]
			# print('fileContents',fileContents)
			arrActionLabels = [line.split(' ')[0] for line in fileContents]
			arrPred = [line.split(' ')[1] for line in fileContents]
			print(arrActionLabels)
			print(arrPred)
			idxMax = np.argmax(arrPred)
			print(arrActionLabels[idxMax])
			quit()
			arr = np.fromfile(f)
			print(arr.shape)
			print(arr)
		# arr = np.fromfile(filepath, dtype=dtype.str, sep=" ")
		# print(arr.shape)
		# print(arr)
		quit()

def main():
	labelAccuracy(dir_HOF_HOG + 'HOF*')

if __name__ == '__main__':
	main()