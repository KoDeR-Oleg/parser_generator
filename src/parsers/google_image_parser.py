from lxml import html

from markups.image_markup import ImageMarkup, ImageMarkupComponent, HTMLPath
from parser_result import ParserResult, Component
from parsers.parser import Parser


class GoogleImageParser(Parser):
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
            path = "/" + element.tag + "[" + str(GoogleImageParser.get_index(element.getparent(), element)) + "]" + path
            element = element.getparent()
        path = "//html" + path
        return path

    def get_from_page(self, element, xpath, attr):
        tag = element.xpath(xpath)
        if len(tag) == 0:
            return ""
        tag = tag[0]
        attrs = ["href", "title"]
        if attr in attrs:
            return tag.get(attr)
        text = ""
        for i in tag.itertext():
            text += i
        return text

    def parse_image(self, element):
        image = Component()
        image.type = "IMAGE"
        image.alignment = "LEFT"
        image.page_url = self.get_from_page(element, "./a", "href")
        image.view_url = self.get_from_page(element, "./cite", "title")
        image.title = self.get_from_page(element, ".", "string")
        return image

    def extract_image(self, element):
        image = ImageMarkupComponent()
        image.page_url = HTMLPath(GoogleImageParser.get_path(element) + "/a", "href")
        image.view_url = HTMLPath(GoogleImageParser.get_path(element) + "/cite", "title")
        image.title = HTMLPath(GoogleImageParser.get_path(element), "string")
        return image

    def extract_markup(self, file_name):
        with open(file_name, "r") as file:
            tree = html.document_fromstring(file.read())
        markup = ImageMarkup()
        markup.file = file_name.split('/')[-1]
        block_list = tree.xpath("//html/body/table/tbody/tr/td/div/div/div/div/table/tr/td")
        for block in block_list:
            image_list = block.xpath(".")
            for image in image_list:
                if len(image.xpath("./a")) > 0 and len(image.xpath("./cite")) > 0:
                    result = self.extract_image(image)
                    markup.add(result)
        return markup

    def parse(self, raw_page):
        tree = html.document_fromstring(raw_page)
        parser_result = ParserResult()
        block_list = tree.xpath("//html/body/table/tbody/tr/td/div/div/div/div/table/tr/td")
        for block in block_list:
            image_list = block.xpath(".")
            for image in image_list:
                if len(image.xpath("./a")) > 0 and len(image.xpath("./cite")) > 0:
                    result = self.parse_image(image)
                    parser_result.add(result)
        return parser_result
