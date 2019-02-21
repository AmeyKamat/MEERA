#!/usr/bin/env python


import ner
import textcat
import data

from copy import deepcopy
from threading import Thread

trainingData = data.getData()

intentTrainingThread = Thread(
	target=textcat.train, 
	args=(
		"en.assistant.intent.model", 
		"./nlp/models/intent_model", 
		trainingData["intents"], 
		deepcopy(trainingData["skillData"]), 
		100
	)
)

entityTraningThread = Thread(
	target=ner.train, 
	args=(
		"en.assistant.entity.model", 
		"./nlp/models/entities_model", 
		trainingData["entities"], 
		deepcopy(trainingData["skillData"]), 
		50
	)
)

chatTrainingThread = Thread(
	target=textcat.train, 
	args=(
		"en.assistant.chat.model", 
		"./nlp/models/chat_model", 
		trainingData["chatCategories"], 
		deepcopy(trainingData["chatData"]), 
		100
	)
)

requestTypeTrainingThread = Thread(
	target=textcat.train, 
	args=(
		"en.assistant.requestType.model", 
		"./nlp/models/request_type_model", 
		trainingData["requestTypes"], 
		deepcopy(trainingData["requestTypeData"]), 
		100
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