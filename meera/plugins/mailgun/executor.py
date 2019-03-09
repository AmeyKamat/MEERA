import os

import requests

class MailgunPlugin(object):

	def __init__(self, config):
		super(MailgunPlugin, self).__init__()
		self.config = config

	def execute(self, context):
		entities = context.nlpAnalysis.entities
		
		sender = self.config["from_email"]
		receiver = entities["email"]
		subject = self.config["subject"]
		message = entities["email-body"]
		body = self.config["body_template"].format(message)

		domian_variable = self.config['domain_variable']
		domain = os.environ[domain_variable]

		key_variable = self.config['key_variable']
		key = os.environ[key_variable]

		response = requests.post(self.config["mail_url"].format(domain=domain, key=key), data = {
			'from': sender,
			'to': receiver,
			'subject': subject,
			'html': body
		}).status_code

		return {"success": response}

	
		