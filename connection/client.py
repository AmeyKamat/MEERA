class Client(object):
	id = ""
	name = ""
	type = ""
	socket = None

	def __init__(self, id, name, type):
		self.id = id
		self.name = name
		self.type = type
		