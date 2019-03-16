import os

from configparser import ConfigParser
from circuits import Component, handler

from events import (NLPConfidenceLowEvent, ChatRequestedEvent,
                    SkillRequestedEvent, UserUnauthorizedEvent)
from nlp.analyser import NLPAnalyser

class NLPAnalysisComponent(Component):

    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'component.ini'))

    analyser = NLPAnalyser()
    paid_plugins = config['thresholds']['paid-plugins'].split(":")

    @handler("ContextCreatedEvent")
    def analyze(self, context):
        analysis = self.analyser.analyze(context.message)
        context.nlp_analysis = analysis

        if analysis.confidence < float(self.config['thresholds']['analysis-confidence']):
            self.fire(NLPConfidenceLowEvent(context))
        elif analysis.requestType == "chat":
            self.fire(ChatRequestedEvent(context))
        elif analysis.requestType == "skill":
            if analysis.intent not in self.paid_plugins or context.is_user_authorized:
                self.fire(SkillRequestedEvent(context))
            else:
                self.fire(UserUnauthorizedEvent(context))
