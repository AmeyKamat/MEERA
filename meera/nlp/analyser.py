import os

from configparser import ConfigParser
from spacy import load

from nlp.model import NLPAnalysis
from definitions import ABS_MODELS_DIR

class NLPAnalyser:

    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'component.ini'))
    
    def __init__(self):
        super(NLPAnalyser, self).__init__()

        models = self.config['models']

        self.requestTypeModel = getModel(models['request-type'])
        self.chatModel = getModel(models['chat'])
        self.intentModel = getModel(models['intent'])
        self.entitiesModel = getModel(models['entities'])

        
    def analyze(self, utterance):
        analysis = NLPAnalysis()
        utterance = utterance.lower()
        rawAnalysis = self.requestTypeModel(utterance)
        analysis.requestType = getCategory(rawAnalysis)
        analysis.confidence = getConfidence(rawAnalysis, analysis.requestType)
        
        if analysis.confidence < float(self.config['thresholds']['request-type-confidence']):
            return analysis

        if analysis.requestType == 'chat':
            rawAnalysis = self.chatModel(utterance.strip())
            analysis.category = getCategory(rawAnalysis)
            analysis.confidence = getConfidence(rawAnalysis, analysis.category)
        elif analysis.requestType == 'skill':
            rawAnalysis = self.intentModel(utterance.strip())
            analysis.intent = getCategory(rawAnalysis)
            analysis.confidence = getConfidence(rawAnalysis, analysis.intent)

            rawAnalysis = self.entitiesModel(utterance.strip())
            analysis.entities = {}
            for ent in rawAnalysis.ents:
                analysis.entities[ent.label_] = ent.text

        return analysis

def getModel(modelDirectory):
    modelPath = os.path.join(ABS_MODELS_DIR, modelDirectory)
    return load(modelPath)

def getCategory(rawAnalysis):
    return sorted(rawAnalysis.cats, key=rawAnalysis.cats.get, reverse=True)[0]

def getConfidence(rawAnalysis, category):
    return rawAnalysis.cats[category]