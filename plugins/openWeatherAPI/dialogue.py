class OpenWeatherAPIPlugin(object):

	def __init__(self, config):
		super(OpenWeatherAPIPlugin, self).__init__()
		self.config = config

	def generate(self, intent, entities, result):
		description = result["description"]
		temperature = result["temperature"]
		pressure = result["pressure"]
		humidity = result["humidity"]

		return {
			"text": "Weather is {0}, with temperature {1} deg. C, pressure {2} hPa and humidity {3}%".format(description, temperature, pressure, humidity)
		}