import jsonpickle
from markups.markup import Markup


class FullPath(Markup):
    def __init__(self, xpath, attr):
        self.xpath = xpath
        self.attr = attr

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return self.xpath + "." + self.attr

    @staticmethod
    def get_attr(tags, attr):
        if isinstance(tags, list):
            if len(tags) == 0:
                return ""
            else:
                tag = tags[0]
        else:
            tag = tags
        attrs = ["href", "title", "style", "src"]
        if attr in attrs:
            if attr == "style":
                return tag.get("style").split("//")[1][:-2]
            return tag.get(attr)
        text = ""
        for i in tag.itertext():
            text += i
        return text


class SearchMarkupComponent(Markup):
    def __init__(self):
        self.type = None
        self.alignment = None
        self.page_url = None
        self.title = None

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        return jsonpickle.encode(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def get_attr(tags, attr):
        return FullPath.get_attr(tags, attr)


class SearchMarkupSearchResult(SearchMarkupComponent):
    def __init__(self):
        SearchMarkupComponent.__init__(self)
        self.type = "SEARCH_RESULT"
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

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        return jsonpickle.encode(self)

    def add(self, component):
        self.components.append(component)

    @staticmethod
    def get_attr(tags, attr):
        return FullPath.get_attr(tags, attr)