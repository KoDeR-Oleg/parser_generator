import jsonpickle
from parser_result import Component
from markups.markup import Markup


class CinemaComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self.snippet = None
        self.year = None
        self.type = "Cinema"
        self.alignment = "LEFT"

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        return jsonpickle.encode(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class CinemaMarkup(Markup):
    def __init__(self):
        self.file = None
        self.components = list()
        self.type = None

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        return jsonpickle.encode(self)

    def add(self, component):
        self.components.append(component)
