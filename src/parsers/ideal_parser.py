import jsonpickle
from lxml import html
from parser_result import ParserResult, Component
from parsers.parser import Parser
import os


class IdealParser(Parser):
    def get_from_page(self, tree, full_path):
        tag = tree.xpath(full_path.xpath)
        if len(tag) == 0:
            return ""
        tag = tag[0]
        attrs = ["href", "title", "style", "src"]
        if full_path.attr in attrs:
            if full_path.attr == "style":
                return tag.get("style").split("//")[1][:-2]
            return tag.get(full_path.attr)
        text = ""
        for i in tag.itertext():
            text += i
        return text

    def get_substitution_search_result(self, tree, document, subst):
        subst.type = document.type
        subst.snippet = self.get_from_page(tree, document.snippet)
        subst.view_url = self.get_from_page(tree, document.view_url)
        return subst

    def get_substitution_wizard_image(self, tree, wizard, subst):
        subst.type = wizard.type
        subst.wizard_type = wizard.wizard_type
        subst.media_links = list()
        for img in wizard.media_links:
            subst.media_links.append(self.get_from_page(tree, img))
        return subst

    def get_substitution_wizard_news(self, tree, wizard, subst):
        subst.type = wizard.type
        subst.wizard_type = wizard.wizard_type
        return subst

    def get_substitution_component(self, tree, component):
        subst = Component()
        subst.type = component.type
        subst.alignment = component.alignment
        subst.page_url = self.get_from_page(tree, component.page_url)
        subst.title = self.get_from_page(tree, component.title)
        if component.type == "SEARCH_RESULT":
            subst = self.get_substitution_search_result(tree, component, subst)
        if component.type == "WIZARD":
            if component.wizard_type == "WIZARD_IMAGE":
                subst = self.get_substitution_wizard_image(tree, component, subst)
            if component.wizard_type == "WIZARD_NEWS":
                subst = self.get_substitution_wizard_news(tree, component, subst)
        return subst

    def get_substitution(self, markup, element=None):
        with open(markup.file, "r") as file:
            tree = html.document_fromstring(file.read())
        if element is None:
            parser_result = ParserResult()
            for component in markup.components:
                parser_result.add(self.get_substitution_component(tree, component))
            return parser_result
        else:
            return self.get_substitution_component(tree, markup.components[element])

    def parse(self, string, directory="../golden"):
        file_names = list()
        for root, dirs, files in os.walk(directory):
            file_names += [os.path.join(root, name) for name in files if name[-4:] == "html"]
        for file_name in file_names:
            with open(file_name, "r") as file:
                if string == file.read():
                    with open(file_name[:-4] + "json", "r") as file_json:
                        parser_result = jsonpickle.decode(file_json.read())
                        return parser_result
        return None

    def extract_markup(self, file_name):
        with open(file_name, "r") as file:
            markup = jsonpickle.decode(file.read())
        return markup
