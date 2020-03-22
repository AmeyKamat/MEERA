import os

import requests

class NewsAPIPlugin:

    def __init__(self, config):
        super(NewsAPIPlugin, self).__init__()
        self.config = config

    def execute(self, context):
        entities = context.nlp_analysis.entities

        key_variable = self.config['key_variable']
        key = os.environ[key_variable]

        if "query" in entities:
            response = requests.get(self.config["news_url"], params={
                'q': entities["query"],
                'apiKey': key
            })
        else:
            response = requests.get(self.config["headlines_url"], params={
                'country': 'in',
                'apiKey': key
            })

        result = response.json()["articles"]
        response = {
            'result': result,
            'status': 'success'
        }
        return response
