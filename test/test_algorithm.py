import unittest
import google_parser
import algorithm
from markup import Component


class TestAlgorithm(unittest.TestCase):

    def test_filename_in_markup_page3(self):
        markup_list = []
        markup_list.append(google_parser.parse_page("../google/2/1.html"))
        markup_list.append(google_parser.parse_page("../google/2/2.html"))
        result_markup = algorithm.parse_page("../google/2/3.html", markup_list)

        self.assertEqual(result_markup.file, "../google/2/3.html")

    def test_count_of_blocks_on_page3(self):
        markup_list = []
        markup_list.append(google_parser.parse_page("../google/2/1.html"))
        markup_list.append(google_parser.parse_page("../google/2/2.html"))
        result_markup = algorithm.parse_page("../google/2/3.html", markup_list)

        self.assertEqual(len(result_markup.components), 9)

    def test_fields_of_first_result_search_on_page3(self):
        markup_list = []
        markup_list.append(google_parser.parse_page("../google/2/1.html"))
        markup_list.append(google_parser.parse_page("../google/2/2.html"))
        result_markup = algorithm.parse_page("../google/2/3.html", markup_list)

        search_result = result_markup.get_substitution(0)
        expected_component = Component()
        expected_component.type = "SEARCH_RESULT"
        expected_component.alignment = "LEFT"
        expected_component.page_url = "https://ru.wikipedia.org/wiki/%D0%9F%D0%B0%D1%80%D0%B0%D1%88%D1%8E%D1%82"
        expected_component.title = "Парашют — Википедия"
        expected_component.snippet = "Парашю́т (фр. parachute) — устройство в форме зонта из ткани или другого мягкого материала, к которому стропами прикреплена подвесная система\xa0..."
        expected_component.view_url = "https://ru.wikipedia.org/wiki/Парашют"
        self.assertEqual(search_result, expected_component)

    def test_count_of_media_links_on_page3(self):
        markup_list = []
        markup_list.append(google_parser.parse_page("../google/2/1.html"))
        markup_list.append(google_parser.parse_page("../google/2/2.html"))
        result_markup = algorithm.parse_page("../google/2/3.html", markup_list)

        self.assertEqual(len(result_markup.components[0].media_links), 6)

    def test_title_of_wizard_image_on_page3(self):
        markup_list = []
        markup_list.append(google_parser.parse_page("../google/2/1.html"))
        markup_list.append(google_parser.parse_page("../google/2/2.html"))
        result_markup = algorithm.parse_page("../google/2/3.html", markup_list)

        self.assertEqual(result_markup.get_substitution(0).title, "Картинки по запросу парашют")

    def test_page_url_of_wizard_image_on_page3(self):
        markup_list = []
        markup_list.append(google_parser.parse_page("../google/2/1.html"))
        markup_list.append(google_parser.parse_page("../google/2/2.html"))
        result_markup = algorithm.parse_page("../google/2/3.html", markup_list)

        self.assertEqual(result_markup.get_substitution(0).page_url, "https://www.google.ru/search?q=%D0%BF%D0%B0%D1%80%D0%B0%D1%88%D1%8E%D1%82&newwindow=1&dcr=0&tbm=isch&tbo=u&source=univ&sa=X&ved=0ahUKEwi5_bz9tu3WAhWJApoKHVbrCgwQsAQIfA")

    def test_media_links_on_page3(self):
        markup_list = []
        markup_list.append(google_parser.parse_page("../google/2/1.html"))
        markup_list.append(google_parser.parse_page("../google/2/2.html"))
        result_markup = algorithm.parse_page("../google/2/3.html", markup_list)

        media_links = result_markup.get_substitution(0).media_links
        expected_list = ["http://www.happiness-shop.ru/parachute/construction-parachute.html",
                         "http://waterfuns.ru/shop/parashuty/",
                         "http://dic.academic.ru/dic.nsf/enc_tech/828/%D0%BF%D0%B0%D1%80%D0%B0%D1%88%D1%8E%D1%82",
                         "http://old.mirf.ru/Articles/art4933.htm",
                         "http://aviaclub.ru/skydiving/pryzhki/",
                         "http://www.mk.ru/social/2016/08/01/parashyut-kak-vyzov-zachem-lyudyam-zatyazhnye-pryzhki.html"]
        self.assertEqual(media_links, expected_list)
