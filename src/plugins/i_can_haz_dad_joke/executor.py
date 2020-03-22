import requests

class ICanHazDadJokePlugin:

    def __init__(self, config):
        super(ICanHazDadJokePlugin, self).__init__()
        self.config = config

    # pylint: disable=unused-argument
    def execute(self, context):
        response = requests.get(self.config["joke_url"], headers={
            "User-Agent": self.config["user_agent"],
            "accept": "application/json"
        }).json()

        result = {}
        result["joke"] = response["joke"]

        response = {
            'result': result,
            'status': 'success'
        }
        return response
