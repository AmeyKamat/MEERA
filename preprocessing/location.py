from configparser import ConfigParser
import requests

class LocationPreprocessor(object):

	config = ConfigParser()
	config.read("./preprocessing/component.ini")
	
	def preprocess(self, location):
		url = self.config["location"]["api"]
		key = self.config["location"]["key"]
		
		response = requests.get(url, params= {
			'address': location,
	    		'key': key
		})

		return {
			"location": location,
			"latitude": response.json()["results"][0]["geometry"]["location"]["lat"],
			"longitude": response.json()["results"][0]["geometry"]["location"]["lng"]
		}