from lxml import html


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

    def get_from_page(self, file_name, full_path):
        with open(file_name, "r") as file:
            tag = html.document_fromstring(file.read()).xpath(full_path.xpath)[0]
        if full_path.attr == "href" or full_path.attr == "title":
            return tag.get(full_path.attr)
        text = ""
        for i in tag.itertext():
            text += i
        return text

    def get_substitution(self, file_name):
        subst = dict()
        subst["type"] = self.type
        subst["alignment"] = self.alignment
        subst["page_url"] = self.get_from_page(file_name, self.page_url)
        subst["title"] = self.get_from_page(file_name, self.title)
        return subst


class SearchResult(Component):
    def __init__(self):
        Component.__init__(self)
        self.type = "SEARCH_RESULT"
        self.snippet = None
        self.view_url = None

    def get_substitution(self, file_name):
        subst = Component.get_substitution(self, file_name)
        subst["type"] = self.type
        subst["snippet"] = self.get_from_page(file_name, self.snippet)
        subst["view_url"] = self.get_from_page(file_name, self.view_url)
        return subst


class WizardImage(Component):
    def __init__(self):
        Component.__init__(self)
        self.type = "WIZARD"
        self.wizard_type = "WIZARD_IMAGE"
        self.media_links = list()

    def get_substitution(self, file_name):
        subst = Component.get_substitution(self, file_name)
        subst["type"] = self.type
        subst["wizard_type"] = self.wizard_type
        subst["media_links"] = list()
        for img in self.media_links:
            subst["media_links"].append(self.get_from_page(file_name, img))
        return subst


class Markup(object):
    def __init__(self):
        self.file = None
        self.components = list()

    def add(self, component):
        self.components.append(component)
