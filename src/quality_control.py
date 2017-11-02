import numpy as np

from parsers.google_parser_v2 import GoogleParser_v2
from parsers.ideal_parser import IdealParser


class QualityControl(object):
    def __init__(self, metric, aggregator):
        self.metric = metric
        self.aggregator = aggregator

    def cv(self, algorithm, n_iter=10):
        N = 50
        nums = np.arange(0, N, dtype=np.int)
        total = 0
        ideal_parser = IdealParser()
        for iter in range(n_iter):
            np.random.shuffle(nums)
            learn_nums = nums[:N // 2]
            test_nums = nums[N // 2:]

            parser = GoogleParser_v2()
            markup_list = list()
            for i in range(learn_nums.shape[0]):
                markup_list.append(parser.extract_markup("../golden/google/" + str(learn_nums[i]) + ".html"))

            algorithm.learn(markup_list)
            dist = list()
            for i in range(test_nums.shape[0]):
                parser_result = algorithm.parse("../golden/google/" + str(test_nums[i]) + ".html")
                ideal_result = ideal_parser.parse("../golden/google/" + str(test_nums[i]) + ".json")
                dist.append(self.metric.distance(parser_result, ideal_result))
            total += self.aggregator.aggregate(dist)

        return total / n_iter

    def get_quality(self, algorithm):
        return self.cv(algorithm)
