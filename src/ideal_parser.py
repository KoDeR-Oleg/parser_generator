from lxml import html
from parser import Parser
from parser_result import ParserResult, Component
import json


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

    def parse_document(self, document, result):
        result.type = document['type']
        result.snippet = document['snippet']
        result.view_url = document['view_url']
        return result

    def get_substitution_document(self, tree, document, subst):
        subst.type = document.type
        subst.snippet = self.get_from_page(tree, document.snippet)
        subst.view_url = self.get_from_page(tree, document.view_url)
        return subst

    def parse_wizard(self, wizard, result):
        result.type = wizard['type']
        result.wizard_type = wizard['wizard_type']
        result.media_links = list()
        for img in wizard['media_links']:
            result.media_links.append(img)
        return result

    def get_substitution_wizard(self, tree, wizard, subst):
        subst.type = wizard.type
        subst.wizard_type = wizard.wizard_type
        subst.media_links = list()
        for img in wizard.media_links:
            subst.media_links.append(self.get_from_page(tree, img))
        return subst

    def parse_component(self, component):
        result = Component()
        result.type = component['type']
        result.alignment = component['alignment']
        result.page_url = component['page_url']
        result.title = component['title']
        if result.type == "SEARCH_RESULT":
            result = self.parse_document(component, result)
        if result.type == "WIZARD":
            result = self.parse_wizard(component, result)
        return result

    def get_substitution_component(self, tree, component):
        subst = Component()
        subst.type = component.type
        subst.alignment = component.alignment
        subst.page_url = self.get_from_page(tree, component.page_url)
        subst.title = self.get_from_page(tree, component.title)
        if component.type == "SEARCH_RESULT":
            subst = self.get_substitution_document(tree, component, subst)
        if component.type == "WIZARD":
            subst = self.get_substitution_wizard(tree, component, subst)
        return subst

    def get_substitution(self, markup, element=None):
        with open(markup.file, "r") as file:
            tree = html.document_fromstring(file.read())
        if element is None:
            parser_result = ParserResult()
            parser_result.file = markup.file
            for component in markup.components:
                parser_result.add(self.get_substitution_component(tree, component))
            return parser_result
        else:
            return self.get_substitution_component(tree, markup.components[element])

    def parse(self, file_name):
        with open(file_name, "r") as file:
            js = json.load(file)
        parser_result = ParserResult()
        parser_result.file = js['file']
        for component in js['components']:
            parser_result.add(self.parse_component(component))
        return parser_result
