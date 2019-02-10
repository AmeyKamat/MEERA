from circuits.web import Controller, expose

class Root(Controller):

	tpl = "./web/resources/index.html"

	@expose("/")
	def index(self):
		with open(self.tpl, 'r') as content_file:
			return content_file.read()

