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
	countFiles = 0
	countCorrect = 0
	for filepath in glob.glob(filepathRegex):
		trueActionLabel = filepath.split('/')[-1].split('_')[4]
		# print(trueActionLabel)
		with open(filepath, "r") as f:
			fileContents = f.read().split('\n')
			# remove last line character
			if fileContents[-1]=='':
				fileContents = fileContents[:-1]
			arrActionLabels = [line.split(' ')[0] for line in fileContents]
			arrPred = [float(line.split(' ')[1]) for line in fileContents]
			idxMax = np.argmax(arrPred)
			predActionLabel = arrActionLabels[idxMax]
			# print(predActionLabel)
			if trueActionLabel == predActionLabel:
				print(trueActionLabel)
				quit()
		# quit()

def main():
	labelAccuracy(dir_HOF_HOG + 'HOF*')

if __name__ == '__main__':
	main()