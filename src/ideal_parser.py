from lxml import html
from parser import Parser
from parser_result import ParserResult, Component


class IdealParser(Parser):
    def get_from_page(self, tree, full_path):
        tag = tree.xpath(full_path.xpath)[0]
        attrs = ["href", "title", "style", "src"]
        if full_path.attr in attrs:
            if full_path.attr == "style":
                return tag.get("style").split("//")[1][:-2]
            return tag.get(full_path.attr)
        text = ""
        for i in tag.itertext():
            text += i
        return text

    def get_substitution_document(self, tree, document, subst):
        subst.type = document.type
        subst.snippet = self.get_from_page(tree, document.snippet)
        subst.view_url = self.get_from_page(tree, document.view_url)
        return subst

    def get_substitution_wizard(self, tree, wizard, subst):
        subst.type = wizard.type
        subst.wizard_type = wizard.wizard_type
        subst.media_links = list()
        for img in wizard.media_links:
            subst.media_links.append(self.get_from_page(tree, img))
        return subst

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
