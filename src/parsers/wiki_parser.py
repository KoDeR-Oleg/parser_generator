import json
import jsonpath
from markups.wiki_markup import WikiMarkup, WikiMarkupComponent
from trees.json_path import JSONPath
from parser_result import ParserResult, Component
from parsers.parser import Parser


class WikiParser(Parser):
    def __init__(self):
        self.block_path = "$.query.search"

    def parse_component(self, element):
        component = Component()
        component.type = "WIKI"
        component.alignment = "JSON"
        component.page_url = jsonpath.jsonpath(element, "$.pageid")[0]
        component.title = jsonpath.jsonpath(element, "$.title")[0]
        component.snippet = jsonpath.jsonpath(element, "$.snippet")[0]
        return component

    def extract_component(self, ind):
        component = WikiMarkupComponent()
        component.page_url = JSONPath(self.block_path + "[" + str(ind) + "].pageid")
        component.title = JSONPath(self.block_path + "[" + str(ind) + "].title")
        component.snippet = JSONPath(self.block_path + "[" + str(ind) + "].snippet")
        return component

    def extract_markup(self, file_name):
        with open(file_name, "r") as file:
            obj = json.load(file)
        markup = WikiMarkup()
        markup.file = file_name.split('/')[-1]
        markup.type = "JSONTree"
        block_list = jsonpath.jsonpath(obj, self.block_path)[0]
        for ind in range(len(block_list)):
            result = self.extract_component(ind)
            markup.add(result)
        return markup

    def parse(self, raw_page):
        obj = json.loads(raw_page)
        parser_result = ParserResult()
        block_list = jsonpath.jsonpath(obj, self.block_path)[0]
        for block in block_list:
            result = self.parse_component(block)
            parser_result.add(result)
        return parser_result
