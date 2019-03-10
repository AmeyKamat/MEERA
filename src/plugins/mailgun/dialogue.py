class MailgunPlugin:

    def __init__(self, config):
        super(MailgunPlugin, self).__init__()
        self.config = config

    # pylint: disable=no-self-use
    def generate(self, result):

        if result["success"] == 200:
            dialogue = "Message sent."
        else:
            dialogue = "Message was not sent."

        return {
            "text": dialogue,
            "voice": dialogue
        }
