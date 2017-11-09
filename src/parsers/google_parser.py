from lxml import html

from markups.search_markup import MarkupSearchResult, FullPath, Markup, MarkupWizardImage
from parser_result import ParserResult, Component
from parsers.parser import Parser


class GoogleParser(Parser):
    @staticmethod
    def get_index(parent, tag):
        index = 1
        for child in parent.iterchildren():
            if child == tag:
                return index
            if child.tag == tag.tag:
                index += 1
        return None

    @staticmethod
    def get_path(element):
        path = ""
        while element.tag != "html":
            path = "/" + element.tag + "[" + str(GoogleParser.get_index(element.getparent(), element)) + "]" + path
            element = element.getparent()
        path = "//html" + path
        return path

    def extract_search_result(self, element):
        search_result = MarkupSearchResult()
        search_result.alignment = "LEFT"
        search_result.page_url = FullPath(GoogleParser.get_path(element) + "/h3/a", "href")
        search_result.title = FullPath(GoogleParser.get_path(element) + "/h3/a", "string")
        search_result.snippet = FullPath(GoogleParser.get_path(element) + "/div/div/span", "strings")
        search_result.view_url = FullPath(GoogleParser.get_path(element) + "/div/div/div/cite", "string")
        return search_result

    def get_from_page(self, element, xpath, attr):
        tag = element.xpath(xpath)
        if len(tag) == 0:
            return ""
        tag = tag[0]
        attrs = ["href", "title", "style", "src"]
        if attr in attrs:
            if attr == "style":
                return tag.get("style").split("//")[1][:-2]
            return tag.get(attr)
        text = ""
        for i in tag.itertext():
            text += i
        return text

    def parse_search_result(self, element):
        search_result = Component()
        search_result.type = "SEARCH_RESULT"
        search_result.alignment = "LEFT"
        search_result.page_url = self.get_from_page(element, "./h3/a", "href")
        search_result.title = self.get_from_page(element, "./h3/a", "string")
        search_result.snippet = self.get_from_page(element, "./div/div/span", "string")
        search_result.view_url = self.get_from_page(element, "./div/div/div/cite", "string")
        return search_result

    def extract_wizard_image(self, element):
        wizard = MarkupWizardImage()
        wizard.alignment = "LEFT"
        img_list = element.xpath("./div[2]/div/div/div/div/div/div/div/div/div/a/g-img/img")
        for img in img_list:
            wizard.media_links.append(FullPath(GoogleParser.get_path(img), "title"))
        wizard.page_url = FullPath(GoogleParser.get_path(element) + "/div[1]/h3/a", "href")
        wizard.title = FullPath(GoogleParser.get_path(element) + "/div[1]/h3/a", "string")
        return wizard

    def parse_wizard_image(self, element):
        wizard = Component()
        wizard.type = "WIZARD"
        wizard.wizard_type = "WIZARD_IMAGE"
        wizard.alignment = "LEFT"
        img_list = element.xpath("./div[2]/div/div/div/div/div/div/div/div/div/a/g-img/img")
        wizard.media_links = list()
        for img in img_list:
            wizard.media_links.append(self.get_from_page(img, ".", "title"))
        wizard.page_url = self.get_from_page(element, "./div[1]/h3/a", "href")
        wizard.title = self.get_from_page(element, "./div[1]/h3/a", "string")
        return wizard

    def extract_markup(self, file_name):
        with open(file_name, "r") as file:
            tree = html.document_fromstring(file.read())
        markup = Markup()
        markup.file = file_name.split('/')[-1]
        block_list = tree.xpath("//html/body/div[7]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div/div")
        for block in block_list:
            document_list = block.xpath("./div/div/div/div")
            for document in document_list:
                result = self.extract_search_result(document)
                markup.add(result)
            wizard_image_list = block.xpath("./div/g-section-with-header")
            for wizard_image in wizard_image_list:
                if len(wizard_image.xpath("./div[1]/h3/a")) > 0:
                    result = self.extract_wizard_image(wizard_image)
                    markup.add(result)
        return markup

    def parse(self, string):
        tree = html.document_fromstring(string)
        parser_result = ParserResult()
        block_list = tree.xpath("//html/body/div[7]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div/div")
        for block in block_list:
            document_list = block.xpath("./div/div/div/div")
            for document in document_list:
                result = self.parse_search_result(document)
                parser_result.add(result)
            wizard_image_list = block.xpath("./div/g-section-with-header")
            for wizard_image in wizard_image_list:
                if len(wizard_image.xpath("./div[1]/h3/a")) > 0:
                    result = self.parse_wizard_image(wizard_image)
                    parser_result.add(result)
        return parser_result
