#!/usr/bin/env python

import data
import spacy

testData = data.getData()

# analyse intents

model = spacy.load("./nlp/models/intent_model")

correctPredictions = 0
totalPredictions = 0

for example in testData["skillData"]:
	totalPredictions = totalPredictions + 1
	utterance = example["sentence"]
	expectedIntent = example["category"]
	prediction = model(utterance)
	predictedIntent = sorted(prediction.cats, key=prediction.cats.get, reverse=True)[0]
	print(expectedIntent.__str__() + " " + predictedIntent)
	if expectedIntent[predictedIntent] == 1.0:
		correctPredictions = correctPredictions + 1

print("Intent Classifier Accuracy: {} percent", correctPredictions*0.1/totalPredictions)


# analyse requestType

model = spacy.load("./nlp/models/request_type_model")

correctPredictions = 0
totalPredictions = 0

for example in testData["requestTypeData"]:
	totalPredictions = totalPredictions + 1
	utterance = example["sentence"]
	expectedRequestType = example["category"]
	prediction = model(utterance)
	predictedRequestType = sorted(prediction.cats, key=prediction.cats.get, reverse=True)[0]
	print(expectedRequestType.__str__() + " " + predictedRequestType)
	if expectedRequestType[predictedRequestType] == 1.0:
		correctPredictions = correctPredictions + 1

print("Request Type Classifier Accuracy: {} percent", correctPredictions*100.0/totalPredictions)


# analyse chat

model = spacy.load("./nlp/models/chat_model")

correctPredictions = 0
totalPredictions = 0

for example in testData["chatData"]:
	totalPredictions = totalPredictions + 1
	utterance = example["sentence"]
	expectedChatResponse = example["category"]
	prediction = model(utterance)
	predictedChatResponse = sorted(prediction.cats, key=prediction.cats.get, reverse=True)[0]
	print(expectedChatResponse.__str__() + " " + predictedChatResponse)
	if expectedChatResponse[predictedChatResponse] == 1.0:
		correctPredictions = correctPredictions + 1

print("Chat Classifier Accuracy: {} percent", correctPredictions*100.0/totalPredictions)


# analyse entites

model = spacy.load("./nlp/models/entities_model")

correctPredictions = 0
totalPredictions = 0

for example in testData["skillData"]:
	totalPredictions = totalPredictions + 1
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

print("Entities NER Accuracy: {} percent", correctPredictions*100.0/totalPredictions)

