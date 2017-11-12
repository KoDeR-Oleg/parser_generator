from abc import ABCMeta, abstractmethod
from typing import List


class MetricAggregator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def aggregate(self, lst: List[float]) -> float:
        """Агрегация результатов"""
