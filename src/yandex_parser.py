from lxml import html
from markup import MarkupSearchResult, FullPath, Markup, MarkupWizardImage
from parser import Parser


class YandexParser(Parser):
    def parse_document(self, element):
        document = MarkupSearchResult()
        document.alignment = "LEFT"
        document.page_url = FullPath(Parser.get_path(element) + "/h2/a", "href")
        document.title = FullPath(Parser.get_path(element) + "/h2/a", "string")
        document.snippet = FullPath(Parser.get_path(element) + "/div[2]/div[1]", "string")
        document.view_url = FullPath(Parser.get_path(element) + "/div[1]/div[1]/a[last()]", "href")
        return document

    def parse_wizard_image(self, element):
        wizard = MarkupWizardImage()
        wizard.alignment = "LEFT"
        img_list = element.xpath("./div[2]/div/div/div/a")
        for img in img_list:
            wizard.media_links.append(FullPath(Parser.get_path(img) + "/div[1]/div[1]", "style"))
        wizard.page_url = FullPath(Parser.get_path(element) + "/div[1]/h2/a", "href")
        wizard.title = FullPath(Parser.get_path(element) + "/div[1]/h2/a", "string")
        return wizard

    def extract_markup(self, file_name):
        with open(file_name, "r") as file:
            tree = html.document_fromstring(file.read())
        markup = Markup()
        markup.file = file_name
        block_list = tree.xpath("//html/body/div[3]/div[1]/div[2]/div[1]/div[1]/ul/li/div")
        for block in block_list:
            if len(block.xpath("./div[2]/div[2]")) > 0 and block.xpath("./div[2]/div[2]")[0].text == "реклама":
                continue
            if len(block.xpath("./h2/a")) > 0:
                result = self.parse_document(block)
                markup.add(result)
            elif len(block.xpath("./div[1]/h2/a")) > 0 and len(block.xpath("./div[2]/div[@class='gallery']")):
                result = self.parse_wizard_image(block)
                markup.add(result)
        return markup
