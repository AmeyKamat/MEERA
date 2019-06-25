import os
from circuits.web import Controller

from markdown2 import Markdown

from definitions import PROJECT_DIR

class Root(Controller):

    def __init__(self):
        super(Root, self).__init__()
        markdowner = Markdown(extras=["fenced-code-blocks", "tables", "task_list"])

        with open(os.path.join(PROJECT_DIR, 'README.md'), 'r') as readme_file:
            self.content = markdowner.convert(readme_file.read())

    def index(self):
        return self.content
