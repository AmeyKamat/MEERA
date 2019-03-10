class BarclaycardUSPlugin:

    def __init__(self, config):
        super(BarclaycardUSPlugin, self).__init__()
        self.config = config

    # pylint: disable=no-self-use
    def generate(self, result):
        url = result["url"]
        text = "Here is your barclaycard application page.\n\n{0}".format(url)
        voice = "Here is your barclaycard application page."

        return {
            "text": text,
            "voice": voice,
            "link": url
        }
