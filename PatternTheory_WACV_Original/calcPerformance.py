from __future__ import division
import numpy as np
import os

inputPath = "./BA_S1_Out/"

actions = ["cut","walk_in","spoon","peel","stir","walk_out", "smear","put","squeeze", "butter", "pour", "fry", "crack", "take", "add"]
objects = ["topping", "topping_on_top", "coffee", "teabag", "plate", "eggs", "juice", "salt_and_pepper", "milk", "powder", "bun_together", "fruit", "tea", "pancake", "cereals", "sugar", "bun", "bowl", "egg", "glass", "water", "orange", "pan", "cup", "oil", "dough", "flour", "squeezer", "butter", "knife"]
filelist = [ f for f in os.listdir(inputPath)]
value = []
values = {}
fullCorrect = 0
numCorrect = 0
set1 = {}
print "Num indpendent videos:", len(filelist)
for errorProb in range(1):
	for split in ["S1"]:
		inputPath1 = inputPath
		filelist = [ f for f in os.listdir(inputPath1)]
		for topK in [10]:
			value = []
			values = {}
			fullCorrect = 0
			numCorrect = 0
			objCorrect = 0
			actCorrect = 0
			for inputFile in filelist:
				truthValue = []
				data = str.split(inputFile.replace('\n', ''), "_")
				dataVal = []
				dataVal.append(data[0])
				dataVal.append(data[1])
				dataVal.append(data[2])
				dataVal.append(data[3])
				dataVal.append(data[4])
				videoName = "_".join(i for i in dataVal)
				truthValue.append(data[3])
				truthValue.append(data[4])
				
				with open(inputPath1+inputFile) as f:
					lineCount = 0
					percentOverlap = []
					objCorrectVid = False
					actCorrectVid = False
					for line in f:
						if lineCount <= topK:# and lineCount < 3:
							if line.isspace() or line == "\r":
								continue
							genVal = []
							val = str.split(line.replace('\n', ''), "_")
							if len(val) <= 1:
								continue
							genVal.append(str.split(val[0], '-')[0])
							genVal.append(str.split(val[1], '-')[0])
							p = float(len(set(truthValue) & set(genVal)) / (len(truthValue)))
							if p > 0:
								if len((set(truthValue) & set(genVal)) & set(objects)) > 0:
									objCorrectVid = True
								if len((set(truthValue) & set(genVal)) & set(actions)) > 0:
									actCorrectVid = True
							if topK == 10:
								if p == 1:
									print videoName, genVal, truthValue
							percentOverlap.append(len(set(truthValue) & set(genVal)) / (len(truthValue)))
						lineCount += 1
					value.append(max(percentOverlap))
					if objCorrectVid:
						objCorrect += 1
					if actCorrectVid:
						actCorrect += 1
					if videoName in values:
						values[videoName].append(max(percentOverlap))
					else:
						values[videoName] = []
						values[videoName].append(max(percentOverlap))

			avgVal = values.values()
			val = []
			percentNone = 0
			for i in avgVal:
				val.append(np.mean(i))
				fullCorrect += i.count(1)
				numCorrect += sum(j > 0 for j in i)
				if sum(j > 0 for j in i) == 0:
					percentNone += 1

			print "Num composite videos:", len(values.keys())
			print "Paper Metric Average Performamce :%s" % np.mean(val)
			print "Object Accuracy:", objCorrect/len(filelist)
			print "Action Accuracy:", actCorrect/len(filelist)
			print "Zero match Composite Videos:", percentNone 
			print "Full Correct", fullCorrect