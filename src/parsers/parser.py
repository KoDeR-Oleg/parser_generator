from abc import ABCMeta, abstractmethod


class Parser:
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract_markup(self, file_name):
        """Получение разметки файла"""

    @abstractmethod
    def parse(self, file_name):
        """Получение ParserResult из строки"""
