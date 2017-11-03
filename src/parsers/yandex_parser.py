from lxml import html

from markup import MarkupSearchResult, FullPath, Markup, MarkupWizardImage, MarkupWizardNews
from parsers.parser import Parser
from parsers.ideal_parser import IdealParser


class YandexParser(Parser):
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
            path = "/" + element.tag + "[" + str(YandexParser.get_index(element.getparent(), element)) + "]" + path
            element = element.getparent()
        path = "//html" + path
        return path

    def parse_rearch_result(self, element):
        search_result = MarkupSearchResult()
        search_result.alignment = "LEFT"
        search_result.page_url = FullPath(YandexParser.get_path(element) + "/h2/a", "href")
        search_result.title = FullPath(YandexParser.get_path(element) + "/h2/a", "string")
        search_result.snippet = FullPath(YandexParser.get_path(element) + "/div[2]/div[1]", "string")
        search_result.view_url = FullPath(YandexParser.get_path(element) + "/div[1]/div[1]/a[last()]", "href")
        return search_result

    def parse_wizard_image(self, element):
        wizard = MarkupWizardImage()
        wizard.alignment = "LEFT"
        img_list = element.xpath("./div[2]/div/div/div/a")
        for img in img_list:
            wizard.media_links.append(FullPath(YandexParser.get_path(img) + "/div[1]/div[1]", "style"))
        wizard.page_url = FullPath(YandexParser.get_path(element) + "/div[1]/h2/a", "href")
        wizard.title = FullPath(YandexParser.get_path(element) + "/div[1]/h2/a", "string")
        return wizard

    def parse_wizard_news(self, element):
        wizard = MarkupWizardNews()
        wizard.alignment = "LEFT"
        wizard.page_url = FullPath(YandexParser.get_path(element) + "/div[1]/h2/a[2]", "href")
        wizard.title = FullPath(YandexParser.get_path(element) + "/div[1]/h2/a[2]", "string")
        return wizard

    def extract_markup(self, file_name):
        with open(file_name, "r") as file:
            tree = html.document_fromstring(file.read())
        markup = Markup()
        markup.file = file_name
        block_list = tree.xpath("//html/body/div[3]/div/div[2]/div/div/ul/li/div")
        for block in block_list:
            if (len(block.xpath("./div[2]/div[2]")) > 0 and block.xpath("./div[2]/div[2]")[0].text == "реклама") or \
                    (len(block.xpath("./div[1]/div[2]")) > 0 and block.xpath("./div[1]/div[2]")[0].text == "реклама"):
                continue
            if len(block.xpath("./h2/a")) > 0:
                result = self.parse_rearch_result(block)
                markup.add(result)
            elif len(block.xpath("./div[1]/h2/a")) > 0 and len(block.xpath("./div[2]/div[@class='gallery']")) > 0:
                result = self.parse_wizard_image(block)
                markup.add(result)
            elif len(block.xpath("./div[1]/h2/a")) > 1:
                result = self.parse_wizard_news(block)
                markup.add(result)
        return markup

    def parse(self, file_name):
        ideal = IdealParser()
        return ideal.get_substitution(self.extract_markup(file_name))