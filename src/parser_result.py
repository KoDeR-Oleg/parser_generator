import json


class Encoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class Component(object):
    def __init__(self):
        self.type = None
        self.alignment = None
        self.page_url = None
        self.title = None

    def __str__(self):
        return json.dumps(self, cls=Encoder, ensure_ascii=False)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ParserResult(object):
    def __init__(self):
        self.file = None
        self.components = list()

    def __str__(self):
        return json.dumps(self, cls=Encoder, ensure_ascii=False)

    def add(self, component):
        self.components.append(component)
