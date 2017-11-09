from abc import ABCMeta, abstractmethod


class Markup:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_attr(self, tags, attr) -> str:
        """Получение значения атрибута"""
