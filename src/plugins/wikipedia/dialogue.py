class WikipediaPlugin:

    def __init__(self, config):
        super(WikipediaPlugin, self).__init__()
        self.config = config

    # pylint: disable=no-self-use
    def generate(self, result):
        url = result["url"]
        text = "This is what I found.\n\n{0}".format(url)
        voice = "This is what I found."

        return {
            "text": text,
            "voice": voice,
            "link": url
        }
