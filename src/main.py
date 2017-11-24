from aggregators.avg_aggregator import AvgAggregator
from algorithms.primitive_algorithm import PrimitiveAlgorithm
from algorithms.primitive_algorithm_v2 import PrimitiveAlgorithm_v2
from algorithms.primitive_algorithm_v3 import PrimitiveAlgorithm_v3
from algorithms.algorithm_v1 import Algorithm_v1
from algorithms.algorithm_v2 import Algorithm_v2
from algorithms.selectors.simple_selector import SimpleSelector
from algorithms.selectors.black_list_selector import BlackListSelector
from metrics.parser_result_levenstein_metric import ParserResultLevensteinMetric
from quality_control import QualityControl

metric = ParserResultLevensteinMetric()
aggregator = AvgAggregator()
control = QualityControl(metric, aggregator)

algorithm1 = Algorithm_v1("")
print("Algorithm v1.: quality =", control.get_quality(algorithm1))

simple_selector = SimpleSelector()
algorithm2 = Algorithm_v2("", selector=simple_selector)
print("Algorithm v2. SimpleSelector: quality =", control.get_quality(algorithm2))

blacklist_selector = BlackListSelector()
algorithm3 = Algorithm_v2("", selector=blacklist_selector)
print("Algorithm v2. BlackListSelector: quality =", control.get_quality(algorithm3))
