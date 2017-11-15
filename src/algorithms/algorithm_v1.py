from lxml import html
from algorithms.algorithm import Algorithm
from parser_result import ParserResult, Component
import logging


class Algorithm_v1(Algorithm):
    def __init__(self, directory):
        self.samples = list()
        self.xpaths = list()
        self.types = list()
        self.blacks = list()
        self.block_xpath = None
        self.directory = directory

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

    def parse_component(self, element, index):
        sample = self.samples[index]
        xpath = self.xpaths[index]
        t = self.types[index]
        block_xpath = self.extract_xpath(self.block_xpath)

        component = Component()
        for key in sample.__dict__.keys():
            if isinstance(sample.__dict__[key], str):
                component.__dict__[key] = sample.__dict__[key]
            elif isinstance(sample.__dict__[key], list):
                inner_xpath = self.extract_xpath(sample.__dict__[key][0].xpath)
                for elem in sample.__dict__[key]:
                    inner_xpath = self.great_common_prefix(inner_xpath, self.extract_xpath(elem.xpath))
                inner_xpath = self.combine_xpath(inner_xpath[len(block_xpath):], True)

                component.__dict__[key] = None
                if len(element.xpath(inner_xpath)) > 0:
                    component.__dict__[key] = list()
                    for elem in element.xpath(inner_xpath):
                        component.__dict__[key].append(t.get_attr(elem, sample.__dict__[key][0].attr))
            else:
                key_xpath = self.extract_xpath(sample.__dict__[key].xpath)[len(block_xpath):]
                component.__dict__[key] = t.get_attr(element.xpath(self.combine_xpath(key_xpath, True)),
                                                     sample.__dict__[key].attr)
            if component.__dict__[key] is None:
                return None

        return component

    def get_substitution(self, tree, markup):
        parser_result = ParserResult()
        for markup_component in markup.components:
            parser_component = Component()
            for key in markup_component.__dict__.keys():
                if isinstance(markup_component.__dict__[key], str):
                    parser_component.__dict__[key] = markup_component.__dict__[key]
                elif isinstance(markup_component.__dict__[key], list):
                    parser_component.__dict__[key] = list()
                    for elem in markup_component.__dict__[key]:
                        parser_component.__dict__[key].append(type(markup).get_attr(tree.xpath(elem.xpath),
                                                              elem.attr))
                else:
                    parser_component.__dict__[key] = type(markup).get_attr(tree.xpath(markup_component.__dict__[key].xpath),
                                                                           markup_component.__dict__[key].attr)
            parser_result.add(parser_component)
        return parser_result

    def get_element_for_parser_component(self, parser_component, tree):
        block_list = tree.xpath(self.block_xpath)
        for block in block_list:
            for i in range(len(self.types)):
                if len(block.xpath("." + self.xpaths[i])) > 0:
                    result = self.parse_component(block, i)
                    if result is not None and result == parser_component:
                        return block, i
        return None, None

    def add_black_for_element(self, element, element_type, markup_list):
        list_pair = list()
        for tag in element.iter():
            for cl in tag.classes:
                list_pair.append((tag.tag, cl))
        list_flag = [True] * len(list_pair)

        list_block_xpath = self.extract_xpath(self.block_xpath)
        len_block_xpath = len(list_block_xpath)

        for markup in markup_list:
            with open(self.directory + markup.file, "r") as file:
                string = file.read()
            tree = html.fromstring(string)

            for component in markup.components:
                if isinstance(component, self.types[element_type]):
                    block = tree.xpath(self.combine_xpath(self.extract_xpath(component.title.xpath)[:len_block_xpath]))[0]
                    for i in range(len(list_pair)):
                        if list_flag[i] and len(block.cssselect(list_pair[i][0] + "." + list_pair[i][1])) > 0:
                            list_flag[i] = False

        for i in range(len(list_flag)):
            if list_flag[i]:
                if list_pair[i] not in self.blacks[element_type]:
                    self.blacks[element_type].append(list_pair[i])
                break

    def generate_black_lists(self, markup_list):
        self.blacks = list()
        for i in range(len(self.types)):
            self.blacks.append(list())

        for markup in markup_list:
            with open(self.directory + markup.file, "r") as file:
                string = file.read()
            actual = self.parse(string)
            tree = html.fromstring(string)
            expected = self.get_substitution(tree, markup)
            if actual.count() == expected.count():
                continue
            for component in actual.components:
                if component not in expected.components:
                    element, element_type = self.get_element_for_parser_component(component, tree)
                    self.add_black_for_element(element, element_type, markup_list)

    def learn(self, markup_list):
        self.samples = list()
        self.xpaths = list()
        self.types = list()
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
                    if isinstance(component.__dict__[key], list):
                        for e in component.__dict__[key]:
                            self.block_xpath = self.great_common_prefix(self.block_xpath,
                                                                        self.extract_xpath(e.xpath))
                    elif not isinstance(component.__dict__[key], str):
                        self.block_xpath = self.great_common_prefix(self.block_xpath,
                                                                    self.extract_xpath(component.__dict__[key].xpath))

        for i in range(len(self.xpaths)):
            self.xpaths[i] = self.combine_xpath(self.xpaths[i][len(self.block_xpath):])
        self.block_xpath = self.combine_xpath(self.block_xpath)

        self.generate_black_lists(markup_list)

        return self

    def is_not_black(self, element, element_type):
        for pair in self.blacks[element_type]:
            if len(element.cssselect(pair[0] + "." + pair[1])) > 0:
                return False
        return True

    def parse(self, raw_page):
        logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(funcname)s]  %(message)s',
                            level=logging.DEBUG, filename = 'algorithm_v1.log')
        logging.info("Start parse")
        tree = html.document_fromstring(raw_page)
        parser_result = ParserResult()

        block_list = tree.xpath(self.block_xpath)
        for block in block_list:
            for i in range(len(self.types)):
                if len(block.xpath("." + self.xpaths[i])) > 0 and self.is_not_black(block, i):
                    result = self.parse_component(block, i)
                    if result is not None:
                        parser_result.add(result)
                        break

        logging.debug("End parse")
        return parser_result
