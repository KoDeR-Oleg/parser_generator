class Component(object):
    def __init__(self):
        self.type = None
        self.alignment = None
        self.page_url = None
        self.title = None

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Analysis(object):
    def __init__(self):
        self.file = None
        self.components = list()

    def add(self, component):
        self.components.append(component)
