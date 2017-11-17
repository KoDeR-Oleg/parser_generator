import jsonpickle
from markups.markup import Markup, TreePath
from parser_result import Component
from lxml import html


class FullPath(TreePath):
    def __init__(self, xpath, attr):
        self.xpath = xpath
        self.attr = attr

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return self.xpath + "." + self.attr

    def get_value(self, tree):
        tags = tree.xpath(self.xpath)
        if len(tags) == 0:
            return None
        else:
            tag = tags[0]
        attrs = ["href", "title", "style", "src"]
        if self.attr in attrs:
            if self.attr == "style":
                if len(tag.get("style").split("//")) > 1:
                    return tag.get("style").split("//")[1][:-2]
                else:
                    return None
            return tag.get(self.attr)
        return tag.text_content()

    def split_xpath(self):
        extract_list = self.xpath.split("/")
        while extract_list[0] == "":
            extract_list = extract_list[1:]
        for i in range(len(extract_list)):
            if extract_list[i][-1] != "]":
                extract_list[i] = (extract_list[i], "0")
            else:
                tlist = extract_list[i].split("[")
                extract_list[i] = (tlist[0], tlist[1][:-1])
        return extract_list

    def merge_xpath(self, extract_list, relative=False):
        xpath = ""
        if relative:
            xpath = "."
        if len(extract_list) > 0 and extract_list[0][0] == "html":
            xpath = "/"
        if len(extract_list) > 0 and extract_list[0][0] == ".":
            xpath = "."
            extract_list = extract_list[1:]
        for item in extract_list:
            xpath += "/" + item[0]
            if str(item[1]) != "0":
                xpath += "[" + str(item[1]) + "]"
        return xpath

    def get_common_prefix(self, tree_path, in_block=False):
        xpath1 = self.split_xpath()
        xpath2 = tree_path.split_xpath()
        common_list = []
        for i in range(min(len(xpath1), len(xpath2))):
            if xpath1[i][0] != xpath2[i][0]:
                break
            if xpath1[i][1] == xpath2[i][1]:
                common_list.append(xpath1[i])
            else:
                if in_block:
                    break
                common_list.append((xpath1[i][0], 0))
        xpath = self.merge_xpath(common_list)
        attr = self.attr
        if attr != tree_path.attr:
            attr = None
        return FullPath(xpath, attr)

    def get_relative_path(self, tree_path):
        return FullPath(self.merge_xpath(self.split_xpath()[len(tree_path.split_xpath()):], True), self.attr)

    def get_elements(self, tree):
        return tree.xpath(self.xpath)

    def len(self):
        lst = self.split_xpath()
        if len(lst) == 1 and lst[0][0] == ".":
            return 0
        return len(lst)

    def drop_for_len(self, len):
        return FullPath(self.merge_xpath(self.split_xpath()[:len]), None)

    def concat(self, tree_path):
        result = FullPath(self.xpath, tree_path.attr)
        if tree_path.xpath[0] == '.':
            result.xpath += tree_path.xpath[1:]
        else:
            result.xpath += tree_path.xpath
        return result

    @staticmethod
    def get_tree(raw_page):
        return html.fromstring(raw_page)


class ImageMarkupComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self.view_url = None
        self.type = "IMAGE"
        self.alignment = "LEFT"

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        return jsonpickle.encode(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ImageMarkup:
    def __init__(self):
        self.file = None
        self.components = list()

    def __str__(self):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        return jsonpickle.encode(self)

    def add(self, component):
        self.components.append(component)

    @staticmethod
    def get_TreePath_class():
        return FullPath