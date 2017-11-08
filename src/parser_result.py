import jsonpickle


class Component(object):
    def __init__(self):
        self.type = None
        self.alignment = None
        self.page_url = None
        self.title = None

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4, ensure_ascii=False)
        return jsonpickle.encode(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ParserResult(object):
    def __init__(self):
        self.components = list()

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4, ensure_ascii=False)
        return jsonpickle.encode(self)

    def add(self, component):
        self.components.append(component)
