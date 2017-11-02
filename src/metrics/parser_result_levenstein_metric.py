from metrics.metric import Metric
from metrics.levenstein_metric import LevensteinMetric


class ParserResultLevensteinMetric(Metric):
    def distance(self, pr1, pr2):
        return LevensteinMetric().distance(pr1.components, pr2.components)
