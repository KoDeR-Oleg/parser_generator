from collections.abc import Iterator
from lxml import html
from trees.tree import Tree


class TagIterator(Iterator):
    def __init__(self, iter):
        self.iter = iter

    def __next__(self):
        try:
            return HTMLTree(html_tree=self.iter.__next__())
        except StopIteration:
            raise StopIteration


class HTMLTree(Tree):
    def __init__(self, **kwargs):
        if 'raw_page' in kwargs:
            self.tree = html.fromstring(kwargs['raw_page'])
        if 'html_tree' in kwargs:
            self.tree = kwargs['html_tree']
        self.tag = self.tree.tag
        self.classes = self.tree.classes

    def get_value(self, html_path):
        tags = self.tree.xpath(html_path.xpath)
        if len(tags) == 0:
            return None
        else:
            tag = tags[0]
        attrs = ["href", "title", "style", "src"]
        if html_path.attr in attrs:
            if html_path.attr == "style":
                if len(tag.get("style").split("//")) > 1:
                    return tag.get("style").split("//")[1][:-2]
                else:
                    return None
            return tag.get(html_path.attr)
        return tag.text_content()

    def get_elements(self, html_path):
        lst = self.tree.xpath(html_path.xpath)
        obj_lst = list()
        for i in range(len(lst)):
            obj_lst.append(HTMLTree(html_tree=lst[i]))
        return obj_lst

    def get_iter(self):
        return TagIterator(self.tree.iter())

    def cssselect(self, attribute):
        return self.tree.cssselect(attribute)
