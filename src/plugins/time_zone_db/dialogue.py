class TimeZoneDBPlugin:

    def __init__(self, config):
        super(TimeZoneDBPlugin, self).__init__()
        self.config = config

    # pylint: disable=no-self-use
    def generate(self, result):

        datetime = result["datetime"]
        location = result["location"]

        return {
            "text": "It is {} in {}".format(datetime, location),
            "voice": "It is {} in {}".format(datetime, location)
        }
