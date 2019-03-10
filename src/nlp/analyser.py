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

        self.request_type_model = get_model(models['request-type'])
        self.chat_model = get_model(models['chat'])
        self.intent_model = get_model(models['intent'])
        self.entities_model = get_model(models['entities'])

    def analyze(self, utterance):
        analysis = NLPAnalysis()
        utterance = utterance.lower()
        raw_analysis = self.request_type_model(utterance)
        analysis.requestType = get_category(raw_analysis)
        analysis.confidence = get_confidence(raw_analysis, analysis.requestType)

        if analysis.confidence < float(self.config['thresholds']['request-type-confidence']):
            return analysis

        if analysis.requestType == 'chat':
            raw_analysis = self.chat_model(utterance.strip())
            analysis.category = get_category(raw_analysis)
            analysis.confidence = get_confidence(raw_analysis, analysis.category)
        elif analysis.requestType == 'skill':
            raw_analysis = self.intent_model(utterance.strip())
            analysis.intent = get_category(raw_analysis)
            analysis.confidence = get_confidence(raw_analysis, analysis.intent)

            raw_analysis = self.entities_model(utterance.strip())
            analysis.entities = {}
            for ent in raw_analysis.ents:
                analysis.entities[ent.label_] = ent.text

        return analysis

def get_model(model_directory):
    model_path = os.path.join(ABS_MODELS_DIR, model_directory)
    return load(model_path)

def get_category(raw_analysis):
    return sorted(raw_analysis.cats, key=raw_analysis.cats.get, reverse=True)[0]

def get_confidence(raw_analysis, category):
    return raw_analysis.cats[category]
