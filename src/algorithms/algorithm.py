from abc import ABCMeta, abstractmethod
from parser_result import ParserResult
from typing import List
from markups.markup import Markup


class Algorithm:
    __metaclass__ = ABCMeta

    @abstractmethod
    def learn(self, markup_list: List[Markup]):
        """Обучение на списке разметок"""

    @abstractmethod
    def parse(self, raw_page: str) -> ParserResult:
        """Парсинг строки"""
