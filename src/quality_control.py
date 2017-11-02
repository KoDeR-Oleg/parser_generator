import numpy as np

from parsers.ideal_parser import IdealParser


class QualityControl(object):
    def __init__(self, metric, aggregator):
        self.metric = metric
        self.aggregator = aggregator

    def cv(self, algorithm, path, n_iter=1):
        np.random.seed(42)
        N = 50
        nums = np.arange(0, N, dtype=np.int)
        total = 0
        ideal_parser = IdealParser()
        for iter in range(n_iter):
            np.random.shuffle(nums)
            learn_nums = nums[:N // 2]
            test_nums = nums[N // 2:]

            parser = IdealParser()
            markup_list = list()
            for i in range(learn_nums.shape[0]):
                markup_list.append(parser.extract_markup(path + str(learn_nums[i]) + "_markup.json"))

            algorithm.learn(markup_list)
            dist = list()
            for i in range(test_nums.shape[0]):
                with open(path + str(test_nums[i]) + ".html", "r") as file:
                    string = file.read()
                parser_result = algorithm.parse(string)
                ideal_result = ideal_parser.parse(path + str(test_nums[i]) + ".json")
                dist.append(self.metric.distance(parser_result, ideal_result))
            total += self.aggregator.aggregate(dist)

        return total / n_iter

    def get_quality(self, algorithm):
        result = dict()
        result['google'] = self.cv(algorithm, "../golden/google/")
        result['yandex'] = self.cv(algorithm, "../golden/yandex/")
        result['total'] = self.aggregator.aggregate(result.values())
        return result
