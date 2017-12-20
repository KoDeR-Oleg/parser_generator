from trees.tree_path import TreePath


class HTMLPath(TreePath):
    def __init__(self, xpath, attr):
        self.xpath = xpath
        self.attr = attr

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return self.xpath + "." + self.attr

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
        return HTMLPath(xpath, attr)

    def get_relative_path(self, tree_path):
        return HTMLPath(self.merge_xpath(self.split_xpath()[len(tree_path.split_xpath()):], True), self.attr)

    def len(self):
        lst = self.split_xpath()
        if len(lst) == 1 and lst[0][0] == ".":
            return 0
        return len(lst)

    def drop_for_len(self, len):
        return HTMLPath(self.merge_xpath(self.split_xpath()[:len]), None)

    def concat(self, tree_path):
        result = HTMLPath(self.xpath, tree_path.attr)
        if tree_path.xpath[0] == '.':
            result.xpath += tree_path.xpath[1:]
        else:
            result.xpath += tree_path.xpath
        return result
