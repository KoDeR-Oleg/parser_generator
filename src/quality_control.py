import numpy as np

from parsers.ideal_parser import IdealParser


class QualityControl(object):
    def __init__(self, metric, aggregator):
        self.metric = metric
        self.aggregator = aggregator

    def cv(self, algorithm, path, part=0.5):
        N = 50
        ideal_parser = IdealParser()

        learn_nums = range(int(N * part))
        test_nums = range(int(N * part), N)

        markup_list = list()
        for i in learn_nums:
            markup_list.append(ideal_parser.extract_markup(path + str(i) + "_markup.json"))

        algorithm.learn(markup_list)
        dist = list()
        for i in test_nums:
            with open(path + str(i) + ".html", "r") as file:
                string = file.read()
            parser_result = algorithm.parse(string)
            ideal_result = ideal_parser.parse(path + str(i) + ".json")
            dist.append(self.metric.distance(parser_result, ideal_result))

        return self.aggregator.aggregate(dist)

    def get_quality(self, algorithm):
        result = dict()
        result['google'] = self.cv(algorithm, "../golden/google/")
        result['yandex'] = self.cv(algorithm, "../golden/yandex/")
        result['total'] = self.aggregator.aggregate(result.values())
        return result
