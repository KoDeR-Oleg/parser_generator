import json

from lxml import html

from markup import Markup, MarkupSearchResult, MarkupWizardImage, FullPath, MarkupWizardNews
from parser_result import ParserResult, Component
from parsers.parser import Parser


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

    def extract_search_result(self, document):
        result = MarkupSearchResult()
        result.type = document['type']
        result.snippet = FullPath(**document['snippet'])
        result.view_url = FullPath(**document['view_url'])
        return result

    def get_substitution_search_result(self, tree, document, subst):
        subst.type = document.type
        subst.snippet = self.get_from_page(tree, document.snippet)
        subst.view_url = self.get_from_page(tree, document.view_url)
        return subst

    def extract_wizard_image(self, wizard):
        result = MarkupWizardImage()
        result.media_links = list()
        for img in wizard['media_links']:
            result.media_links.append(FullPath(**img))
        return result

    def extract_wizard_news(self, wizard):
        result = MarkupWizardNews()
        return result

    def extract_wizard(self, wizard):
        result = None
        if wizard['wizard_type'] == "WIZARD_IMAGE":
            result = self.extract_wizard_image(wizard)
        elif wizard['wizard_type'] == "WIZARD_NEWS":
            result = self.extract_wizard_news(wizard)
        result.type = wizard['type']
        result.wizard_type = wizard['wizard_type']
        return result

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

    def extract_markup_component(self, component):
        result = None
        if component['type'] == "SEARCH_RESULT":
            result = self.extract_search_result(component)
        if component['type'] == "WIZARD":
            result = self.extract_wizard(component)
        result.type = component['type']
        result.alignment = component['alignment']
        result.page_url = FullPath(**component['page_url'])
        result.title = FullPath(**component['title'])
        return result

    def parse_component(self, component):
        result = Component()
        result.__dict__ = component
        return result

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

    def parse(self, file_name):
        with open(file_name, "r") as file:
            js = json.load(file)
        parser_result = ParserResult()
        for component in js['components']:
            parser_result.add(self.parse_component(component))
        return parser_result

    def extract_markup(self, file_name):
        with open(file_name, "r") as file:
            js = json.load(file)
        markup = Markup()
        markup.file = js['file']
        for component in js['components']:
            markup.add(self.extract_markup_component(component))
        return markup
