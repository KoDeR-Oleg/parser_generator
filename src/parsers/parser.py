from abc import ABCMeta, abstractmethod
from markup import Markup
from parser_result import ParserResult


class Parser:
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract_markup(self, file_name) -> Markup:
        """Получение разметки файла"""

    @abstractmethod
    def parse(self, file_name) -> ParserResult:
        """Получение ParserResult из файла"""
