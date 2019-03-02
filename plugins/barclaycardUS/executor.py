class BarclaycardUSPlugin(object):

	def __init__(self, config):
		super(BarclaycardUSPlugin, self).__init__()
		self.config = config

	def execute(self, context):
		entities = context.nlpAnalysis.entities
		
		campaign = entities["campaign"]
		cell = entities["cell"]

		result = {}
		result["url"] = self.config["barclaycard_url"].format(campaign, cell)
		
		return result