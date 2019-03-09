import os

import requests

from execution.exception import SelfLocationNotFoundException

class GoogleDistanceMatrixAPIPlugin(object):

	def __init__(self, config):
		super(GoogleDistanceMatrixAPIPlugin, self).__init__()
		self.config = config

	def execute(self, context):
		entities = context.nlpAnalysis.entities
		if "source-location" in entities:
			sourceLatitude = entities["source-location"]["latitude"]
			sourceLongitude = entities["source-location"]["longitude"]
		elif "self-location" in entities:
			sourceLatitude = entities["self-location"]["latitude"]
			sourceLongitude = entities["self-location"]["longitude"]
		else:
			raise SelfLocationNotFoundException("Self Location Not Found")

		if "destination-location" in entities:
			destinationLatitude = entities["destination-location"]["latitude"]
			destinationLongitude = entities["destination-location"]["longitude"]
		elif "self-location" in entities:
			destinationLatitude = entities["self-location"]["latitude"]
			destinationLongitude = entities["self-location"]["longitude"]
		else:
			raise SelfLocationNotFoundException("Self Location Not Found")
		
		key_variable = self.config['key_variable']
		key = os.environ[key_variable]

		response = requests.get(self.config["distance_url"], params= {
				'origins': str(sourceLatitude) + "," + str(sourceLongitude),
				'destinations': str(destinationLatitude) + "," + str(destinationLongitude),
	    		'key': key
		}).json()

		result = {}
		result["duration"] = response["rows"][0]["elements"][0]["duration"]["text"]
		result["distance"] = response["rows"][0]["elements"][0]["distance"]["text"]
		result["source-location"] = entities.get("source-location")
		result["destination-location"] = entities.get("destination-location")

		return result