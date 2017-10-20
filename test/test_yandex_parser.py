import unittest
from yandex_parser import parse_page
from analysis import Component
from markup import MarkupSearchResult, FullPath


class TestYandexParser(unittest.TestCase):

    def test_filename_in_markup_page1(self):
        markup = parse_page("../yandex/1.html")
        self.assertEqual(markup.file, "../yandex/1.html")

    def test_filename_in_markup_page2(self):
        markup = parse_page("../yandex/2.html")
        self.assertEqual(markup.file, "../yandex/2.html")

    def test_count_of_blocks_on_page1(self):
        markup = parse_page("../yandex/1.html")
        self.assertEqual(len(markup.components), 11)

    def test_count_of_blocks_on_page2(self):
        markup = parse_page("../yandex/2.html")
        self.assertEqual(len(markup.components), 10)

    def test_markups_of_first_result_search_on_page1(self):
        markup_component = parse_page("../yandex/1.html").components[0]
        expected_component = MarkupSearchResult()
        expected_component.type = "SEARCH_RESULT"
        expected_component.alignment = "LEFT"
        expected_component.page_url = FullPath("//html/body[1]/div[3]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[1]/div[1]/h2/a", "href")
        expected_component.title = FullPath("//html/body[1]/div[3]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[1]/div[1]/h2/a", "string")
        expected_component.snippet = FullPath("//html/body[1]/div[3]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[1]/div[1]/div[2]/div[1]", "string")
        expected_component.view_url = FullPath("//html/body[1]/div[3]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[1]/div[1]/div[1]/div[1]/a[last()]", "href")
        self.assertEqual(markup_component, expected_component)

    def test_fields_of_first_result_search_on_page1(self):
        markup = parse_page("../yandex/1.html")
        search_result = markup.get_substitution(0)
        expected_component = Component()
        expected_component.type = "SEARCH_RESULT"
        expected_component.alignment = "LEFT"
        expected_component.page_url = "https://money.yandex.ru/"
        expected_component.title = "Яндекс.Деньги — сервис онлайн-платежей"
        expected_component.snippet = "Оплата товаров и услуг через интернет, перевод денег на счета или банковские карты. Возможность оформить виртуальную или пластиковую банковскую карту."
        expected_component.view_url = "https://money.yandex.ru/"
        self.assertEqual(search_result, expected_component)

    def test_fields_of_last_result_search_on_page1(self):
        markup = parse_page("../yandex/1.html")
        search_result = markup.get_substitution(10)
        expected_component = Component()
        expected_component.type = "SEARCH_RESULT"
        expected_component.alignment = "LEFT"
        expected_component.page_url = "http://www.habit.ru/18/252.html"
        expected_component.title = "Таблица ядов · Химия"
        expected_component.snippet = "Таблица ядов. Какие мысли возникают у Вас при слове «яд»?\xa0... Итак, давайте познакомимся с ядами поближе."
        expected_component.view_url = "http://www.habit.ru/18/252.html"
        self.assertEqual(search_result, expected_component)

    def test_fields_of_first_result_search_on_page2(self):
        markup = parse_page("../yandex/2.html")
        search_result = markup.get_substitution(0)
        expected_component = Component()
        expected_component.type = "SEARCH_RESULT"
        expected_component.alignment = "LEFT"
        expected_component.page_url = "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%80%D0%B0%D0%BD%D0%B4%D0%B0%D1%88"
        expected_component.title = "Карандаш — Википедия"
        expected_component.snippet = "Каранда́ш — инструмент в виде стержня, изготавливаемого из пишущего материала (угля, графита, сухих красок и тому подобного), применяемый для письма..."
        expected_component.view_url = "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%80%D0%B0%D0%BD%D0%B4%D0%B0%D1%88"
        self.assertEqual(search_result, expected_component)

    def test_fields_of_last_result_search_on_page2(self):
        markup = parse_page("../yandex/2.html")
        search_result = markup.get_substitution(9)
        expected_component = Component()
        expected_component.type = "SEARCH_RESULT"
        expected_component.alignment = "LEFT"
        expected_component.page_url = "https://www.mekka-spb.ru/catalog/karandashi-chernografitnyje/"
        expected_component.title = "Карандаши чернографитные - купить в интернет-магазине..."
        expected_component.snippet = "Купить карандаши чернографитные предлагаем на сайте Канцелярская мекка.\xa0... 7Карандаши чернографитные в наборах."
        expected_component.view_url = "https://www.mekka-spb.ru/catalog/karandashi-chernografitnyje/"
        self.assertEqual(search_result, expected_component)

    def test_count_of_media_links_on_page1(self):
        markup = parse_page("../yandex/1.html")
        self.assertEqual(len(markup.components[7].media_links), 3)

    def test_title_of_wizard_image_on_page1(self):
        markup = parse_page("../yandex/1.html")
        self.assertEqual(markup.get_substitution(7).title, "яд — смотрите картинки")

    def test_page_url_of_wizard_image_on_page1(self):
        markup = parse_page("../yandex/1.html")
        self.assertEqual(markup.get_substitution(7).page_url, "https://yandex.ru/images/search?text=%D1%8F%D0%B4&stype=image&lr=2&noreask=1&parent-reqid=1507840705773924-1204282718026678870245913-vla1-2156&source=wiz")

    def test_media_links_on_page1(self):
        markup = parse_page("../yandex/1.html")
        media_links = markup.get_substitution(7).media_links
        expected_list = ["im0-tub-ru.yandex.net/i?id=353e0e40d1d5ddf2f7a6be4fc3834d53&n=22",
                         "im0-tub-ru.yandex.net/i?id=a64b49cb5028dde1632048248050d956&n=22",
                         "im0-tub-ru.yandex.net/i?id=52a9ed57daafb3f8bcf99d2784695e78&n=22"]
        self.assertEqual(media_links, expected_list)
