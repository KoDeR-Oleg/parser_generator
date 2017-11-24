from collections.abc import Iterator
from trees.tree import Tree
import json
import jsonpath


class ChildIterator(Iterator):
    def __init__(self, iter):
        self.iter = iter

    def __next__(self):
        try:
            return JSONTree(self.iter.__next__())
        except StopIteration:
            raise StopIteration


class JSONTree(Tree):
    def __init__(self, json_tree):
        self.tree = json_tree
        self.tag = self.tree.__class__
        self.classes = list()

    def get_value(self, json_path):
        fields = jsonpath.jsonpath(self.tree, json_path.path)
        if len(fields) == 0:
            return None
        else:
            return fields[0]

    def get_elements(self, json_path):
        lst = jsonpath.jsonpath(self.tree, json_path.path)
        if not lst:
            return [self]
        obj_lst = list()
        for i in range(len(lst)):
            obj_lst.append(JSONTree(lst[i]))
        return obj_lst

    def get_iter(self):
        return ChildIterator(self.tree.__dict__)

    def cssselect(self, attribute):
        return list()

    @staticmethod
    def get_tree(raw_page):
        return JSONTree(json.loads(raw_page))
