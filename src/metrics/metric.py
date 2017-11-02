from abc import ABCMeta, abstractmethod


class Metric:
    __metaclass__ = ABCMeta

    @abstractmethod
    def distance(self, pr1, pr2):
        """Расстояние между векторами"""
