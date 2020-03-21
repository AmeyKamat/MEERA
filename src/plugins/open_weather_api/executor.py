import os

import requests

class OpenWeatherAPIPlugin:

    def __init__(self, config):
        super(OpenWeatherAPIPlugin, self).__init__()
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
            return {'status': 'need-location'}

        key_variable = self.config['key_variable']
        key = os.environ[key_variable]

        response = requests.get(self.config["weather_url"], params={
            'lat': latitude,
            'lon': longitude,
            'units': "metric",
            'APPID': key
        }).json()
        print(response)

        result = {}
        result["description"] = response["weather"][0]["description"]
        result["temperature"] = response["main"]["temp"]
        result["pressure"] = response["main"]["pressure"]
        result["humidity"] = response["main"]["humidity"]

        response = {
            'result': result,
            'status': 'success'
        }

        return result
