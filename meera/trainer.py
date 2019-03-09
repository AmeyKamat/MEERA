#!/usr/bin/env python

import sys
import os
from copy import deepcopy
from threading import Thread

from configparser import ConfigParser

import nlp.training.ner as ner
import nlp.training.textcat as textcat
import nlp.training.data as data
from definitions import ROOT_DIR, ABS_MODELS_DIR


config = ConfigParser()
config.read(os.path.join(ROOT_DIR, 'nlp', 'component.ini'))

trainingData = data.getData()

def getNumberOfSkillUtterances(trainingData):
	data = trainingData["skillData"]
	return len(data)

def getNumberOfIntents(trainingData):
	data = trainingData["intents"]
	return len(data)

def getNumberOfTaggedEntities(trainingData):
	data = trainingData["skillData"]
	counter = 0
	for record in data:
		counter += len(record["entities"])
	return counter

def getNumberOfEntityClasses(trainingData):
	data = trainingData["entities"]
	return len(data)

def getNumberOfChatCategories(trainingData):
	data = trainingData["chatCategories"]
	return len(data)

print("# of utterance: {}".format(getNumberOfSkillUtterances(trainingData)))
print()
print("# of intents: {}".format(getNumberOfIntents(trainingData)))
print("Intents: " + trainingData["intents"].__str__())
print()
print("# of entity classes: {}".format(getNumberOfEntityClasses(trainingData)))
print("# of tagged entities: {}".format(getNumberOfTaggedEntities(trainingData)))
print("Entity classes: " + trainingData["entities"].__str__())
print()
print("# of chat categories: {}".format(getNumberOfChatCategories(trainingData)))
print("Chat categories: " + trainingData["chatCategories"].__str__())

iterations = int(sys.argv[1])

intentTrainingThread = Thread(
	target=textcat.train, 
	args=(
		"en.assistant.intent.model", 
		os.path.join(ABS_MODELS_DIR, config['models']['intent']), 
		trainingData["intents"], 
		deepcopy(trainingData["skillData"]), 
		iterations
	)
)

entityTraningThread = Thread(
	target=ner.train, 
	args=(
		"en.assistant.entity.model", 
		os.path.join(ABS_MODELS_DIR, config['models']['entities']), 
		trainingData["entities"], 
		deepcopy(trainingData["skillData"]), 
		iterations
	)
)

chatTrainingThread = Thread(
	target=textcat.train, 
	args=(
		"en.assistant.chat.model", 
		os.path.join(ABS_MODELS_DIR, config['models']['chat']), 
		trainingData["chatCategories"], 
		deepcopy(trainingData["chatData"]), 
		iterations
	)
)

requestTypeTrainingThread = Thread(
	target=textcat.train, 
	args=(
		"en.assistant.requestType.model", 
		os.path.join(ABS_MODELS_DIR, config['models']['request-type']), 
		trainingData["requestTypes"], 
		deepcopy(trainingData["requestTypeData"]), 
		iterations
	)
)

entityTraningThread.start()
intentTrainingThread.start()
chatTrainingThread.start()
requestTypeTrainingThread.start()

intentTrainingThread.join()
chatTrainingThread.join()
requestTypeTrainingThread.join()
entityTraningThread.join()