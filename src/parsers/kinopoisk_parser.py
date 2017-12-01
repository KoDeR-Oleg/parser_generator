from lxml import html

from markups.cinema_markup import CinemaComponent, CinemaMarkup
from parser_result import ParserResult, Component
from parsers.parser import Parser
from trees.html_path import HTMLPath


class KinopoiskParser(Parser):
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
            path = "/" + element.tag + "[" + str(KinopoiskParser.get_index(element.getparent(), element)) + "]" + path
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

    def parse_cinema(self, element):
        cinema = Component()
        cinema.type = "Cinema"
        cinema.alignment = "LEFT"
        cinema.page_url = self.get_from_page(element, "./div[2]/p/a", "href")
        cinema.title = self.get_from_page(element, "./div[2]/p/a", "string")
        cinema.snippet = self.get_from_page(element, "./div[2]/span[2]", "string")
        cinema.year = self.get_from_page(element, "./div[2]/p/span", "string")
        return cinema

    def extract_cinema(self, element):
        cinema = CinemaComponent()
        cinema.page_url = HTMLPath(KinopoiskParser.get_path(element) + "/div[2]/p/a", "href")
        cinema.title = HTMLPath(KinopoiskParser.get_path(element) + "/div[2]/p/a", "string")
        cinema.snippet = HTMLPath(KinopoiskParser.get_path(element) + "/div[2]/span[2]", "string")
        cinema.year = HTMLPath(KinopoiskParser.get_path(element) + "/div[2]/p/span", "string")
        return cinema

    def extract_markup(self, file_name):
        with open(file_name, "r") as file:
            tree = html.document_fromstring(file.read())
        markup = CinemaMarkup()
        markup.file = file_name.split('/')[-1]
        markup.type = "HTMLTree"
        block_list = tree.xpath("//html/body/div/div/table/tr/td[1]/div/div/div")
        for block in block_list:
            cinema_list = block.xpath(".")
            for cinema in cinema_list:
                if len(cinema.xpath("./div[2]/p/a")) > 0 and len(cinema.xpath("./div[2]/p/span")) > 0:
                    result = self.extract_cinema(cinema)
                    markup.add(result)
        return markup

    def parse(self, raw_page):
        tree = html.document_fromstring(raw_page)
        parser_result = ParserResult()
        block_list = tree.xpath("///html/body/div/div/table/tr/td[1]/div/div/div")
        for block in block_list:
            cinema_list = block.xpath(".")
            for cinema in cinema_list:
                if len(cinema.xpath("./div[2]/p/a")) > 0 and len(cinema.xpath("./div[2]/p/span")) > 0:
                    result = self.parse_cinema(cinema)
                    parser_result.add(result)
        return parser_result
