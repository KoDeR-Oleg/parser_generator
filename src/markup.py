from lxml import html
from analysis import Component, Analysis


class FullPath(object):
    def __init__(self, xpath, attr):
        self.xpath = xpath
        self.attr = attr

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return self.xpath + "." + self.attr


class MarkupComponent(object):
    def __init__(self):
        self.type = None
        self.alignment = None
        self.page_url = None
        self.title = None

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_from_page(self, tree, full_path):
        tag = tree.xpath(full_path.xpath)[0]
        if full_path.attr == "href" or full_path.attr == "title" or full_path.attr == "style":
            if full_path.attr == "style":
                return tag.get("style").split("//")[1][:-2]
            return tag.get(full_path.attr)
        text = ""
        for i in tag.itertext():
            text += i
        return text

    def get_substitution(self, tree):
        subst = Component()
        subst.type = self.type
        subst.alignment = self.alignment
        subst.page_url = self.get_from_page(tree, self.page_url)
        subst.title = self.get_from_page(tree, self.title)
        return subst


class MarkupSearchResult(MarkupComponent):
    def __init__(self):
        MarkupComponent.__init__(self)
        self.type = "SEARCH_RESULT"
        self.snippet = None
        self.view_url = None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_substitution(self, tree):
        subst = MarkupComponent.get_substitution(self, tree)
        subst.type = self.type
        subst.snippet = self.get_from_page(tree, self.snippet)
        subst.view_url = self.get_from_page(tree, self.view_url)
        return subst


class MarkupWizardImage(MarkupComponent):
    def __init__(self):
        MarkupComponent.__init__(self)
        self.type = "WIZARD"
        self.wizard_type = "WIZARD_IMAGE"
        self.media_links = list()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_substitution(self, tree):
        subst = MarkupComponent.get_substitution(self, tree)
        subst.type = self.type
        subst.wizard_type = self.wizard_type
        subst.media_links = list()
        for img in self.media_links:
            subst.media_links.append(self.get_from_page(tree, img))
        return subst


class Markup(object):
    def __init__(self):
        self.file = None
        self.components = list()

    def add(self, component):
        self.components.append(component)

    def get_substitution(self, element = None):
        with open(self.file, "r") as file:
            tree = html.document_fromstring(file.read())
        if element is None:
            analysis = Analysis()
            analysis.file = self.file
            for component in self.components:
                analysis.add(component.get_substitution(tree))
            return analysis
        else:
            return self.components[element].get_substitution(tree)
