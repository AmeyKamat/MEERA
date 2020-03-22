import urllib

class GoogleSearchPlugin:

    def __init__(self, config):
        super(GoogleSearchPlugin, self).__init__()
        self.config = config

    def execute(self, context):
        message = context.message
        entities = context.nlp_analysis.entities

        if "query" in entities:
            search_query = entities["query"]
        else:
            search_query = message

        result = {}
        result["url"] = self.config["search_api"] + urllib.request.pathname2url(search_query)

        response = {
            'result': result,
            'status': 'success'
        }
        return response
