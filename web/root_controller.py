from circuits.web import Controller

class Root(Controller):

	tpl = "./web/resources/index.html"

	def index(self):
		with open(self.tpl, 'r') as content_file:
			return content_file.read()
