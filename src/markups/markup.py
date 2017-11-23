from abc import ABCMeta, abstractstaticmethod


class Markup:
    __metaclass__ = ABCMeta

    @abstractstaticmethod
    def get_TreePath_class():
        "Получение класса для путей"
