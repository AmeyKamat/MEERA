import os

from circuits import Component, handler

from definitions import ROOT_DIR

class LoggingComponent(Component):

    @handler("DialogueGeneratedEvent")
    # pylint: disable=no-self-use
    def preprocess(self, context):
        file = open(os.path.join(ROOT_DIR, '..', 'log', 'meera.log'), "a")
        file.write(
            "{0}: {1} {2}\n".format(
                context.context_id,
                context.message,
                context.interaction['text']
            )
        )
        file.close()
