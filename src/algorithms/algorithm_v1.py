from algorithms.algorithm import Algorithm
from parser_result import ParserResult, Component
from trees.tree_path import TreePath
import logging


class Algorithm_v1(Algorithm):
    def __init__(self, directory):
        self.samples = list()
        self.treepaths = list()
        self.types = list()
        self.blacks = list()
        self.block_treepath = None
        self.directory = directory
        self.markup_type = None
        logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(funcName)s]  %(message)s',
                            level=logging.DEBUG, filename='algorithm_v1.log')

    def parse_component(self, element, index_of_type):
        logging.info("Start")
        sample = self.samples[index_of_type]

        component = Component()
        for key in sample.__dict__.keys():
            field = sample.__dict__[key]
            if isinstance(field, str):
                component.__dict__[key] = field
            elif isinstance(field, list):
                inner_treepath = field[0]
                for elem in field:
                    inner_treepath = inner_treepath.get_common_prefix(elem)
                inner_treepath = inner_treepath.get_relative_path(self.block_treepath)

                component.__dict__[key] = None
                if len(element.get_elements(inner_treepath)) > 0:
                    component.__dict__[key] = list()
                    for elem in element.get_elements(inner_treepath):
                        component.__dict__[key].append(elem.get_value(field[0].get_relative_path(field[0])))
            else:
                component.__dict__[key] = element.get_value(field.get_relative_path(self.block_treepath))
            if component.__dict__[key] is None:
                logging.info("End None")
                return None
        logging.info("End ok")
        return component

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
                        parser_component.__dict__[key].append(tree.get_value(elem))
                else:
                    parser_component.__dict__[key] = tree.get_value(field)
            parser_result.add(parser_component)
        logging.info("End")
        return parser_result

    def get_element_for_parser_component(self, parser_component, tree):
        logging.info("Start")
        block_list = tree.get_elements(self.block_treepath)
        for block in block_list:
            for i in range(len(self.types)):
                if len(block.get_elements(self.treepaths[i])) > 0:
                    result = self.parse_component(block, i)
                    if result is not None and result == parser_component:
                        logging.info("End ok")
                        return block, i
        logging.info("End None")
        return None, None

    def add_black_for_element(self, element, index_of_element_type, markup_list):
        logging.info("Start")
        list_pair = list()
        for tag in element.get_iter():
            for cl in tag.classes:
                list_pair.append((tag.tag, cl))
        list_flag = [True] * len(list_pair)

        for markup in markup_list:
            with open(self.directory + markup.file, "r") as file:
                string = file.read()
            tree = markup.get_TreePath_class().get_Tree_class().get_tree(string)

            for component in markup.components:
                if isinstance(component, self.types[index_of_element_type]):
                    block = tree.get_elements(component.title.drop_for_len(self.block_treepath.len()))[0]
                    for i in range(len(list_pair)):
                        if list_flag[i] and len(block.cssselect(list_pair[i][0] + "." + list_pair[i][1])) > 0:
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

        for markup in markup_list:
            logging.debug("Markup for " + markup.file)
            with open(self.directory + markup.file, "r") as file:
                string = file.read()
            actual = self.parse(string)
            tree = markup.get_TreePath_class().get_Tree_class().get_tree(string)
            expected = self.get_substitution(tree, markup)
            logging.debug("Actual count = " + str(actual.count()) + ", Expected count = " + str(expected.count()))
            if actual.count() == expected.count():
                if actual == expected:
                    continue
            for component in actual.components:
                if component not in expected.components:
                    logging.debug(component == expected.components[0])
                    element, element_type = self.get_element_for_parser_component(component, tree)
                    self.add_black_for_element(element, element_type, markup_list)
                else:
                    logging.debug(str(component))

        logging.info("End")

    def learn(self, markup_list):
        logging.info("Start learn")
        self.markup_type = type(markup_list[0])
        self.samples = list()
        self.treepaths = list()
        self.types = list()
        self.block_treepath = markup_list[0].components[0].title
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
                        self.treepaths[ind] = self.treepaths[ind].get_common_prefix(component.title)
                        break
                    ind += 1

                if not f:
                    self.treepaths.append(component.title)
                    self.samples.append(component)
                    self.types.append(type(component))

                for key in component.__dict__.keys():
                    field = component.__dict__[key]
                    if isinstance(field, list):
                        for e in field:
                            self.block_treepath = self.block_treepath.get_common_prefix(e)
                            self.treepaths[ind] = self.treepaths[ind].get_common_prefix(e)
                    elif isinstance(component.__dict__[key], TreePath):
                        self.block_treepath = self.block_treepath.get_common_prefix(field)
                        self.treepaths[ind] = self.treepaths[ind].get_common_prefix(field)

        for i in range(len(self.treepaths)):
            self.treepaths[i] = self.treepaths[i].get_relative_path(self.block_treepath)

        self.generate_black_lists(markup_list)
        logging.info("End learn")
        return self

    def is_not_black(self, element, element_type):
        for pair in self.blacks[element_type]:
            if len(element.cssselect(pair[0] + "." + pair[1])) > 0:
                return False
        return True

    def parse(self, raw_page):
        logging.info("Start parse")
        tree = self.markup_type.get_TreePath_class().get_Tree_class().get_tree(raw_page)
        parser_result = ParserResult()

        block_list = tree.get_elements(self.block_treepath)
        for block in block_list:
            for i in range(len(self.types)):
                if len(block.get_elements(self.treepaths[i])) > 0 and self.is_not_black(block, i):
                    result = self.parse_component(block, i)
                    if result is not None:
                        parser_result.add(result)
                        break

        logging.debug("End parse")
        return parser_result
