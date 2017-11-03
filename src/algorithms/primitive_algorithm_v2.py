from lxml import html

from algorithms.algorithm import Algorithm
from parser_result import ParserResult, Component


class PrimitiveAlgorithm_v2(Algorithm):
    def __init__(self):
        self.sample_search_result = None
        self.sample_wizard_image = None
        self.sample_wizard_news = None
        self.block_xpath = None
        self.search_result_xpath = None
        self.wizard_image_xpath = None
        self.wizard_news_xpath = None

    def get_index(self, parent, tag):
        index = 1
        for child in parent.iterchildren():
            if child == tag:
                return index
            if child.tag == tag.tag:
                index += 1
        return None

    def get_path(self, element):
        path = ""
        while element.tag != "html":
            path = "/" + element.tag + "[" + str(self.get_index(element.getparent(), element)) + "]" + path
            element = element.getparent()
        path = "//html" + path
        return path

    def extract_xpath(self, xpath):
        extract_list = xpath.split("/")
        while extract_list[0] == "":
            extract_list = extract_list[1:]
        for i in range(len(extract_list)):
            if extract_list[i][-1] != "]":
                extract_list[i] = (extract_list[i], "0")
            else:
                tlist = extract_list[i].split("[")
                extract_list[i] = (tlist[0], tlist[1][:-1])
        return extract_list

    def combine_xpath(self, extract_list, relative=False):
        xpath = ""
        if relative:
            xpath = "."
        if len(extract_list) > 0 and extract_list[0][0] == "html":
            xpath = "/"
        for item in extract_list:
            xpath += "/" + item[0]
            if str(item[1]) > "0":
                xpath += "[" + str(item[1]) + "]"
        return xpath

    def great_common_prefix(self, xpath1, xpath2):
        common_list = []
        for i in range(min(len(xpath1), len(xpath2))):
            if xpath1[i][0] != xpath2[i][0]:
                break
            if xpath1[i][1] == xpath2[i][1]:
                common_list.append(xpath1[i])
            else:
                common_list.append((xpath1[i][0], 0))
        return common_list

    def get_attr(self, tags, attr):
        if isinstance(tags, list):
            if len(tags) == 0:
                return ""
            else:
                tag = tags[0]
        else:
            tag = tags
        attrs = ["href", "title", "style", "src"]
        if attr in attrs:
            if attr == "style":
                return tag.get("style").split("//")[1][:-2]
            return tag.get(attr)
        text = ""
        for i in tag.itertext():
            text += i
        return text

    def parse_search_result(self, element, block_xpath, sample):
        search_result = Component()
        search_result.type = "SEARCH_RESULT"
        search_result.alignment = "LEFT"

        block_xpath = self.extract_xpath(block_xpath)

        page_url_xpath = self.extract_xpath(sample.page_url.xpath)[len(block_xpath):]
        search_result.page_url = self.get_attr(element.xpath(self.combine_xpath(page_url_xpath, True)), sample.page_url.attr)

        title_xpath = self.extract_xpath(sample.title.xpath)[len(block_xpath):]
        search_result.title = self.get_attr(element.xpath(self.combine_xpath(title_xpath, True)), sample.title.attr)

        snippet_xpath = self.extract_xpath(sample.snippet.xpath)[len(block_xpath):]
        search_result.snippet = self.get_attr(element.xpath(self.combine_xpath(snippet_xpath, True)), sample.snippet.attr)

        view_url_xpath = self.extract_xpath(sample.view_url.xpath)[len(block_xpath):]
        search_result.view_url = self.get_attr(element.xpath(self.combine_xpath(view_url_xpath, True)), sample.view_url.attr)
        return search_result

    def parse_wizard_image(self, element, block_xpath, sample):
        wizard = Component()
        wizard.type = "WIZARD"
        wizard.wizard_type = "WIZARD_IMAGE"
        wizard.alignment = "LEFT"

        block_xpath = self.extract_xpath(block_xpath)

        inner_xpath = self.extract_xpath(sample.media_links[0].xpath)
        for img in sample.media_links:
            inner_xpath = self.great_common_prefix(inner_xpath, self.extract_xpath(img.xpath))
        inner_xpath = self.combine_xpath(inner_xpath[len(block_xpath):], True)

        wizard.media_links = list()
        img_list = element.xpath(inner_xpath)
        for img in img_list:
            wizard.media_links.append(self.get_attr(img, sample.media_links[0].attr))

        page_url_xpath = self.extract_xpath(sample.page_url.xpath)[len(block_xpath):]
        wizard.page_url = self.get_attr(element.xpath(self.combine_xpath(page_url_xpath, True)), sample.page_url.attr)

        title_xpath = self.extract_xpath(sample.title.xpath)[len(block_xpath):]
        wizard.title = self.get_attr(element.xpath(self.combine_xpath(title_xpath, True)), sample.title.attr)
        return wizard

    def parse_wizard_news(self, element, block_xpath, sample):
        wizard = Component()
        wizard.type = "WIZARD"
        wizard.wizard_type = "WIZARD_NEWS"
        wizard.alignment = "LEFT"

        block_xpath = self.extract_xpath(block_xpath)

        page_url_xpath = self.extract_xpath(sample.page_url.xpath)[len(block_xpath):]
        wizard.page_url = self.get_attr(element.xpath(self.combine_xpath(page_url_xpath, True)), sample.page_url.attr)

        title_xpath = self.extract_xpath(sample.title.xpath)[len(block_xpath):]
        wizard.title = self.get_attr(element.xpath(self.combine_xpath(title_xpath, True)), sample.title.attr)
        return wizard

    def learn(self, markup_list):
        self.block_xpath = self.extract_xpath(markup_list[0].components[0].title.xpath)
        self.search_result_xpath = []
        self.sample_search_result = None
        self.wizard_image_xpath = []
        self.sample_wizard_image = None
        self.wizard_news_xpath = []
        self.sample_wizard_news = None
        for markup in markup_list:
            for component in markup.components:
                self.block_xpath = self.great_common_prefix(self.block_xpath, self.extract_xpath(component.title.xpath))
                if component.type == "SEARCH_RESULT":
                    self.block_xpath = self.great_common_prefix(self.block_xpath,
                                                                self.extract_xpath(component.snippet.xpath))
                    if self.search_result_xpath == []:
                        self.search_result_xpath = self.extract_xpath(component.title.xpath)
                        self.sample_search_result = component
                    else:
                        self.search_result_xpath = self.great_common_prefix(self.search_result_xpath,
                                                                            self.extract_xpath(component.title.xpath))
                if component.type == "WIZARD" and component.wizard_type == "WIZARD_IMAGE":
                    if self.wizard_image_xpath == []:
                        self.wizard_image_xpath = self.extract_xpath(component.title.xpath)
                        self.sample_wizard_image = component
                    else:
                        self.wizard_image_xpath = self.great_common_prefix(self.wizard_image_xpath,
                                                                           self.extract_xpath(component.title.xpath))

                if component.type == "WIZARD" and component.wizard_type == "WIZARD_NEWS":
                    if self.wizard_news_xpath == []:
                        self.wizard_news_xpath = self.extract_xpath(component.title.xpath)
                        self.sample_wizard_news = component
                    else:
                        self.wizard_news_xpath = self.great_common_prefix(self.wizard_news_xpath,
                                                                           self.extract_xpath(component.title.xpath))

        self.search_result_xpath = self.combine_xpath(self.search_result_xpath[len(self.block_xpath):])
        self.wizard_image_xpath = self.combine_xpath(self.wizard_image_xpath[len(self.block_xpath):])
        self.wizard_news_xpath = self.combine_xpath(self.wizard_news_xpath[len(self.block_xpath):])
        self.block_xpath = self.combine_xpath(self.block_xpath)
        return self

    def parse(self, string):
        tree = html.document_fromstring(string)
        parser_result = ParserResult()

        block_list = tree.xpath(self.block_xpath)
        for block in block_list:
            if len(block.xpath("." + self.search_result_xpath)) > 0 and self.sample_search_result is not None:
                result = self.parse_search_result(block, self.block_xpath, self.sample_search_result)
                parser_result.add(result)
            elif len(block.xpath("." + self.wizard_image_xpath)) > 0 and self.sample_wizard_image is not None:
                result = self.parse_wizard_image(block, self.block_xpath, self.sample_wizard_image)
                parser_result.add(result)
            elif len(block.xpath("." + self.wizard_news_xpath)) > 0 and self.sample_wizard_news is not None:
                result = self.parse_wizard_news(block, self.block_xpath, self.sample_wizard_news)
                parser_result.add(result)

        return parser_result
