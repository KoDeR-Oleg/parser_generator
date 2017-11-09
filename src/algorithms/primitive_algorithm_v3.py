from lxml import html

from algorithms.algorithm import Algorithm
from markups.markup import FullPath
from parser_result import ParserResult, Component


class PrimitiveAlgorithm_v3(Algorithm):
    def __init__(self):
        self.samples = list()
        self.xpaths = list()
        self.types = list()
        self.block_xpath = None

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

    def parse_component(self, element, index):
        sample = self.samples[index]
        xpath = self.xpaths[index]
        t = self.types[index]
        block_xpath = self.extract_xpath(self.block_xpath)

        component = Component()
        for key in sample.__dict__.keys():
            if isinstance(sample.__dict__[key], str):
                component.__dict__[key] = sample.__dict__[key]
            elif isinstance(sample.__dict__[key], FullPath):
                key_xpath = self.extract_xpath(sample.__dict__[key].xpath)[len(block_xpath):]
                component.__dict__[key] = self.get_attr(element.xpath(self.combine_xpath(key_xpath, True)),
                                                        sample.__dict__[key].attr)
            elif isinstance(sample.__dict__[key], list):
                inner_xpath = self.extract_xpath(sample.__dict__[key][0].xpath)
                for elem in sample.__dict__[key]:
                    inner_xpath = self.great_common_prefix(inner_xpath, self.extract_xpath(elem.xpath))
                inner_xpath = self.combine_xpath(inner_xpath[len(block_xpath):], True)

                component.__dict__[key] = list()
                for elem in element.xpath(inner_xpath):
                    component.__dict__[key].append(self.get_attr(elem, sample.__dict__[key][0].attr))

        return component

    def learn(self, markup_list):
        self.block_xpath = self.extract_xpath(markup_list[0].components[0].title.xpath)
        for markup in markup_list:
            for component in markup.components:
                self.block_xpath = self.great_common_prefix(self.block_xpath, self.extract_xpath(component.title.xpath))

                f = False
                ind = 0
                for t in self.types:
                    if type(component) == t:
                        f = True
                        self.xpaths[ind] = self.great_common_prefix(self.xpaths[ind],
                                                                    self.extract_xpath(component.title.xpath))
                        break
                    ind += 1

                if not f:
                    self.xpaths.append(self.extract_xpath(component.title.xpath))
                    self.samples.append(component)
                    self.types.append(type(component))

                for key in component.__dict__.keys():
                    if isinstance(component.__dict__[key], FullPath):
                        self.block_xpath = self.great_common_prefix(self.block_xpath,
                                                                    self.extract_xpath(component.__dict__[key].xpath))

        for i in range(len(self.xpaths)):
            self.xpaths[i] = self.combine_xpath(self.xpaths[i][len(self.block_xpath):])
        self.block_xpath = self.combine_xpath(self.block_xpath)
        return self

    def parse(self, string):
        tree = html.document_fromstring(string)
        parser_result = ParserResult()

        block_list = tree.xpath(self.block_xpath)
        for block in block_list:
            for i in range(len(self.types)):
                if len(block.xpath("." + self.xpaths[i])) > 0:
                    result = self.parse_component(block, i)
                    parser_result.add(result)

        return parser_result
