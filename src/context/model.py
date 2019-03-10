import uuid

from nlp.model import NLPAnalysis

class Context:

    client_id = None
    context_id = None
    conversation_id = None
    message = None
    nlp_analysis = NLPAnalysis()
    previous_context = None
    self_location = None
    interaction = {}
    result = {}
    status = "INITIALISED"

    def __init__(self, client_id, message):
        self.context_id = str(uuid.uuid4())
        self.client_id = client_id
        self.message = message
