from circuits import Component, handler

from events import EntitiesPreprocessedEvent
from preprocessing.location import LocationPreprocessor
from preprocessing.date import DatePreprocessor

class PreprocessingComponent(Component):

    prepocessors = {
        "location": LocationPreprocessor(),
        "source-location": LocationPreprocessor(),
        "destination-location": LocationPreprocessor(),
        "date": DatePreprocessor()
    }

    @handler("SkillRequestedEvent")
    def preprocess(self, context):
        try:
            entities = context.nlp_analysis.entities
            for key in entities.keys():
                value = entities[key]
                preprocessor = self.prepocessors.get(key)
                if preprocessor is not None:
                    entities[key] = preprocessor.preprocess(value)
            context.nlp_analysis.entities = entities
        # pylint: disable=broad-except
        except Exception:
            pass

        self.fire(EntitiesPreprocessedEvent(context))
