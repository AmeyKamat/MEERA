#!/usr/bin/env python

import os
import ner
import textcat
import re
from threading import Thread


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
	return re.sub(r'[^\w\s]','', line.split('|')[0]).lower().strip()

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
					int(entity.split(',')[1]), 			# start index
					int(entity.split(',')[2]),			# end index
					entity.split(',')[0].strip()		# entity
				)
			)
	return entities

def getEntityNames(line):
	entities = []
	record = line.split('|')
	if len(record) > 2:
		for index in range(2, len(record)):
			entity = record[index]
			entities.append(entity.split(',')[0].strip())
	return entities

def getSkillCategories(skillRawTrainingData):
	return set([line.split('|')[1].strip() for line in skillRawTrainingData])

def getChatCategories(chatRawTrainingData):
	return set([line.split('|')[1].strip() for line in chatRawTrainingData])

def getEntityCategories(skillRawTrainingData):
	entityNames = []
	for line in skillRawTrainingData:
		entityNames += getEntityNames(line)
	return entityNames

skillRawTrainingData = []
chatRawTrainingData = []

installedPlugins = [f.name for f in os.scandir("plugins") if f.is_dir() and f.name != "__pycache__"] 

for plugin in installedPlugins:
	file = open("./plugins/{0}/plugin.utterance".format(plugin), "r")
	for line in file:
		skillRawTrainingData.append(line)

file = open("./nlp/chat.utterance".format(plugin), "r")

for line in file:
    chatRawTrainingData.append(line)

SKILL_CATEGORIES = getSkillCategories(skillRawTrainingData)
CHAT_CATEGORIES = getChatCategories(chatRawTrainingData)
NER_CATEGORIES = set(getEntityCategories(skillRawTrainingData))

print(SKILL_CATEGORIES)
print(CHAT_CATEGORIES)
print(NER_CATEGORIES)

skillData = getSkillData(skillRawTrainingData)
chatData = getchatData(chatRawTrainingData)
requestTypeResolutionData = getRequestTypeResolutionData(skillRawTrainingData, chatRawTrainingData)

intentTrainingThread = Thread(target=textcat.train, args=("en.assistant.intent.model", "./nlp/models/intent_model", SKILL_CATEGORIES, skillData, 100))
entityTraningThread = Thread(target=ner.train, args=("en.assistant.entity.model", "./nlp/models/entities_model", NER_CATEGORIES, skillData, 100))
chatTrainingThread = Thread(target=textcat.train, args=("en.assistant.chat.model", "./nlp/models/chat_model", CHAT_CATEGORIES, chatData, 100))
requestTypeTrainingThread = Thread(target=textcat.train, args=("en.assistant.requestType.model", "./nlp/models/request_type_model", ["chat", "skill"], requestTypeResolutionData, 100))

entityTraningThread.start()
intentTrainingThread.start()
chatTrainingThread.start()
requestTypeTrainingThread.start()

intentTrainingThread.join()
chatTrainingThread.join()
requestTypeTrainingThread.join()
entityTraningThread.join()