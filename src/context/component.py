from circuits import Component, handler

from events import ContextCreatedEvent, EntitiesPreprocessedEvent

class ContextComponent(Component):

    def __init__(self, context_manager):
        super(ContextComponent, self).__init__()
        self.context_manager = context_manager

    @handler("MessageReceivedEvent")
    def record_context(self, request):
        context = self.context_manager.create_context(request)
        print("Context created: " + str(context.context_id))
        self.fire(ContextCreatedEvent(context))


    @handler("SelfLocationReceivedEvent")
    def update_self_location_in_context(self, request):
        context_id = request["context_id"]
        context = self.context_manager.get_context(context_id)
        entities = context.nlp_analysis.entities

        entities["self-location"] = {
            "latitude": request["body"]["latitude"],
            "longitude": request["body"]["longitude"]
        }

        self.fire(EntitiesPreprocessedEvent(context))
