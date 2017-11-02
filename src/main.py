from avg_aggregator import AvgAggregator
from metrics.parser_result_levenstein_metric import ParserResultLevensteinMetric
from primitive_algorithm import PrimitiveAlgorithm
from quality_control import QualityControl

metric = ParserResultLevensteinMetric()
aggregator = AvgAggregator()

algorithm = PrimitiveAlgorithm()
control = QualityControl(metric, aggregator)
print("Quality =", control.get_quality(algorithm))
