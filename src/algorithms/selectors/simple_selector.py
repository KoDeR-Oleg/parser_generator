from algorithms.selectors.selector import Selector
from collections.abc import Iterator


class IndexIterator(Iterator):
    def __init__(self, lst):
        self.lst = lst

    def __next__(self):
        try:
            return self.lst.__next__()
        except StopIteration:
            raise StopIteration


class SimpleSelector(Selector):
    def __init__(self, algorithm, markup_list):
        pass

    def get_iter(self, **kwargs):
        node = kwargs['node']
        lst = range(len(node.indexes))
        i = 0
        while i < len(lst) - 1:
            if len(node.samples[lst[i]].__dict__) < len(node.samples[lst[i + 1]].__dict__):
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                if i > 0: i -= 1
            else: i += 1
        return IndexError(lst)
