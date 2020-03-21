class SayPlugin:

    def __init__(self, config):
        super(SayPlugin, self).__init__()
        self.config = config

    # pylint: disable=no-self-use
    def execute(self, context):
        entities = context.nlp_analysis.entities

        result = {}
        result["query"] = entities["query"]

        response = {
            'result': result,
            'status': 'success'
        }
        return response
