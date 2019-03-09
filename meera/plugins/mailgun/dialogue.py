import requests

class MailgunPlugin(object):

	def __init__(self, config):
		super(MailgunPlugin, self).__init__()
		self.config = config

	def generate(self, result):
		
		if result["success"] == 200:
			dialogue = "Message sent."
		else:
			dialogue = "Message was not sent."

		return {
			"text": dialogue,
			"voice": dialogue
		}

	
		