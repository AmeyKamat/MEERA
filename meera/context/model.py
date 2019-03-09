import uuid

class Context:

    clientId = None
    contextId = None
    conversationId = None
    message = None
    nlpAnalysis = None
    previousContext = None
    selfLocation = None
    interaction = {}
    result = {}
    status = "INITIALISED"

    def __init__(self, clientId, message):
        self.contextId = str(uuid.uuid4())
        self.clientId = clientId
        self.message = message