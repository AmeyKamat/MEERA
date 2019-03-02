#!/usr/bin/env python

import sys

import ner
import textcat
import data

from copy import deepcopy
from threading import Thread

trainingData = data.getData()

print("Intents: " + trainingData["intents"].__str__())
print("Entities: " + trainingData["entities"].__str__())
print("ChatCategories: " + trainingData["chatCategories"].__str__())

iterations = int(sys.argv[1])

intentTrainingThread = Thread(
	target=textcat.train, 
	args=(
		"en.assistant.intent.model", 
		"./nlp/models/intent_model", 
		trainingData["intents"], 
		deepcopy(trainingData["skillData"]), 
		iterations
	)
)

entityTraningThread = Thread(
	target=ner.train, 
	args=(
		"en.assistant.entity.model", 
		"./nlp/models/entities_model", 
		trainingData["entities"], 
		deepcopy(trainingData["skillData"]), 
		iterations
	)
)

chatTrainingThread = Thread(
	target=textcat.train, 
	args=(
		"en.assistant.chat.model", 
		"./nlp/models/chat_model", 
		trainingData["chatCategories"], 
		deepcopy(trainingData["chatData"]), 
		iterations
	)
)

requestTypeTrainingThread = Thread(
	target=textcat.train, 
	args=(
		"en.assistant.requestType.model", 
		"./nlp/models/request_type_model", 
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