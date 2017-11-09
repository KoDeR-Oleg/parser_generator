from abc import ABCMeta, abstractmethod

from markups.search_markup import SearchMarkup
from parser_result import ParserResult


class Parser:
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract_markup(self, file_name) -> SearchMarkup:
        """Получение разметки файла"""

    @abstractmethod
    def parse(self, string) -> ParserResult:
        """Получение ParserResult из файла"""
