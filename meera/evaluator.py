#!/usr/bin/env python

import os

from spacy import load
from configparser import ConfigParser

import nlp.training.data as data
from definitions import ROOT_DIR, ABS_MODELS_DIR

config = ConfigParser()
config.read(os.path.join(ROOT_DIR, 'nlp', 'component.ini'))

testData = data.getData()

# analyse intents

def getIntentModelAccuracy():
	print(os.path.join(ABS_MODELS_DIR, config['models']['intent']))
	model = load(os.path.join(ABS_MODELS_DIR, config['models']['intent']))

	correctPredictions = 0
	totalPredictions = 0

	for example in testData["skillData"]:
		totalPredictions = totalPredictions + 1
		utterance = example["sentence"]
		expectedIntent = example["category"]
		prediction = model(utterance)
		predictedIntent = sorted(prediction.cats, key=prediction.cats.get, reverse=True)[0]
		if expectedIntent[predictedIntent] == 1.0:
			correctPredictions = correctPredictions + 1
		else:
			print(utterance + " " + predictedIntent)
	return correctPredictions*100/totalPredictions




# analyse requestType

def getRequestTypeModelAccuracy():
	model = load(os.path.join(ABS_MODELS_DIR, config['models']['request-type']))

	correctPredictions = 0
	totalPredictions = 0

	for example in testData["requestTypeData"]:
		totalPredictions = totalPredictions + 1
		utterance = example["sentence"]
		expectedRequestType = example["category"]
		prediction = model(utterance)
		predictedRequestType = sorted(prediction.cats, key=prediction.cats.get, reverse=True)[0]
		if expectedRequestType[predictedRequestType] == 1.0:
			correctPredictions = correctPredictions + 1
	return correctPredictions*100/totalPredictions




# analyse chat

def getChatModelAccuracy():
	model = load(os.path.join(ABS_MODELS_DIR, config['models']['chat']))

	correctPredictions = 0
	totalPredictions = 0

	for example in testData["chatData"]:
		totalPredictions = totalPredictions + 1
		utterance = example["sentence"]
		expectedChatResponse = example["category"]
		prediction = model(utterance)
		predictedChatResponse = sorted(prediction.cats, key=prediction.cats.get, reverse=True)[0]
		if expectedChatResponse[predictedChatResponse] == 1.0:
			correctPredictions = correctPredictions + 1
	return correctPredictions*100/totalPredictions



# analyse entites

def getEntitesModelAccuracy():
	model = load(os.path.join(ABS_MODELS_DIR, config['models']['entities']))

	correctPredictions = 0
	totalPredictions = 0

	for example in testData["skillData"]:
		utterance = example["sentence"]
		expectedEntities = example["entities"]
		prediction = model(utterance)
		predictedEntities = {}

		for ent in prediction.ents:
			predictedEntities[ent.label_] = ent.text

		for expectedEntity in expectedEntities:
			totalPredictions = totalPredictions + 1
			if expectedEntity[2] in predictedEntities.keys():
				expectedEntityText = utterance[expectedEntity[0]:expectedEntity[1]]
				if expectedEntityText == predictedEntities[expectedEntity[2]]:
					correctPredictions = correctPredictions + 1
	return correctPredictions*100/totalPredictions

try:
	print("Intent Classifier Accuracy: {} percent".format(getIntentModelAccuracy()))
except(Exception):
	print("Error calculating accuracy of Intent Classifier")

try:
	print("Request Type Classifier Accuracy: {} percent".format(getRequestTypeModelAccuracy()))
except(Exception):
	print("Error calculating accuracy of Request Type Classifier")

try:
	print("Chat Classifier Accuracy: {} percent".format(getChatModelAccuracy()))
except(Exception):
	print("Error calculating accuracy of Chat Classifier")

try:
	print("Entities NER Accuracy: {} percent".format(getEntitesModelAccuracy()))
except(Exception):
	print("Error calculating accuracy of Entities NER")


