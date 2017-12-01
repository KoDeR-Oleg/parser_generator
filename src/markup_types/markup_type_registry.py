from trees.html_tree import HTMLTree
from trees.json_tree import JSONTree

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class MarkupTypeRegistry:

    def get_tree(self, markup_type, raw_page):
        if markup_type == "HTMLTree":
            return HTMLTree(raw_page=raw_page)
        elif markup_type == "JSONTree":
            return JSONTree(raw_page=raw_page)
