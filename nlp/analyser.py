import spacy
from configparser import ConfigParser

class NLPAnalyser(object):

	config = ConfigParser()
	config.read("./nlp/component.ini")
	
	def __init__(self):
		super(NLPAnalyser, self).__init__()
		
		print(self.config.sections())
		#self.requestTypeModel = spacy.load(self.config['models']['requestType'])
		#self.chatModel = spacy.load(self.config['models']['chat'])
		#self.skillModel = spacy.load(self.config['models']['skill'])

		
	def analyze(self, utterance):
		analysis = {}
		
		#rawAnalysis = self.requestTypeModel(utterance)
		analysis.requestType = "skill" #self.getCategory(rawAnalysis)
		analysis.confidence = 0.9 #self.getConfidence(rawAnalysis, analysis.requestType)
		
		if analysis.confidence < float(self.config['thresholds']['requestTypeConfidence']):
			return analysis

		if analysis.requestType == "chat":
			#rawAnalysis = self.chatModel(utterance)
			analysis.category = 1 #self.getCategory(rawAnalysis)
			analysis.confidence = 0.1 #self.getConfidence(rawAnalysis, analysis.category)
		elif analysis.requestType == "skill":
			#rawAnalysis = self.skillModel(utterance)
			analysis.intent = "question" #self.getCategory(rawAnalysis)
			analysis.confidence = 0.9 #self.getConfidence(rawAnalysis, analysis.intent)

			for ent in rawAnalysis.ents:
				analysis.entities[ent.label_] = ent.text

		return analysis

	def getCategory(self, rawAnalysis):
		return sorted(rawAnalysis.cats, key=rawAnalysis.cats.get, reverse=True)[0]

	def getConfidence(self, rawAnalysis, category):
		return doc.cats[category]