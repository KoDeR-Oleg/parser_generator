from abc import ABCMeta, abstractmethod
from algorithms.algorithm import Algorithm
from markups.markup import Markup
from typing import List


class Selector:
    __metaclass__ = ABCMeta

    @abstractmethod
    def learn(self, algorithm: Algorithm, markup_list: List[Markup]):
        "Инициализация фильтра коллизий"

    @abstractmethod
    def get_iter(self, **kwargs):
        "Получение итератора по компонентам дерева с учётом фильтра"
