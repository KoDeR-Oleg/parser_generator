import jsonpickle

from markups.markup import Markup
from parser_result import Component
from trees.json_path import JSONPath


class WikiMarkupComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self.type = "WIKI"
        self.alignment = "JSON"
        self.page_url = None
        self.title = None
        self.snippet = None

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        return jsonpickle.encode(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class WikiMarkup(Markup):
    def __init__(self):
        self.file = None
        self.components = list()

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        return jsonpickle.encode(self)

    def add(self, component):
        self.components.append(component)

    @staticmethod
    def get_TreePath_class():
        return JSONPath
