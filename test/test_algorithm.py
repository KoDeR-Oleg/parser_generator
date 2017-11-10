import unittest

from algorithms.algorithm_v1 import Algorithm_v1
from parsers.ideal_parser import IdealParser


class TestAlgorithm(unittest.TestCase):

    def setUp(self):
        self.algorithm = Algorithm_v1()

    def get_markup_list(self, path, part=0.5):
        N = 50
        markup_list = list()
        ideal_parser = IdealParser()
        for i in range(int(N * part)):
            markup_list.append(ideal_parser.extract_markup(path + str(i) + "_markup.json"))
        return markup_list

    def parse(self, golden_set, page):
        path = "./golden/" + golden_set + "/"
        markup_list = self.get_markup_list(path)
        self.algorithm.learn(markup_list, directory=path)
        with open(path + str(page) + ".html", "r") as file:
            parser_result = self.algorithm.parse(file.read())
        return parser_result

    def get_expected(self, golden_set, page):
        ideal_parser = IdealParser()
        with open("./golden/" + golden_set + "/" + str(page) + ".html", "r") as file:
            parser_result = ideal_parser.parse(file.read(), "./golden")
        return parser_result

    def test_count_of_blocks_on_google_page25(self):
        actual = self.parse("google", 25)
        expected = self.get_expected("google", 25)
        self.assertEqual(actual.count(), expected.count())

    def test_count_of_blocks_with_type_on_google_page34(self):
        actual = self.parse("google", 34)
        expected = self.get_expected("google", 34)
        self.assertEqual(actual.count(), expected.count())
        self.assertEqual(actual.count("SEARCH_RESULT"), expected.count("SEARCH_RESULT"))
        self.assertEqual(actual.count("WIZARD"), expected.count("WIZARD"))

    def test_type_of_blocks_on_google_image_page25(self):
        actual = self.parse("google_image", 25)
        expected = self.get_expected("google_image", 25)
        self.assertEqual(actual.count(), expected.count())
        for i in range(actual.count()):
            with self.subTest(msg="Component "+str(i)):
                self.assertIsNotNone(actual.components[i].type)

    def test_title_of_blocks_on_google_image_page25(self):
        actual = self.parse("google_image", 25)
        expected = self.get_expected("google_image", 25)
        self.assertEqual(actual.count(), expected.count())
        for i in range(actual.count()):
            with self.subTest(msg="Component "+str(i)):
                self.assertIsNotNone(actual.components[i].title)

    def test_view_url_of_blocks_on_yandex_page44(self):
        actual = self.parse("yandex", 44)
        expected = self.get_expected("yandex", 44)
        self.assertEqual(actual.count(), expected.count())
        for i in range(actual.count()):
            with self.subTest(msg="Component "+str(i)):
                self.assertIsNotNone(actual.components[i].view_url)
                self.assertNotEqual(actual.components[i].view_url, "")

    def test_count_of_blocks_on_yandex_page47(self):
        actual = self.parse("yandex", 47)
        expected = self.get_expected("yandex", 47)
        self.assertEqual(actual.count(), expected.count())

    def test_count_of_wizard_on_yandex_page47(self):
        actual = self.parse("yandex", 47)
        expected = self.get_expected("yandex", 47)
        self.assertEqual(actual.count("WIZARD"), expected.count("WIZARD"))

    def test_count_of_block_on_yandex_page30(self):
        actual = self.parse("yandex", 30)
        print(actual)
        expected = self.get_expected("yandex", 30)
        self.assertEqual(actual.count(), expected.count())
