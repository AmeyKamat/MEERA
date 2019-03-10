import os

from configparser import ConfigParser
import requests

class LocationPreprocessor:

    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'component.ini'))

    def preprocess(self, location):
        try:
            url = self.config["location"]["api"]
            key_variable = self.config["location"]["key_variable"]
            key = os.environ[key_variable]

            response = requests.get(url, params={
                'address': location,
                'key': key
            })

            return {
                "location": location,
                "latitude": response.json()["results"][0]["geometry"]["location"]["lat"],
                "longitude": response.json()["results"][0]["geometry"]["location"]["lng"]
            }
        #pylint: disable=broad-except
        except Exception:
            return location
