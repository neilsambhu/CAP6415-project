import os
import requests
import numpy as np

def writePriors(priors, outputFile):
	for relation in priors.keys():
		
		for item1,item2Dict in priors[relation].iteritems():
			target.write(item1 + ",")
			for item2,weight in item2Dict.iteritems():
				target.write(item2 + ":" + str(weight) + ",")			
			target.seek(-1, os.SEEK_END)
			target.truncate()
			target.write("\n")
		target.close()


def getEquivalence(item, rel):
	equivalent = {}
	obj = requests.get('http://api.conceptnet.io/query?start=/c/en/' + item + '&' + rel + '&filter=/c/en').json()
	if not obj:
		return equivalent
	if len(obj['edges']) > 0:
		for i in obj['edges']:
			relation = i['rel']['label']
			weight = i['weight']
			label = i['end']['label']
			labelID = i['end']['@id']
			equivalent[labelID] = weight
	return equivalent

def getPriors(item, equivalentDict):
	priors = []
	
	for item1, weight in equivalentDict.iteritems():
		# print item, item1
		i = str.split(str(item1),'/');
		if len(i) > 4:
			print i
			i.pop()
			print '/'.join(i)
		url = 'http://api.conceptnet.io/query?node=/c/en/' + item + '&other=' + '/'.join(i)
		print url
		obj = requests.get(url).json()
		if not obj:
			continue
		if len(obj['edges']) > 0:
			for i in obj['edges']:
				wt = i['weight']
				priors.append(wt)

	# print priors
	return np.linalg.norm(priors)

outputFilePath = "./"
outputFileNameSuffix = "contextualPriors"

actions = ["cut","walk_in","spoon","peel","stir","walk_out", "smear","put","squeeze", "butter", "pour", "fry", "crack", "take", "add"]
# actions = ["spoon","peel"]
objects = ["topping", "topping_on_top", "coffee", "teabag", "plate", "eggs", "juice", "salt_and_pepper", "milk", "powder", "bun_together", "fruit", "tea", "pancake", "cereals", "sugar", "bun", "bowl", "egg", "glass", "water", "orange", "pan", "cup", "oil", "dough", "flour", "squeezer", "butter", "knife"]

rel = 'rel=/r/IsA'

item1 = 'oil'
item2 = 'pour'

equivalent = {}
priors = {'HC_IsA': {}}

print "Obtaining Equivalents ..."
for item1 in objects:
	e = getEquivalence(item1, rel)
	equivalent[item1] = e

print "Constructing priors table ..."

outputFileName = outputFilePath + outputFileNameSuffix + "_Action_Object_HC_IsA.txt"
target = open(outputFileName, 'w')

for item2 in actions:
	target.write(item2 + ",")
	for label, e in equivalent.iteritems():
		p = getPriors(item2, e)
		# priors['HC_IsA'][item2][label] = p
		target.write(label + ":" + str(p) + ",")
		# print item2, label, p
	target.seek(-1, os.SEEK_END)
	target.truncate()
	target.write("\n")
target.close()


# print "Writing priors table to file ..."

writePriors(priors, outputFileName)
# print item1, item2, p 