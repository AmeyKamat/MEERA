class OpenWeatherAPIPlugin:

    def __init__(self, config):
        super(OpenWeatherAPIPlugin, self).__init__()
        self.config = config

    # pylint: disable=no-self-use
    def generate(self, result):
        description = result["description"]
        temperature = result["temperature"]
        pressure = result["pressure"]
        humidity = result["humidity"]

        text = ("Weather is {0}, with temperature {1} "
                "deg. C, pressure {2} hPa and humidity {3}%").format(
                    description, temperature, pressure, humidity)
        voice = ("Weather is {0}, with temperature {1} "
                 "degree Centigrade, pressure {2} hPa and humidity {3}%").format(
                     description, temperature, pressure, humidity)

        return {
            "text": text,
            "voice": voice
        }
