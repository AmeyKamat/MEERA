class ChatInteractionManager:

    # pylint: disable=no-self-use
    def generate(self, nlpAnalysis):
        return {
            "text": nlpAnalysis.category,
            "voice": nlpAnalysis.category
        }
        