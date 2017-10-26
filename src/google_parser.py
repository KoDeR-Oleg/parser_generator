from lxml import html
from markup import MarkupSearchResult, FullPath, Markup, MarkupWizardImage
from parser import Parser
from ideal_parser import IdealParser


class GoogleParser(Parser):
    def parse_document(self, element):
        document = MarkupSearchResult()
        document.alignment = "LEFT"
        document.page_url = FullPath(Parser.get_path(element) + "/h3/a", "href")
        document.title = FullPath(Parser.get_path(element) + "/h3/a", "string")
        document.snippet = FullPath(Parser.get_path(element) + "/div/div/span", "strings")
        document.view_url = FullPath(Parser.get_path(element) + "/div/div/div/cite", "string")
        return document

    def parse_wizard_image(self, element):
        wizard = MarkupWizardImage()
        wizard.alignment = "LEFT"
        img_list = element.xpath("./div[2]/div/div/div/div/div/div/div/div/div/a/g-img/img")
        for img in img_list:
            wizard.media_links.append(FullPath(Parser.get_path(img), "title"))
        wizard.page_url = FullPath(Parser.get_path(element) + "/div[1]/h3/a", "href")
        wizard.title = FullPath(Parser.get_path(element) + "/div[1]/h3/a", "string")
        return wizard

    def extract_markup(self, file_name):
        with open(file_name, "r") as file:
            tree = html.document_fromstring(file.read())
        markup = Markup()
        markup.file = file_name
        block_list = tree.xpath("//html/body/div[7]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div/div")
        for block in block_list:
            document_list = block.xpath("./div/div/div/div")
            for document in document_list:
                result = self.parse_document(document)
                markup.add(result)
            wizard_image_list = block.xpath("./div/g-section-with-header")
            for wizard_image in wizard_image_list:
                if len(wizard_image.xpath("./div[1]/h3/a")) > 0:
                    result = self.parse_wizard_image(wizard_image)
                    markup.add(result)
        return markup

    def parse(self, file_name):
        ideal = IdealParser()
        return ideal.get_substitution(self.extract_markup(file_name))
