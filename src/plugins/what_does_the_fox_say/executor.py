import random

class WhatDoesTheFoxSayPlugin:

    def __init__(self, config):
        super(WhatDoesTheFoxSayPlugin, self).__init__()
        self.config = config
        self.fox_sounds = [
            "Ring-ding-ding-ding-dingeringeding!",
            "Wa-pa-pa-pa-pa-pa-pow!",
            "Hatee-hatee-hatee-ho!",
            "Joff-tchoff-tchoffo-tchoffo-tchoff!",
            "Jacha-chacha-chacha-chow!",
            "Fraka-kaka-kaka-kaka-kow!",
            "A-hee-ahee ha-hee!",
            "A-oo-oo-oo-ooo!"
        ]

    # pylint: disable=unused-argument
    def execute(self, context):
        result = {}
        result["response"] = random.choice(self.fox_sounds)
        return result
