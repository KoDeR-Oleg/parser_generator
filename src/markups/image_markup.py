import jsonpickle
from markups.markup import Markup
from parser_result import Component


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
                return None
            else:
                tag = tags[0]
        else:
            tag = tags
        attrs = ["href", "title"]
        if attr in attrs:
            return tag.get(attr)
        text = ""
        for i in tag.itertext():
            text += i
        return text


class ImageMarkupComponent(Component, Markup):
    def __init__(self):
        Component.__init__(self)
        self.view_url = None
        self.type = "IMAGE"
        self.alignment = "LEFT"

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        return jsonpickle.encode(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def get_attr(tags, attr):
        return FullPath.get_attr(tags, attr)


class ImageMarkup(Markup):
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
