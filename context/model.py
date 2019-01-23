class Context(object):

	message = None
	status = "INITIALISED"

	def __init__(self, message):
		self.message = message