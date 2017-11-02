from aggregators.metric_aggregator import MetricAggregator


class AvgAggregator(MetricAggregator):
    def aggregate(self, lst):
        return sum(lst) / len(lst)
