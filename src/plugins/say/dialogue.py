class SayPlugin:

    def __init__(self, config):
        super(SayPlugin, self).__init__()
        self.config = config

    # pylint: disable=no-self-use
    def generate(self, result):

        return {
            "text": result["query"],
            "voice": result["query"]
        }
