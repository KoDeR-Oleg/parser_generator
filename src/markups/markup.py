from abc import ABCMeta, abstractmethod


class Markup:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, component):
        """Добавление элемента в components"""
