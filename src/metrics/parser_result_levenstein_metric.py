from metrics.metric import Metric
from metrics.levenstein_metric import LevensteinMetric


class ParserResultLevensteinMetric(Metric):
    def __init__(self, add=1, delete=1, change=1):
        self.add_cost = add
        self.del_cost = delete
        self.change_cost = change

    def distance(self, pr1, pr2):
        return LevensteinMetric(self.add_cost, self.del_cost, self.change_cost).distance(pr1.components, pr2.components)
