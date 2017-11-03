from aggregators.avg_aggregator import AvgAggregator
from algorithms.primitive_algorithm import PrimitiveAlgorithm
from algorithms.primitive_algorithm_v2 import PrimitiveAlgorithm_v2
from metrics.parser_result_levenstein_metric import ParserResultLevensteinMetric
from quality_control import QualityControl

metric = ParserResultLevensteinMetric()
aggregator = AvgAggregator()

algorithm = PrimitiveAlgorithm()
control = QualityControl(metric, aggregator)
print("Quality =", control.get_quality(algorithm))

algorithm2 = PrimitiveAlgorithm_v2()
print("Quality =", control.get_quality(algorithm2))
