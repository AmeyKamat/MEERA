class BarclaycardUSPlugin:

    def __init__(self, config):
        super(BarclaycardUSPlugin, self).__init__()
        self.config = config

    def execute(self, context):
        entities = context.nlp_analysis.entities

        campaign = entities["campaign"]
        cell = entities["cell"]

        result = {}
        result["url"] = self.config["barclaycard_url"].format(campaign, cell)
        response = {
            'result': result,
            'status': 'success'
        }

        return response
