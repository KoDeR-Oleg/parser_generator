from abc import ABCMeta, abstractstaticmethod


class Markup:
    __metaclass__ = ABCMeta

    @abstractstaticmethod
    def get_attr(tags, attr) -> str:
        """Получение значения атрибута"""
