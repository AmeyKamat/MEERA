import spacy
import re
from configparser import ConfigParser

from nlp.model import NLPAnalysis

class NLPAnalyser(object):

	config = ConfigParser()
	config.read("./nlp/component.ini")
	
	def __init__(self):
		super(NLPAnalyser, self).__init__()
		
		print(self.config.sections())
		self.requestTypeModel = spacy.load(self.config['models']['requestType'])
		self.chatModel = spacy.load(self.config['models']['chat'])
		self.intentModel = spacy.load(self.config['models']['intent'])
		self.entitiesModel = spacy.load(self.config['models']['entities'])

		
	def analyze(self, utterance):
		analysis = NLPAnalysis()
		utterance = re.sub(r'[^\w\s]','',utterance).lower()
		rawAnalysis = self.requestTypeModel(utterance)
		analysis.requestType = self.getCategory(rawAnalysis)
		analysis.confidence = self.getConfidence(rawAnalysis, analysis.requestType)
		
		if analysis.confidence < float(self.config['thresholds']['requestTypeConfidence']):
			return analysis

		if analysis.requestType == "chat":
			rawAnalysis = self.chatModel(utterance.strip())
			analysis.category = self.getCategory(rawAnalysis)
			analysis.confidence = self.getConfidence(rawAnalysis, analysis.category)
		elif analysis.requestType == "skill":
			rawAnalysis = self.intentModel(utterance.strip())
			analysis.intent = self.getCategory(rawAnalysis)
			analysis.confidence = self.getConfidence(rawAnalysis, analysis.intent)

			rawAnalysis = self.entitiesModel(utterance.strip())
			analysis.entities = {}
			for ent in rawAnalysis.ents:
				analysis.entities[ent.label_] = ent.text

		return analysis

	def getCategory(self, rawAnalysis):
		return sorted(rawAnalysis.cats, key=rawAnalysis.cats.get, reverse=True)[0]

	def getConfidence(self, rawAnalysis, category):
		return rawAnalysis.cats[category]