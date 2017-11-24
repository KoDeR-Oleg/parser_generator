from algorithms.selectors.selector import Selector


class BlackListSelector(Selector):
    def __init__(self):
        self.blacks = None

    def learn(self, algorithm, markup_list):
        self.blacks = list()
        for i in range(len(algorithm.types)):
            self.blacks.append(list())

        i = 0
        while i < len(markup_list):
            markup = markup_list[i]
            with open(algorithm.directory + markup.file, "r") as file:
                string = file.read()
            actual = algorithm.parse(string)
            tree = algorithm.tree_type.get_tree(string)
            expected = algorithm.get_substitution(tree, markup)
            if actual.count() == expected.count():
                if actual == expected:
                    continue
            for component in actual.components:
                if component not in expected.components:
                    element, element_path, element_type = algorithm.get_element_for_parser_component(component, tree)
                    self.add_black_for_element(algorithm, element, element_path, element_type, markup_list)
                    i -= 1
                    break
            i += 1
        return self

    def get_iter(self, **kwargs):
        node = kwargs['node']
        tree = kwargs['tree']
        lst = list()
        for i in range(len(node.indexes)):
            if self.is_not_black(tree, node.indexes[i]):
                lst.append(i)
        return lst

    def is_not_black(self, element, element_type):
        for pair in self.blacks[element_type]:
            if len(element.cssselect(pair[0] + "." + pair[1])) > 0:
                return False
        return True

    def add_black_for_element(self, algorithm, element, element_path, index_of_element_type, markup_list):
        list_pair = list()
        for tag in element.get_iter():
            for cl in tag.classes:
                list_pair.append((tag.tag, cl))
        list_flag = [True] * len(list_pair)

        for markup in markup_list:
            with open(algorithm.directory + markup.file, "r") as file:
                string = file.read()
            tree = algorithm.tree_type.get_tree(string)

            for component in markup.components:
                if isinstance(component, algorithm.types[index_of_element_type]):
                    block_list = tree.get_elements(component.title.drop_for_len(element_path.len()))
                    if len(block_list) > 0:
                        for i in range(len(list_pair)):
                            if list_flag[i] and len(block_list[0].cssselect(list_pair[i][0] + "." + list_pair[i][1])) > 0:
                                list_flag[i] = False

        for i in range(len(list_flag)):
            if list_flag[i]:
                if list_pair[i] not in self.blacks[index_of_element_type]:
                    self.blacks[index_of_element_type].append(list_pair[i])
                    break
