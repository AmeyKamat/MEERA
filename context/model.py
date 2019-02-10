class Context(object):

	clientId = None
	message = None
	status = "INITIALISED"

	def __init__(self, clientId, message):
		self.clientId = clientId
		self.message = message