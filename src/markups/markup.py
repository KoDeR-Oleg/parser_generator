from abc import ABCMeta, abstractmethod, abstractstaticmethod, abstractproperty


class TreePath:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_value(self, root):
        "Получение значения из дерева"

    @abstractmethod
    def get_relative_path(self, tree_path):
        "Получение пути относительно tree_path"

    @abstractmethod
    def get_common_prefix(self, tree_path):
        "Получение наибольшего общего пути"

    @abstractmethod
    def get_elements(self, tree):
        "Получение всех элементов для заданного пути"

    @abstractmethod
    def len(self):
        "Получение длины пути"

    @abstractmethod
    def drop_for_len(self, len):
        "Обрезание пути до заданной длины"

    @abstractmethod
    def concat(self, tree_path):
        "Конкатенация путей"

    @abstractstaticmethod
    def get_tree(raw_page):
        "Получение дерева путей"


class Markup:
    __metaclass__ = ABCMeta

    @abstractstaticmethod
    def get_TreePath_class():
        "Получение класса для путей"
