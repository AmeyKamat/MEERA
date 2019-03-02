import requests
import urllib
from datetime import datetime

from execution.exception import SelfLocationNotFoundException

class TimeZoneDBPlugin(object):

	def __init__(self, config):
		super(TimeZoneDBPlugin, self).__init__()
		self.config = config

	def execute(self, context):
		entities = context.nlpAnalysis.entities
		
		if "location" in entities:
			latitude = entities["location"]["latitude"]
			longitude = entities["location"]["longitude"]
		elif "self-location" in entities:
			latitude = entities["self-location"]["latitude"]
			longitude = entities["self-location"]["longitude"]
		else:
			raise SelfLocationNotFoundException("Self Location Not Found")
			
		response = requests.get(self.config["time_url"], params= {
			'key': self.config["key"],
			'format': 'json',
			'by': 'position',
			'lat': latitude,
			'lng': longitude
		}).json()

		receivedDateFormat = self.config["received_date_format"]
		requiredDateFormat = self.config["required_date_format"]

		result = {}
		result["datetime"] = datetime.strptime(response["formatted"], receivedDateFormat).strftime(requiredDateFormat)
		result["location"] = entities["location"]["location"] if 'location' in entities else response["zoneName"]

		return result