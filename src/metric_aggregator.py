from abc import ABCMeta, abstractmethod


class MetricAggregator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def aggregate(self, lst):
        """Агрегация результатов"""
