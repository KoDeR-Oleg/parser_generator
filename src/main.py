from algorithms.primitive_algorithm import PrimitiveAlgorithm
from avg_aggregator import AvgAggregator
from metrics.parser_result_levenstein_metric import ParserResultLevensteinMetric
from quality_control import QualityControl

metric = ParserResultLevensteinMetric()
aggregator = AvgAggregator()

algorithm = PrimitiveAlgorithm()
control = QualityControl(metric, aggregator)
print("Quality =", control.get_quality(algorithm))
