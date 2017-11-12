from abc import ABCMeta, abstractstaticmethod


class Markup:
    __metaclass__ = ABCMeta

    @abstractstaticmethod
    def get_attr(tags, attr: str) -> str:
        """Получение значения атрибута"""
