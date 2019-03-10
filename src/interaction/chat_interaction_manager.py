class ChatInteractionManager:

    # pylint: disable=no-self-use
    def generate(self, nlp_analysis):
        return {
            "text": nlp_analysis.category,
            "voice": nlp_analysis.category
        }
        