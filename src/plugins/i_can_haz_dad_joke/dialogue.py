class ICanHazDadJokePlugin:

    def __init__(self, config):
        super(ICanHazDadJokePlugin, self).__init__()
        self.config = config

    # pylint: disable=no-self-use
    def generate(self, result):

        return {
            "text": result["joke"],
            "voice": result["joke"]
        }
