from lxml import html

from markups.search_markup import MarkupSearchResult, FullPath, Markup, MarkupWizardImage, MarkupWizardNews
from parser_result import ParserResult, Component
from parsers.parser import Parser


class GoogleParser_v2(Parser):
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
            path = "/" + element.tag + "[" + str(GoogleParser_v2.get_index(element.getparent(), element)) + "]" + path
            element = element.getparent()
        path = "//html" + path
        return path

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

    def extract_search_result(self, element):
        search_result = MarkupSearchResult()
        search_result.alignment = "LEFT"
        search_result.page_url = FullPath(GoogleParser_v2.get_path(element) + "/h3/a", "href")
        search_result.title = FullPath(GoogleParser_v2.get_path(element) + "/h3/a", "string")
        search_result.snippet = FullPath(GoogleParser_v2.get_path(element) + "/div/span", "strings")
        search_result.view_url = FullPath(GoogleParser_v2.get_path(element) + "/div/div/cite", "string")
        return search_result

    def parse_search_result(self, element):
        search_result = Component()
        search_result.type = "SEARCH_RESULT"
        search_result.alignment = "LEFT"
        search_result.page_url = self.get_from_page(element, "./h3/a", "href")
        search_result.title = self.get_from_page(element, "./h3/a", "string")
        search_result.snippet = self.get_from_page(element, "./div/span", "strings")
        search_result.view_url = self.get_from_page(element, "./div/div/cite", "string")
        return search_result

    def extract_wizard_image(self, element):
        wizard = MarkupWizardImage()
        wizard.alignment = "LEFT"
        img_list = element.xpath("./div/a/img")
        for img in img_list:
            wizard.media_links.append(FullPath(GoogleParser_v2.get_path(img), "src"))
        wizard.page_url = FullPath(GoogleParser_v2.get_path(element) + "/h3/a", "href")
        wizard.title = FullPath(GoogleParser_v2.get_path(element) + "/h3/a", "string")
        return wizard

    def parse_wizard_image(self, element):
        wizard = Component()
        wizard.type = "WIZARD"
        wizard.wizard_type = "WIZARD_IMAGE"
        wizard.alignment = "LEFT"
        img_list = element.xpath("./div/a/img")
        wizard.media_links = list()
        for img in img_list:
            wizard.media_links.append(self.get_from_page(img, ".", "src"))
        wizard.page_url = self.get_from_page(element, "./h3/a", "href")
        wizard.title = self.get_from_page(element, "./h3/a", "string")
        return wizard

    def extract_wizard_news(self, element):
        wizard = MarkupWizardNews()
        wizard.alignment = "LEFT"
        wizard.page_url = FullPath(GoogleParser_v2.get_path(element), "href")
        wizard.title = FullPath(GoogleParser_v2.get_path(element), "string")
        return wizard

    def parse_wizard_news(self, element):
        wizard = Component()
        wizard.type = "WIZARD"
        wizard.wizard_type = "WIZARD_NEWS"
        wizard.alignment = "LEFT"
        wizard.page_url = self.get_from_page(element, ".", "href")
        wizard.title = self.get_from_page(element, ".", "string")
        return wizard

    def extract_markup(self, file_name):
        with open(file_name, "r") as file:
            tree = html.document_fromstring(file.read())
        markup = Markup()
        markup.file = file_name.split('/')[-1]
        block_list = tree.xpath("//html/body/table/tbody/tr/td/div/div/div/div/ol/div")
        for block in block_list:
            document_list = block.xpath(".")
            for document in document_list:
                if len(document.xpath("./div/div/cite")) > 0:
                    result = self.extract_search_result(document)
                    markup.add(result)
            wizard_image_list = block.xpath(".")
            for wizard_image in wizard_image_list:
                if len(wizard_image.xpath("./div[1]/a")) > 0:
                    result = self.extract_wizard_image(wizard_image)
                    markup.add(result)
            wizard_news_list = block.xpath("./div/h3/a")
            for wizard_news in wizard_news_list:
                result = self.extract_wizard_news(wizard_news)
                markup.add(result)
        return markup

    def parse(self, string):
        tree = html.document_fromstring(string)
        parser_result = ParserResult()
        block_list = tree.xpath("//html/body/table/tbody/tr/td/div/div/div/div/ol/div")
        for block in block_list:
            document_list = block.xpath(".")
            for document in document_list:
                if len(document.xpath("./div/div/cite")) > 0:
                    result = self.parse_search_result(document)
                    parser_result.add(result)
            wizard_image_list = block.xpath(".")
            for wizard_image in wizard_image_list:
                if len(wizard_image.xpath("./div[1]/a")) > 0:
                    result = self.parse_wizard_image(wizard_image)
                    parser_result.add(result)
            wizard_news_list = block.xpath("./div/h3/a")
            for wizard_news in wizard_news_list:
                result = self.parse_wizard_news(wizard_news)
                parser_result.add(result)
        return parser_result
