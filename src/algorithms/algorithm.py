from abc import ABCMeta, abstractmethod
from parser_result import ParserResult


class Algorithm:
    __metaclass__ = ABCMeta

    @abstractmethod
    def learn(self, markup_list):
        """Обучение на списке разметок"""

    @abstractmethod
    def parse(self, string) -> ParserResult:
        """Парсинг строки"""
