import os

import requests

class GoogleSelfLocationPlugin:

    def __init__(self, config):
        super(GoogleSelfLocationPlugin, self).__init__()
        self.config = config

    def execute(self, context):
        entities = context.nlp_analysis.entities

        if "self-location" not in entities:
            return {'status': 'need-location'}

        self_location = entities["self-location"]

        key_variable = self.config['key_variable']
        key = os.environ[key_variable]

        response = requests.get(self.config["geocoding_url"], params={
            'latlng': str(self_location["latitude"]) + "," + str(self_location["longitude"]),
            'key': key
        }).json()

        result = {}
        result["location"] = response["results"][0]["formatted_address"]

        response = {
            'result': result,
            'status': 'success'
        }
        return response
