class ChatInteractionManager(object):

	def generate(self, nlpAnalysis):
		return {
			"text": nlpAnalysis.category,
			"voice": nlpAnalysis.category
		}
		