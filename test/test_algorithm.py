import unittest

from algorithms.algorithm_v1 import Algorithm_v1
from parsers.ideal_parser import IdealParser


class TestAlgorithm(unittest.TestCase):

    def setUp(self):
        self.algorithm = Algorithm_v1("")

    def get_markup_list(self, path, part=0.5):
        N = 50
        markup_list = list()
        ideal_parser = IdealParser(path)
        for i in range(int(N * part)):
            markup_list.append(ideal_parser.extract_markup(str(i) + "_markup.json"))
        return markup_list

    def parse(self, golden_set, page):
        path = "./golden/" + golden_set + "/"
        markup_list = self.get_markup_list(path)
        self.algorithm.directory = path
        self.algorithm.learn(markup_list)
        with open(path + page, "r") as file:
            parser_result = self.algorithm.parse(file.read())
        return parser_result

    def get_expected(self, golden_set, page):
        ideal_parser = IdealParser("./golden/" + golden_set)
        with open("./golden/" + golden_set + "/" + page, "r") as file:
            parser_result = ideal_parser.parse(file.read())
        return parser_result

    def test_equal_count_of_blocks_on_google_page(self):
        actual = self.parse("google", "25.html")
        expected = self.get_expected("google", "25.html")
        self.assertEqual(actual.count(), expected.count())

    def test_equal_count_of_blocks_on_google_page1(self):
        actual = self.parse("google", "1.html")
        expected = self.get_expected("google", "1.html")
        print(actual)
        self.assertEqual(actual.count(), expected.count())

    def test_equal_count_of_blocks_with_type_on_google_page(self):
        actual = self.parse("google", "34.html")
        expected = self.get_expected("google", "34.html")
        self.assertEqual(actual.count(), expected.count())
        self.assertEqual(actual.count("SEARCH_RESULT"), expected.count("SEARCH_RESULT"))
        self.assertEqual(actual.count("WIZARD"), expected.count("WIZARD"))

    def test_type_of_blocks_is_not_none_on_google_image_page(self):
        actual = self.parse("google_image", "25.html")
        expected = self.get_expected("google_image", "25.html")
        self.assertEqual(actual.count(), expected.count())
        for i in range(actual.count()):
            with self.subTest(msg="Component "+str(i)):
                self.assertIsNotNone(actual.components[i].type)

    def test_title_of_blocks_is_not_none_on_google_image_page(self):
        actual = self.parse("google_image", "25.html")
        expected = self.get_expected("google_image", "25.html")
        self.assertEqual(actual.count(), expected.count())
        for i in range(actual.count()):
            with self.subTest(msg="Component "+str(i)):
                self.assertIsNotNone(actual.components[i].title)

    def test_view_url_of_blocks_is_not_empty_on_yandex_page(self):
        actual = self.parse("yandex", "44.html")
        expected = self.get_expected("yandex", "44.html")
        self.assertEqual(actual.count(), expected.count())
        for i in range(actual.count()):
            with self.subTest(msg="Component "+str(i)):
                self.assertIsNotNone(actual.components[i].view_url)
                self.assertNotEqual(actual.components[i].view_url, "")

    def test_equal_count_of_blocks_on_yandex_page(self):
        actual = self.parse("yandex", "47.html")
        expected = self.get_expected("yandex", "47.html")
        self.assertEqual(actual.count(), expected.count())

    def test_equal_count_of_wizard_on_yandex_page(self):
        actual = self.parse("yandex", "47.html")
        expected = self.get_expected("yandex", "47.html")
        self.assertEqual(actual.count("WIZARD"), expected.count("WIZARD"))

    def test_equal_count_of_block_on_yandex_page_with_adv(self):
        actual = self.parse("yandex", "30.html")
        expected = self.get_expected("yandex", "30.html")
        self.assertEqual(actual.count(), expected.count())
