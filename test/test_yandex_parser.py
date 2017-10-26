import unittest
from yandex_parser import YandexParser
from parser_result import Component
from markup import MarkupSearchResult, FullPath


class TestYandexParser(unittest.TestCase):

    def test_filename_in_markup_page1(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/1.html")
        self.assertEqual(markup.file, "../yandex/1.html")

    def test_filename_in_markup_page2(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/2.html")
        self.assertEqual(markup.file, "../yandex/2.html")

    def test_count_of_blocks_on_page1(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/1.html")
        self.assertEqual(len(markup.components), 11)

    def test_count_of_blocks_on_page2(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/2.html")
        self.assertEqual(len(markup.components), 10)

    def test_markups_of_first_result_search_on_page1(self):
        parser = YandexParser()
        markup_component = parser.extract_markup("../yandex/1.html").components[0]
        self.assertEqual(markup_component.type, "SEARCH_RESULT")
        self.assertEqual(markup_component.alignment, "LEFT")
        self.assertEqual(markup_component.page_url.xpath, "//html/body[1]/div[3]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[1]/div[1]/h2/a")
        self.assertEqual(markup_component.page_url.attr, "href")
        self.assertEqual(markup_component.title.xpath, "//html/body[1]/div[3]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[1]/div[1]/h2/a")
        self.assertEqual(markup_component.title.attr, "string")
        self.assertEqual(markup_component.snippet.xpath, "//html/body[1]/div[3]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[1]/div[1]/div[2]/div[1]")
        self.assertEqual(markup_component.snippet.attr, "string")
        self.assertEqual(markup_component.view_url.xpath, "//html/body[1]/div[3]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[1]/div[1]/div[1]/div[1]/a[last()]")
        self.assertEqual(markup_component.view_url.attr, "href")

    def test_fields_of_first_result_search_on_page1(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/1.html")
        search_result = markup.get_substitution(0)
        self.assertEqual(search_result.type, "SEARCH_RESULT")
        self.assertEqual(search_result.alignment, "LEFT")
        self.assertEqual(search_result.page_url, "https://money.yandex.ru/")
        self.assertEqual(search_result.title, "Яндекс.Деньги — сервис онлайн-платежей")
        self.assertEqual(search_result.snippet, "Оплата товаров и услуг через интернет, перевод денег на счета или банковские карты. Возможность оформить виртуальную или пластиковую банковскую карту.")
        self.assertEqual(search_result.view_url, "https://money.yandex.ru/")

    def test_fields_of_last_result_search_on_page1(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/1.html")
        search_result = markup.get_substitution(10)
        self.assertEqual(search_result.type, "SEARCH_RESULT")
        self.assertEqual(search_result.alignment, "LEFT")
        self.assertEqual(search_result.page_url, "http://www.habit.ru/18/252.html")
        self.assertEqual(search_result.title, "Таблица ядов · Химия")
        self.assertEqual(search_result.snippet, "Таблица ядов. Какие мысли возникают у Вас при слове «яд»?\xa0... Итак, давайте познакомимся с ядами поближе.")
        self.assertEqual(search_result.view_url, "http://www.habit.ru/18/252.html")

    def test_fields_of_first_result_search_on_page2(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/2.html")
        search_result = markup.get_substitution(0)
        self.assertEqual(search_result.type, "SEARCH_RESULT")
        self.assertEqual(search_result.alignment, "LEFT")
        self.assertEqual(search_result.page_url, "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%80%D0%B0%D0%BD%D0%B4%D0%B0%D1%88")
        self.assertEqual(search_result.title, "Карандаш — Википедия")
        self.assertEqual(search_result.snippet, "Каранда́ш — инструмент в виде стержня, изготавливаемого из пишущего материала (угля, графита, сухих красок и тому подобного), применяемый для письма...")
        self.assertEqual(search_result.view_url, "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%80%D0%B0%D0%BD%D0%B4%D0%B0%D1%88")

    def test_fields_of_last_result_search_on_page2(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/2.html")
        search_result = markup.get_substitution(9)
        self.assertEqual(search_result.type, "SEARCH_RESULT")
        self.assertEqual(search_result.alignment, "LEFT")
        self.assertEqual(search_result.page_url, "https://www.mekka-spb.ru/catalog/karandashi-chernografitnyje/")
        self.assertEqual(search_result.title, "Карандаши чернографитные - купить в интернет-магазине...")
        self.assertEqual(search_result.snippet, "Купить карандаши чернографитные предлагаем на сайте Канцелярская мекка.\xa0... 7Карандаши чернографитные в наборах.")
        self.assertEqual(search_result.view_url, "https://www.mekka-spb.ru/catalog/karandashi-chernografitnyje/")

    def test_count_of_media_links_on_page1(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/1.html")
        self.assertEqual(len(markup.components[7].media_links), 3)

    def test_title_of_wizard_image_on_page1(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/1.html")
        self.assertEqual(markup.get_substitution(7).title, "яд — смотрите картинки")

    def test_page_url_of_wizard_image_on_page1(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/1.html")
        self.assertEqual(markup.get_substitution(7).page_url, "https://yandex.ru/images/search?text=%D1%8F%D0%B4&stype=image&lr=2&noreask=1&parent-reqid=1507840705773924-1204282718026678870245913-vla1-2156&source=wiz")

    def test_media_links_on_page1(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/1.html")
        media_links = markup.get_substitution(7).media_links
        self.assertEqual(media_links[0], "im0-tub-ru.yandex.net/i?id=353e0e40d1d5ddf2f7a6be4fc3834d53&n=22")
        self.assertEqual(media_links[1], "im0-tub-ru.yandex.net/i?id=a64b49cb5028dde1632048248050d956&n=22")
        self.assertEqual(media_links[2], "im0-tub-ru.yandex.net/i?id=52a9ed57daafb3f8bcf99d2784695e78&n=22")

    def test_regress_on_page1(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/1.html")
        search_result = markup.get_substitution()
        with open("../yandex/1.json", "r") as file:
            expected_string = file.read()
        self.assertEqual(str(search_result), expected_string)

    def test_regress_on_page2(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/2.html")
        search_result = markup.get_substitution()
        with open("../yandex/2.json", "r") as file:
            expected_string = file.read()
        self.assertEqual(str(search_result), expected_string)

    def test_markup_regress_on_page1(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/1.html")
        with open("../yandex/1_markup.json", "r") as file:
            expected_markup = file.read()
        self.assertEqual(str(markup), expected_markup)

    def test_markup_regress_on_page2(self):
        parser = YandexParser()
        markup = parser.extract_markup("../yandex/2.html")
        with open("../yandex/2_markup.json", "r") as file:
            expected_markup = file.read()
        self.assertEqual(str(markup), expected_markup)
