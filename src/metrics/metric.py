from abc import ABCMeta, abstractmethod
from typing import List, Any


class Metric:
    __metaclass__ = ABCMeta

    @abstractmethod
    def distance(self, pr1: List[Any], pr2: List[Any]) -> float:
        """Расстояние между векторами"""
