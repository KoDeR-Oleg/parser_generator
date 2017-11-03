from lxml import html

from markup import MarkupSearchResult, FullPath, Markup, MarkupWizardImage, MarkupWizardNews
from parsers.ideal_parser import IdealParser
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

    def parse_search_result(self, element):
        search_result = MarkupSearchResult()
        search_result.alignment = "LEFT"
        search_result.page_url = FullPath(GoogleParser_v2.get_path(element) + "/h3/a", "href")
        search_result.title = FullPath(GoogleParser_v2.get_path(element) + "/h3/a", "string")
        search_result.snippet = FullPath(GoogleParser_v2.get_path(element) + "/div/span", "strings")
        search_result.view_url = FullPath(GoogleParser_v2.get_path(element) + "/div/div/cite", "string")
        return search_result

    def parse_wizard_image(self, element):
        wizard = MarkupWizardImage()
        wizard.alignment = "LEFT"
        img_list = element.xpath("./div/a/img")
        for img in img_list:
            wizard.media_links.append(FullPath(GoogleParser_v2.get_path(img), "src"))
        wizard.page_url = FullPath(GoogleParser_v2.get_path(element) + "/h3/a", "href")
        wizard.title = FullPath(GoogleParser_v2.get_path(element) + "/h3/a", "string")
        return wizard

    def parse_wizard_news(self, element):
        wizard = MarkupWizardNews()
        wizard.alignment = "LEFT"
        wizard.page_url = FullPath(GoogleParser_v2.get_path(element), "href")
        wizard.title = FullPath(GoogleParser_v2.get_path(element), "string")
        return wizard

    def extract_markup(self, file_name):
        with open(file_name, "r") as file:
            tree = html.document_fromstring(file.read())
        markup = Markup()
        markup.file = file_name
        block_list = tree.xpath("//html/body/table/tbody/tr/td/div/div/div/div/ol/div")
        for block in block_list:
            document_list = block.xpath(".")
            for document in document_list:
                if len(document.xpath("./div/div/cite")) > 0:
                    result = self.parse_search_result(document)
                    markup.add(result)
            wizard_image_list = block.xpath(".")
            for wizard_image in wizard_image_list:
                if len(wizard_image.xpath("./div[1]/a")) > 0:
                    result = self.parse_wizard_image(wizard_image)
                    markup.add(result)
            wizard_news_list = block.xpath("./div/h3/a")
            for wizard_news in wizard_news_list:
                result = self.parse_wizard_news(wizard_news)
                markup.add(result)
        return markup

    def parse(self, file_name):
        ideal = IdealParser()
        return ideal.get_substitution(self.extract_markup(file_name))


#test = GoogleParser_v2()
#print(str(test.extract_markup("../google/golden/35.html")))