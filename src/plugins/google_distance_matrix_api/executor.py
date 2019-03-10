import os

import requests

from execution.exception import SelfLocationNotFoundException

class GoogleDistanceMatrixAPIPlugin:

    def __init__(self, config):
        super(GoogleDistanceMatrixAPIPlugin, self).__init__()
        self.config = config

    def execute(self, context):
        entities = context.nlp_analysis.entities
        if "source-location" in entities:
            source_latitude = entities["source-location"]["latitude"]
            source_longitude = entities["source-location"]["longitude"]
        elif "self-location" in entities:
            source_latitude = entities["self-location"]["latitude"]
            source_longitude = entities["self-location"]["longitude"]
        else:
            raise SelfLocationNotFoundException("Self Location Not Found")

        if "destination-location" in entities:
            destination_latitude = entities["destination-location"]["latitude"]
            destination_longitude = entities["destination-location"]["longitude"]
        elif "self-location" in entities:
            destination_latitude = entities["self-location"]["latitude"]
            destination_longitude = entities["self-location"]["longitude"]
        else:
            raise SelfLocationNotFoundException("Self Location Not Found")

        key_variable = self.config['key_variable']
        key = os.environ[key_variable]

        response = requests.get(self.config["distance_url"], params={
            'origins': str(source_latitude) + "," + str(source_longitude),
            'destinations': str(destination_latitude) + "," + str(destination_longitude),
            'key': key
        }).json()

        result = {}
        result["duration"] = response["rows"][0]["elements"][0]["duration"]["text"]
        result["distance"] = response["rows"][0]["elements"][0]["distance"]["text"]
        result["source-location"] = entities.get("source-location")
        result["destination-location"] = entities.get("destination-location")

        return result
