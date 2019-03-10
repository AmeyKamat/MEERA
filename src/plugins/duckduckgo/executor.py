import urllib

import requests

class DuckDuckGoPlugin:

    def __init__(self, config):
        super(DuckDuckGoPlugin, self).__init__()
        self.config = config

    def execute(self, context):
        message = context.message
        entities = context.nlp_analysis.entities

        response = requests.get(self.config["question_api"], params={
            'q': message,
            'format': 'json'
        }).json()

        result = {}

        if response["Answer"] != "":
            result["answer"] = response["Answer"]
            result["source"] = "DuckDuckGo"
        elif response["Definition"] != "":
            result["answer"] = response["Definition"]
            result["source"] = response["DefinitionSource"]
        elif response["AbstractText"] != "":
            result["answer"] = response["AbstractText"]
            result["source"] = response["AbstractSource"]
        else:
            if "query" in entities:
                search_query = entities["query"]
            else:
                search_query = message
            result["url"] = self.config["search_api"] + urllib.request.pathname2url(search_query)

        return result
