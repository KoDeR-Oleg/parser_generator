from abc import ABCMeta, abstractmethod


class Algorithm:
    __metaclass__ = ABCMeta

    @abstractmethod
    def learn(self, markup_list):
        """Обучение на списке разметок"""

    @abstractmethod
    def parse(self, file_name):
        """Парсинг строки"""
