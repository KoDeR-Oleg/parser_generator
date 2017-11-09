from algorithms.primitive_algorithm_v3 import PrimitiveAlgorithm_v3
from metrics.parser_result_levenstein_metric import ParserResultLevensteinMetric
from parsers.ideal_parser import IdealParser


def get_max_distance(algorithm, golden_set):
    path = "../golden/" + golden_set + "/"
    N = 50
    part = 0.5
    ideal_parser = IdealParser()

    learn_nums = range(int(N * part))
    test_nums = range(int(N * part), N)

    markup_list = list()
    for i in learn_nums:
        markup_list.append(ideal_parser.extract_markup(path + str(i) + "_markup.json"))

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

algorithm3 = PrimitiveAlgorithm_v3()
dist, page = get_max_distance(algorithm3, "google_image")
print("Max dist = ", dist, ", page = ", page, sep="")