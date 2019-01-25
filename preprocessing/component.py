from circuits import Component, handler
from configparser import ConfigParser

from events import *
from preprocessing.location import LocationPreprocessor
from preprocessing.date import DatePreprocessor

class PreprocessingComponent(Component):

	prepocessors = {
		"location": LocationPreprocessor(),
		"date": DatePreprocessor()
	}

	@handler("SkillRequestedEvent")
	def preprocess(self, context):
		entities = context.nlpAnalysis.entities
		for key, value in entities:
			preprocessor = self.prepocessors.get(key)
			if preprocessor != None:
				entities.update(preprocessor.preprocess(value))
		context.nlpAnalysis.entities = entities
		self.fire(EntitiesPreprocessedEvent(context))