from abc import ABCMeta, abstractmethod, abstractstaticmethod


class TreePath:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_relative_path(self, tree_path):
        "Получение пути относительно tree_path"

    @abstractmethod
    def get_common_prefix(self, tree_path):
        "Получение наибольшего общего пути"

    @abstractmethod
    def len(self):
        "Получение длины пути"

    @abstractmethod
    def drop_for_len(self, len):
        "Обрезание пути до заданной длины"

    @abstractmethod
    def concat(self, tree_path):
        "Конкатенация путей"
