import requests
import os

def getContextualPriors(list1, list2):
	priors = {}
	for item1 in list1:
		for item2 in list2:
			if item1 != item2:
				obj = requests.get('http://api.conceptnet.io/query?node=/c/en/' + item1 + '&other=/c/en/' + item2).json()
				if len(obj['edges']) > 0:
					print item1, item2
					for i in obj['edges']:
						print i['weight'], i['rel']['label']
						relation = i['rel']['label']
						weight = i['weight']
						if relation not in priors.keys():
							priors[relation] = {}
						if item1 not in priors[relation].keys():
							priors[relation][item1] = {}
						# if item2 not in priors[relation].keys():
						# 	priors[relation][item2] = {}
						priors[relation][item1][item2] = weight
						# priors[relation][item2][item1] = weight
				# else:
					# print "No match betwen %s and %s" % (item1, item2)
	return priors

def writePriors(priors, outputFile):
	for relation in priors.keys():
		outputFileName = outputFile + relation + ".txt"
		target = open(outputFileName, 'w')
		for item1,item2Dict in priors[relation].iteritems():
			target.write(item1 + ",")
			for item2,weight in item2Dict.iteritems():
				target.write(item2 + ":" + str(weight) + ",")			
			target.seek(-1, os.SEEK_END)
			target.truncate()
			target.write("\n")
		target.close()

outputFilePath = "/home/saakur/Desktop/hierarchicalContextualReasoningPT/HRC_Priors/Contextual_Priors/"
outputFileNameSuffix = "contextualPriors"

actions = ["cut","walk_in","spoon","peel","stir","walk_out", "smear","put","squeeze", "butter", "pour", "fry", "crack", "take", "add"]
objects = ["topping", "topping_on_top", "coffee", "teabag", "plate", "eggs", "juice", "salt_and_pepper", "milk", "powder", "bun_together", "fruit", "tea", "pancake", "cereals", "sugar", "bun", "bowl", "egg", "glass", "water", "orange", "pan", "cup", "oil", "dough", "flour", "squeezer", "butter", "knife"]

act_act_priors = getContextualPriors(actions, actions)
outputFileName = outputFilePath + outputFileNameSuffix + "_Action_Action_"
writePriors(act_act_priors, outputFileName)

act_obj_priors = getContextualPriors(actions, objects)
print act_obj_priors
outputFileName = outputFilePath + outputFileNameSuffix + "_Action_Object_"
writePriors(act_obj_priors, outputFileName)

obj_obj_priors = getContextualPriors(objects, objects)
outputFileName = outputFilePath + outputFileNameSuffix + "_Object_Object_"
writePriors(obj_obj_priors, outputFileName)