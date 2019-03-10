import urllib

class WikipediaPlugin:

    def __init__(self, config):
        super(WikipediaPlugin, self).__init__()
        self.config = config

    def execute(self, context):
        entities = context.nlp_analysis.entities

        search_query = entities["query"]
        result = {}
        result["url"] = self.config["wikipedia_api"] + urllib.request.pathname2url(search_query)
        return result
