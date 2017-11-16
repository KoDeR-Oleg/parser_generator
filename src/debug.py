from algorithms.primitive_algorithm_v3 import PrimitiveAlgorithm_v3
from algorithms.algorithm_v1 import Algorithm_v1
from metrics.parser_result_levenstein_metric import ParserResultLevensteinMetric
from parsers.ideal_parser import IdealParser


def get_max_distance(algorithm, golden_set):
    path = "../golden/" + golden_set + "/"
    N = 50
    part = 0.5
    ideal_parser = IdealParser(path)

    learn_nums = range(int(N * part))
    test_nums = range(int(N * part), N)

    markup_list = list()
    for i in learn_nums:
        markup_list.append(ideal_parser.extract_markup(str(i) + "_markup.json"))

    algorithm.directory = path
    algorithm.learn(markup_list)
    mx_dist = 0
    mx_ind = 0
    for i in test_nums:
        with open(path + str(i) + ".html", "r") as file:
            string = file.read()
        parser_result = algorithm.parse(string)
        ideal_result = ideal_parser.parse(string)
        dist = metric.distance(parser_result, ideal_result)
        if dist > mx_dist:
            mx_dist, mx_ind = dist, i

    return mx_dist, mx_ind


metric = ParserResultLevensteinMetric()

algorithm = Algorithm_v1("")
dist, page = get_max_distance(algorithm, "yandex")
print("Max dist = ", dist, ", page = ", page, sep="")