from circuits import Component, handler
from configparser import ConfigParser

from events import *
from nlp.analyser import NLPAnalyser

class NLPAnalysisComponent(Component):

	config = ConfigParser()
	config.read("./nlp/component.ini")
	
	analyser = NLPAnalyser()

	@handler("ContextCreatedEvent")
	def analyze(self, context):
		analysis = self.analyser.analyze(context.message)
		context.nlpAnalysis = analysis
		print(analysis)
		
		if analysis.confidence < float(self.config['thresholds']['analysisConfidence']):
			self.fire(NLPConfidenceLowEvent(context))
		elif analysis.requestType == "chat":
			self.fire(ChatRequestedEvent(context))
		elif analysis.requestType == "skill":
			self.fire(SkillRequestedEvent(context))