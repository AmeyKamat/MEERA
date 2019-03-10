class GoogleDistanceMatrixAPIPlugin:

    def __init__(self, config):
        super(GoogleDistanceMatrixAPIPlugin, self).__init__()
        self.config = config

    # pylint: disable=no-self-use
    def generate(self, result):
        distance = result["distance"]
        duration = result["duration"]

        if result["source-location"] is None:
            source_location = "here"
        else:
            source_location = result["source-location"]["location"]

        if result["destination-location"] is None:
            destination_location = "This place"
        else:
            destination_location = result["destination-location"]["location"]


        dialogue = "{0} is {1} away from {2}. It will take {3} by car.".format(
            destination_location, distance, source_location, duration)

        return {
            "text": dialogue,
            "voice": dialogue
        }
