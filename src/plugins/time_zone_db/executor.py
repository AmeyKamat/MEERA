import os
from datetime import datetime

import requests

from execution.exception import SelfLocationNotFoundException

class TimeZoneDBPlugin:

    def __init__(self, config):
        super(TimeZoneDBPlugin, self).__init__()
        self.config = config

    def execute(self, context):
        entities = context.nlp_analysis.entities

        if "location" in entities:
            latitude = entities["location"]["latitude"]
            longitude = entities["location"]["longitude"]
        elif "self-location" in entities:
            latitude = entities["self-location"]["latitude"]
            longitude = entities["self-location"]["longitude"]
        else:
            raise SelfLocationNotFoundException("Self Location Not Found")

        key_variable = self.config['key_variable']
        key = os.environ[key_variable]

        response = requests.get(self.config["time_url"], params={
            'key': key,
            'format': 'json',
            'by': 'position',
            'lat': latitude,
            'lng': longitude
        }).json()

        received_date_format = self.config["received_date_format"]
        required_date_format = self.config["required_date_format"]

        result = {}
        result["datetime"] = datetime.strptime(
            response["formatted"],
            received_date_format).strftime(required_date_format)

        if entities.get("location") is not None:
            location = entities["location"]["location"]
        else:
            location = None

        result["location"] = location if 'location' in entities else response["zoneName"]

        return result
