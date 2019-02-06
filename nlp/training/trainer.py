#!/usr/bin/env python

import os
import ner
import textcat

def getSkillData(skillRawTrainingData):
	skillData = []
	for line in skillRawTrainingData:
		skillData.append({
			"sentence": getSentence(line),
			"category": getCategory(line, SKILL_CATEGORIES),
			"entities": getEntities(line)
		})

	return skillData

def getchatData(chatRawTrainingData):
	chatData = []
	for line in chatRawTrainingData:
		chatData.append({
			"sentence": getSentence(line),
			"category": getCategory(line, CHAT_CATEGORIES)
		})
	return chatData

def getRequestTypeResolutionData(skillRawTrainingData, chatRawTrainingData):
	requestResolutionTypeData = []
	for line in skillRawTrainingData:
		requestResolutionTypeData.append({
			"sentence": getSentence(line),
			"category": { "chat": 0.0, "skill": 1.0 }
		})
	for line in chatRawTrainingData:
		requestResolutionTypeData.append({
			"sentence": getSentence(line),
			"category": { "chat": 1.0, "skill": 0.0 }
		})
	return requestResolutionTypeData

def getSentence(line):
	return line.split('|')[0]

def getCategory(line, categories):
	categoryCounter = {}
	category = line.split('|')[1]
	for definedCategory in categories:
		if definedCategory == category:
			categoryCounter[definedCategory] = 1.0
		else:
			categoryCounter[definedCategory] = 0.0
	return categoryCounter

def getEntities(line):
	entities = []
	record = line.split('|')
	if len(record) > 2:
		for index in range(2, len(record)):
			entity = record[index]
			entities.append(
				(
					int(entity.split(',')[1]), 	# start index
					int(entity.split(',')[2]),	# end index
					entity.split(',')[0]		# entity
				)
			)
	return entities

SKILL_CATEGORIES = ['news']
NER_CATEGORIES = ['date', 'query', 'news-category']

skillRawTrainingData = []
chatRawTrainingData = []

installedPlugins = [f.name for f in os.scandir("plugins") if f.is_dir() and f.name != "__pycache__"] 

for plugin in installedPlugins:
	file = open("./plugins/{0}/plugin.utterance".format(plugin), "r")
	for line in file:
		skillRawTrainingData.append(line)

file = open("./nlp/chat.utterance".format(plugin), "r")

for line in file:
    chatRawTrainingData.append(line, "utf-8")

skillData = getSkillData(skillRawTrainingData)
chatData = getchatData(chatRawTrainingData)
requestTypeResolutionData = getRequestTypeResolutionData(skillRawTrainingData, chatRawTrainingData)

textcat.train("en.assistant.intent.model", "./nlp/models/intent_model", SKILL_CATEGORIES, skillData, 20)
ner.train("en.assistant.entity.model", "./nlp/models/entities_model", NER_CATEGORIES, skillData, 20)
textcat.train("en.assistant.chat.model", "./nlp/models/chat_model", CHAT_CATEGORIES, chatData, 20)
textcat.train("en.assistant.requestType.model", "./nlp/models/request_type_model", ["chat", "skill"], requestTypeResolutionData, 20)
