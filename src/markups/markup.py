from abc import ABCMeta, abstractmethod

from markups.search_markup import SearchMarkup
from parser_result import ParserResult


class Markup:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_attr(self, tags, attr) -> str:
        """Получение значения атрибута"""
