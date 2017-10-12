class FullPath(object):
    def __init__(self, xpath, attr):
        self.xpath = xpath
        self.attr = attr

    def __str__(self):
        return self.xpath + "." + self.attr


class Component(object):
    def __init__(self):
        self.type = None
        self.alignment = None
        self.page_url = None
        self.title = None

    def __str__(self):
        return str(self.__dict__)


class SearchResult(Component):
    def __init__(self):
        Component.__init__(self)
        self.type = "SEARCH_RESULT"
        self.snippet = None
        self.view_url = None

    def __repr__(self):
        pass


class WizardImage(Component):
    def __init__(self):
        Component.__init__(self)
        self.type = "WIZARD"
        self.wizard_type = "WIZARD_IMAGE"
        self.media_links = list()


class Markup(object):
    def __init__(self):
        self.file = None
        self.components = list()

    def add(self, component):
        self.components.append(component)
