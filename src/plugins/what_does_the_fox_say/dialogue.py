class WhatDoesTheFoxSayPlugin:

    def __init__(self, config):
        super(WhatDoesTheFoxSayPlugin, self).__init__()
        self.config = config

    # pylint: disable=no-self-use
    def generate(self, result):

        return {
            "text": result["response"],
            "voice": result["response"]
        }
