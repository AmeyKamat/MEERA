class GoogleDistanceMatrixAPIPlugin(object):

	def __init__(self, config):
		super(GoogleDistanceMatrixAPIPlugin, self).__init__()
		self.config = config

	def generate(self, result):
		distance = result["distance"]
		duration = result["duration"]

		if result["source-location"] is None:
			sourceLocation = "here"
		else:
			sourceLocation = result["source-location"]["location"]

		if result["destination-location"] is None:
			destinationLocation = "This place"
		else:
			destinationLocation = result["destination-location"]["location"]
		

		dialogue = "{0} is {1} away from {2}. It will take {3} by car.".format(destinationLocation, distance, sourceLocation, duration)

		return {
			"text": dialogue,
			"voice": dialogue
		}