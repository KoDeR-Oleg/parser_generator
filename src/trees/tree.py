from abc import ABCMeta, abstractmethod, abstractstaticmethod
from trees.tree_path import TreePath


class Tree:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_value(self, tree_path: TreePath):
        "Получение значения из дерева"

    @abstractmethod
    def get_elements(self, tree_path: TreePath):
        "Получение поддеревьев заданого пути"

    @abstractmethod
    def get_iter(self):
        "Получение итератора по потомкам"
