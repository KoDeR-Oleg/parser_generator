from algorithms.selectors.selector import Selector


class SimpleSelector(Selector):
    def learn(self, algorithm, markup_list):
        return self

    def get_iter(self, **kwargs):
        node = kwargs['node']
        lst = list(range(len(node.indexes)))
        i = 0
        while i < len(lst) - 1:
            if len(node.samples[lst[i]].__dict__) < len(node.samples[lst[i + 1]].__dict__):
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                if i > 0:
                    i -= 1
            else:
                i += 1
        return lst
