from algorithms.algorithm import Algorithm
from parser_result import ParserResult, Component
from markups.markup import TreePath
import copy
import logging


class Node:
    def __init__(self):
        self.indexes = list()
        self.samples = list()
        self.treepaths = list()


class Algorithm_v2(Algorithm):
    def __init__(self, directory):
        self.root = None
        self.samples = list()
        self.types = list()
        self.blacks = list()
        self.directory = directory
        self.markup_type = None
        logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(funcName)s]  %(message)s',
                            level=logging.DEBUG, filename='algorithm_v1.log')

    def get_substitution(self, tree, markup):
        logging.info("Start")
        parser_result = ParserResult()
        for markup_component in markup.components:
            parser_component = Component()
            for key in markup_component.__dict__.keys():
                field = markup_component.__dict__[key]
                if isinstance(field, str):
                    parser_component.__dict__[key] = field
                elif isinstance(field, list):
                    parser_component.__dict__[key] = list()
                    for elem in field:
                        parser_component.__dict__[key].append(elem.get_value(tree))
                else:
                    parser_component.__dict__[key] = field.get_value(tree)
            parser_result.add(parser_component)
        logging.info("End")
        return parser_result

    def get_element_for_parser_component(self, parser_component, tree):
        return self.dfs(self.root, tree, parser_component, True)

    def add_black_for_element(self, element, element_path, index_of_element_type, markup_list):
        logging.info("Start")
        list_pair = list()
        for tag in element.iter():
            for cl in tag.classes:
                list_pair.append((tag.tag, cl))
        list_flag = [True] * len(list_pair)

        for markup in markup_list:
            with open(self.directory + markup.file, "r") as file:
                string = file.read()
            tree = markup.get_TreePath_class().get_tree(string)

            for component in markup.components:
                if isinstance(component, self.types[index_of_element_type]):
                    block_list = component.title.drop_for_len(element_path.len()).get_elements(tree)# element_path.get_elements(tree)
                    # block = component.title.drop_for_len(self.block_treepath.len()).get_elements(tree)[0]
                    if len(block_list) > 0:
                        for i in range(len(list_pair)):
                            if list_flag[i] and len(block_list[0].cssselect(list_pair[i][0] + "." + list_pair[i][1])) > 0:
                                list_flag[i] = False

        for i in range(len(list_flag)):
            if list_flag[i]:
                if list_pair[i] not in self.blacks[index_of_element_type]:
                    self.blacks[index_of_element_type].append(list_pair[i])
                    break
        logging.info("End")

    def generate_black_lists(self, markup_list):
        logging.info("Start")
        self.blacks = list()
        for i in range(len(self.types)):
            self.blacks.append(list())

        i = 0
        while i < len(markup_list):
            markup = markup_list[i]
            logging.debug("Markup for " + markup.file)
            with open(self.directory + markup.file, "r") as file:
                string = file.read()
            actual = self.parse(string)
            tree = markup.get_TreePath_class().get_tree(string)
            expected = self.get_substitution(tree, markup)
            logging.debug("Actual count = " + str(actual.count()) + ", Expected count = " + str(expected.count()))
            if actual.count() == expected.count():
                if actual == expected:
                    continue
            for component in actual.components:
                if component not in expected.components:
                    logging.debug(component == expected.components[0])
                    element, element_path, element_type = self.get_element_for_parser_component(component, tree)
                    self.add_black_for_element(element, element_path, element_type, markup_list)
                    i -= 1
                    break
                else:
                    logging.debug(str(component))
            i += 1

        logging.info("End")

    def get_relative_component(self, component, treepath):
        for key in component.__dict__.keys():
            if isinstance(component.__dict__[key], TreePath):
                component.__dict__[key] = component.__dict__[key].get_relative_path(treepath)
            elif isinstance(component.__dict__[key], list):
                for i in range(len(component.__dict__[key])):
                    component.__dict__[key][i] = component.__dict__[key][i].get_relative_path(treepath)
        return component

    def add_component(self, node, treepath, index_of_type, sample):
        if treepath.len() <= 1:
            if index_of_type not in node.indexes:
                node.indexes.append(index_of_type)
                node.samples.append(sample)
            return
        for i in range(len(node.treepaths)):
            common_path = treepath.get_common_prefix(node.treepaths[i][0])
            if common_path.len() > 0:
                if common_path.len() == node.treepaths[i][0].len():
                    node.treepaths[i] = (common_path, node.treepaths[i][1])
                    self.add_component(node.treepaths[i][1],
                                       treepath.get_relative_path(node.treepaths[i][0]),
                                       index_of_type,
                                       self.get_relative_component(sample, node.treepaths[i][0]))
                else:
                    new_node = Node()
                    new_node.treepaths.append((node.treepaths[i][0].get_relative_path(common_path), node.treepaths[i][1]))
                    node.treepaths[i] = (common_path, new_node)
                    self.add_component(new_node,
                                       treepath.get_relative_path(node.treepaths[i][0]),
                                       index_of_type,
                                       self.get_relative_component(sample, node.treepaths[i][0]))
                return
        new_node = Node()
        node.treepaths.append((treepath, new_node))
        self.add_component(new_node,
                           treepath.get_relative_path(treepath),
                           index_of_type,
                           self.get_relative_component(sample, treepath))

    def learn(self, markup_list):
        logging.info("Start learn")
        self.markup_type = type(markup_list[0])
        self.root = Node()
        self.types = list()

        logging.debug("Len of markup list = " + str(len(markup_list)))
        for markup in markup_list:
            logging.debug("Markup for " + markup.file)
            for component in markup.components:
                logging.debug("Component " + component.type)
                f = False
                ind = 0
                for t in self.types:
                    if type(component) == t:
                        f = True
                        break
                    ind += 1

                if not f:
                    self.types.append(type(component))

                component_path = component.title
                for key in component.__dict__.keys():
                    field = component.__dict__[key]
                    if isinstance(field, list):
                        for e in field:
                            component_path = component_path.get_common_prefix(e, True)
                    elif isinstance(component.__dict__[key], TreePath):
                        component_path = component_path.get_common_prefix(field, True)

                self.add_component(self.root, component_path, ind, copy.deepcopy(component))

        self.generate_black_lists(markup_list)
        logging.info("End learn")
        return self

    def parse_component(self, element, sample):
        logging.info("Start")

        component = Component()
        for key in sample.__dict__.keys():
            field = sample.__dict__[key]
            if isinstance(field, str):
                component.__dict__[key] = field
            elif isinstance(field, list):
                inner_treepath = field[0]
                for elem in field:
                    inner_treepath = inner_treepath.get_common_prefix(elem)

                component.__dict__[key] = None
                if len(inner_treepath.get_elements(element)) > 0:
                    component.__dict__[key] = list()
                    for elem in inner_treepath.get_elements(element):
                        component.__dict__[key].append(field[0].get_relative_path(field[0]).get_value(elem))
            else:
                component.__dict__[key] = field.get_value(element)
            if component.__dict__[key] is None:
                logging.info("End None")
                return None
        logging.info("End ok")
        return component

    def is_not_black(self, element, element_type):
        for pair in self.blacks[element_type]:
            if len(element.cssselect(pair[0] + "." + pair[1])) > 0:
                return False
        return True

    def dfs(self, node, tree, parser_result, check=False, current_path=None):
        if node is None:
            return None, None, None
        for i in range(len(node.indexes)):
            if self.is_not_black(tree, node.indexes[i]):
                result = self.parse_component(tree, node.samples[i])
                if result is not None:
                    if check:
                        if parser_result == result:
                            return tree, current_path, node.indexes[i]
                    else:
                        parser_result.add(result)
                        break
        for path, next_node in node.treepaths:
            elements = path.get_elements(tree)
            for elem in elements:
                if current_path is None:
                    new_path = copy.deepcopy(path)
                else:
                    new_path = current_path.concat(path)
                a, b, c = self.dfs(next_node, elem, parser_result, check, new_path)
                if a is not None:
                    return a, b, c
        return None, None, None

    def parse(self, raw_page):
        logging.info("Start parse")
        tree = self.markup_type.get_TreePath_class().get_tree(raw_page)
        parser_result = ParserResult()

        self.dfs(self.root, tree, parser_result)

        logging.debug("End parse")
        return parser_result
