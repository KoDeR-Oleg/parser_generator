import unittest

from algorithms.primitive_algorithm import PrimitiveAlgorithm
from parser_result import Component
from parsers.google_parser import GoogleParser


class TestAlgorithm(unittest.TestCase):

    def test_count_of_blocks_on_page3(self):
        parser = GoogleParser()
        markup_list = []
        markup_list.append(parser.extract_markup("test/google/2/1.html"))
        markup_list.append(parser.extract_markup("test/google/2/2.html"))
        primitive_algorithm = PrimitiveAlgorithm().learn(markup_list)
        with open("test/google/2/3.html", "r") as file:
            string = file.read()
        parser_result = primitive_algorithm.parse(string)

        self.assertEqual(len(parser_result.components), 9)

    def test_fields_of_first_result_search_on_page3(self):
        parser = GoogleParser()
        markup_list = []
        markup_list.append(parser.extract_markup("test/google/2/1.html"))
        markup_list.append(parser.extract_markup("test/google/2/2.html"))
        primitive_algorithm = PrimitiveAlgorithm().learn(markup_list)
        with open("test/google/2/3.html", "r") as file:
            string = file.read()
        parser_result = primitive_algorithm.parse(string)

        search_result = parser_result.components[0]
        self.assertEqual(search_result.type, "SEARCH_RESULT")
        self.assertEqual(search_result.alignment, "LEFT")
        self.assertEqual(search_result.page_url, "https://ru.wikipedia.org/wiki/%D0%9F%D0%B0%D1%80%D0%B0%D1%88%D1%8E%D1%82")
        self.assertEqual(search_result.title, "Парашют — Википедия")
        self.assertEqual(search_result.snippet, "Парашю́т (фр. parachute) — устройство в форме зонта из ткани или другого мягкого материала, к которому стропами прикреплена подвесная система\xa0...")
        self.assertEqual(search_result.view_url, "https://ru.wikipedia.org/wiki/Парашют")

    def test_count_of_media_links_on_page3(self):
        parser = GoogleParser()
        markup_list = []
        markup_list.append(parser.extract_markup("test/google/2/1.html"))
        markup_list.append(parser.extract_markup("test/google/2/2.html"))
        primitive_algorithm = PrimitiveAlgorithm().learn(markup_list)
        with open("test/google/2/3.html", "r") as file:
            string = file.read()
        parser_result = primitive_algorithm.parse(string)

        self.assertEqual(len(parser_result.components[0].media_links), 6)

    def test_title_of_wizard_image_on_page3(self):
        parser = GoogleParser()
        markup_list = []
        markup_list.append(parser.extract_markup("test/google/2/1.html"))
        markup_list.append(parser.extract_markup("test/google/2/2.html"))
        primitive_algorithm = PrimitiveAlgorithm().learn(markup_list)
        with open("test/google/2/3.html", "r") as file:
            string = file.read()
        parser_result = primitive_algorithm.parse(string)

        self.assertEqual(parser_result.components[0].title, "Картинки по запросу парашют")

    def test_page_url_of_wizard_image_on_page3(self):
        parser = GoogleParser()
        markup_list = []
        markup_list.append(parser.extract_markup("test/google/2/1.html"))
        markup_list.append(parser.extract_markup("test/google/2/2.html"))
        primitive_algorithm = PrimitiveAlgorithm().learn(markup_list)
        with open("test/google/2/3.html", "r") as file:
            string = file.read()
        parser_result = primitive_algorithm.parse(string)

        self.assertEqual(parser_result.components[0].page_url, "https://www.google.ru/search?q=%D0%BF%D0%B0%D1%80%D0%B0%D1%88%D1%8E%D1%82&newwindow=1&dcr=0&tbm=isch&tbo=u&source=univ&sa=X&ved=0ahUKEwi5_bz9tu3WAhWJApoKHVbrCgwQsAQIfA")

    def test_media_links_on_page3(self):
        parser = GoogleParser()
        markup_list = []
        markup_list.append(parser.extract_markup("test/google/2/1.html"))
        markup_list.append(parser.extract_markup("test/google/2/2.html"))
        primitive_algorithm = PrimitiveAlgorithm().learn(markup_list)
        with open("test/google/2/3.html", "r") as file:
            string = file.read()
        parser_result = primitive_algorithm.parse(string)

        media_links = parser_result.components[0].media_links
        expected_list = ["http://www.happiness-shop.ru/parachute/construction-parachute.html",
                         "http://waterfuns.ru/shop/parashuty/",
                         "http://dic.academic.ru/dic.nsf/enc_tech/828/%D0%BF%D0%B0%D1%80%D0%B0%D1%88%D1%8E%D1%82",
                         "http://old.mirf.ru/Articles/art4933.htm",
                         "http://aviaclub.ru/skydiving/pryzhki/",
                         "http://www.mk.ru/social/2016/08/01/parashyut-kak-vyzov-zachem-lyudyam-zatyazhnye-pryzhki.html"]
        self.assertEqual(media_links, expected_list)
