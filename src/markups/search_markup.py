import jsonpickle

from markups.markup import Markup
from parser_result import Component


class SearchMarkupComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self.type = None
        self.alignment = None
        self.page_url = None
        self.title = None

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        return jsonpickle.encode(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class SearchMarkupSearchResult(SearchMarkupComponent):
    def __init__(self):
        SearchMarkupComponent.__init__(self)
        self.type = "SEARCH_RESULT"
        self.snippet = None
        self.view_url = None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class SearchMarkupAdv(SearchMarkupComponent):
    def __init__(self):
        SearchMarkupComponent.__init__(self)
        self.type = "ADV"
        self.snippet = None
        self.view_url = None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class SearchMarkupWizardImage(SearchMarkupComponent):
    def __init__(self):
        SearchMarkupComponent.__init__(self)
        self.type = "WIZARD"
        self.wizard_type = "WIZARD_IMAGE"
        self.media_links = list()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class SearchMarkupWizardNews(SearchMarkupComponent):
    def __init__(self):
        SearchMarkupComponent.__init__(self)
        self.type = "WIZARD"
        self.wizard_type = "WIZARD_NEWS"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class SearchMarkup(Markup):
    def __init__(self):
        self.file = None
        self.components = list()
        self.type = None

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        return jsonpickle.encode(self)

    def add(self, component):
        self.components.append(component)
