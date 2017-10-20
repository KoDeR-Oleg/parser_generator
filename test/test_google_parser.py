import unittest
from google_parser import parse_page
from markup import Component


class TestGoogleParser(unittest.TestCase):

    def test_filename_in_markup_page1(self):
        markup = parse_page("../google/2/1.html")
        self.assertEqual(markup.file, "../google/2/1.html")

    def test_filename_in_markup_page2(self):
        markup = parse_page("../google/2/2.html")
        self.assertEqual(markup.file, "../google/2/2.html")

    def test_count_of_blocks_on_page1(self):
        markup = parse_page("../google/2/1.html")
        self.assertEqual(len(markup.components), 10)

    def test_count_of_blocks_on_page2(self):
        markup = parse_page("../google/2/2.html")
        self.assertEqual(len(markup.components), 10)

    def test_fields_of_first_result_search_on_page1(self):
        markup = parse_page("../google/2/1.html")
        search_result = markup.get_substitution(0)
        expected_component = Component()
        expected_component.type = "SEARCH_RESULT"
        expected_component.alignment = "LEFT"
        expected_component.page_url = "https://ru.wikipedia.org/wiki/%D0%AF%D0%B4"
        expected_component.title = "Яд — Википедия"
        expected_component.snippet = "Яд, отрава — вещество, приводящее в определенных дозах, даже небольших относительно массы тела, к нарушению жизнедеятельности организма:\xa0..."
        expected_component.view_url = "https://ru.wikipedia.org/wiki/Яд"
        self.assertEqual(search_result, expected_component)

    def test_fields_of_result_search_with_video_on_page1(self):
        markup = parse_page("../google/2/1.html")
        search_result = markup.get_substitution(7)
        expected_component = Component()
        expected_component.type = "SEARCH_RESULT"
        expected_component.alignment = "LEFT"
        expected_component.page_url = "https://russia.tv/video/show/brand_id/62142/episode_id/1546175/video_id/1677534/"
        expected_component.title = "Андрей Малахов. Прямой эфир / Яд для банкира: отравить жизнь ..."
        expected_component.snippet = "Ее обвиняют в том, что она подсыпала яд - таллий - в картофельное пюре, которое приготовила для любимого мужа. Кто истинный\xa0..."
        expected_component.view_url = "https://russia.tv/video/show/brand_id/62142/...id/.../1677534/"
        self.assertEqual(search_result, expected_component)

    def test_fields_of_last_result_search_on_page1(self):
        markup = parse_page("../google/2/1.html")
        search_result = markup.get_substitution(9)
        expected_component = Component()
        expected_component.type = "SEARCH_RESULT"
        expected_component.alignment = "LEFT"
        expected_component.page_url = "https://vk.com/jaxta"
        expected_component.title = "ЯД | ВКонтакте"
        expected_component.snippet = "6 дней назад - Отбираем туда 3% самых популярных и обсуждаемых по Вашему мнению постов с ЯД, FORMATICA и ShockBlast и выкладываем ночью,\xa0..."
        expected_component.view_url = "https://vk.com/jaxta"
        self.assertEqual(search_result, expected_component)

    def test_fields_of_first_result_search_on_page2(self):
        markup = parse_page("../google/2/2.html")
        search_result = markup.get_substitution(0)
        expected_component = Component()
        expected_component.type = "SEARCH_RESULT"
        expected_component.alignment = "LEFT"
        expected_component.page_url = "http://karandash-production.ru/"
        expected_component.title = "Карандаш"
        expected_component.snippet = "02.12.2016. Новая песня Карандаш и Lenin - Жечь! 31.10.2016. Бекстейдж клипа \"Отражение\". 05.02.2016. Итоги 2015г.- Карандаш для RHYME Magazine."
        expected_component.view_url = "karandash-production.ru/"
        self.assertEqual(search_result, expected_component)

    def test_fields_of_result_search_with_video_on_page2(self):
        markup = parse_page("../google/2/2.html")
        search_result = markup.get_substitution(9)
        expected_component = Component()
        expected_component.type = "SEARCH_RESULT"
        expected_component.alignment = "LEFT"
        expected_component.page_url = "https://www.youtube.com/watch?v=AUUBSKXLKtU"
        expected_component.title = "Карандаш - Двор - YouTube"
        expected_component.snippet = "Большой концерт КАРАНДАША 19 марта! Билеты тут! http://www.concert.ru/Details.aspx?ActionID=61100 Остальные города СЛЕДИ ЗА\xa0..."
        expected_component.view_url = "https://www.youtube.com/watch?v=AUUBSKXLKtU"
        self.assertEqual(search_result, expected_component)

    def test_count_of_media_links_on_page1(self):
        markup = parse_page("../google/2/1.html")
        self.assertEqual(len(markup.components[3].media_links), 5)

    def test_count_of_media_links_on_page2(self):
        markup = parse_page("../google/2/2.html")
        self.assertEqual(len(markup.components[5].media_links), 6)

    def test_title_of_wizard_image_on_page1(self):
        markup = parse_page("../google/2/1.html")
        self.assertEqual(markup.get_substitution(3).title, "Картинки по запросу яд")

    def test_title_of_wizard_image_on_page2(self):
        markup = parse_page("../google/2/2.html")
        self.assertEqual(markup.get_substitution(5).title, "Картинки по запросу карандаш")

    def test_page_url_of_wizard_image_on_page1(self):
        markup = parse_page("../google/2/1.html")
        self.assertEqual(markup.get_substitution(3).page_url, "https://www.google.ru/search?q=%D1%8F%D0%B4&newwindow=1&tbm=isch&tbo=u&source=univ&sa=X&ved=0ahUKEwj62dOj8tvWAhWmFJoKHVGvDzoQsAQIQw")

    def test_page_url_of_wizard_image_on_page2(self):
        markup = parse_page("../google/2/2.html")
        self.assertEqual(markup.get_substitution(5).page_url, "https://www.google.ru/search?q=%D0%BA%D0%B0%D1%80%D0%B0%D0%BD%D0%B4%D0%B0%D1%88&newwindow=1&tbm=isch&tbo=u&source=univ&sa=X&ved=0ahUKEwic0a6D9tvWAhWJDpoKHUJRDREQsAQIUg")

    def test_media_links_on_page1(self):
        markup = parse_page("../google/2/1.html")
        media_links = markup.get_substitution(3).media_links
        expected_list = ["http://www.i-sonnik.ru/yad/",
                         "http://lfly.ru/sonnik-yad-k-chemu-snitsya-yad.html",
                         "http://ohrana.ru/articles/37425/",
                         "http://himsnab-spb.ru/article/pi/toxin/",
                         "http://bezsna.net/tolkovanie_snov/4832-yad.html"]
        self.assertEqual(media_links, expected_list)

    def test_media_links_on_page2(self):
        markup = parse_page("../google/2/2.html")
        media_links = markup.get_substitution(5).media_links
        expected_list = ["http://www.lesyadraw.ru/raznye/predmety/kak-narisovat-karandash-na-bumage-poetapno.html",
                         "http://i-fakt.ru/interesnye-fakty-o-karandashe/",
                         "https://wordassociations.net/ru/%D0%B0%D1%81%D1%81%D0%BE%D1%86%D0%B8%D0%B0%D1%86%D0%B8%D0%B8-%D0%BA-%D1%81%D0%BB%D0%BE%D0%B2%D1%83/%D0%9A%D0%B0%D1%80%D0%B0%D0%BD%D0%B4%D0%B0%D1%88",
                         "http://getpen.ru/staedtler-noris-pencil-2b/i/915",
                         "https://www.etudesite.ru/catalog/lastiki_karandashi_quot_perfection_quot/",
                         "https://www.popmech.ru/history/12293-kto-i-kogda-izobrel-karandash/"]
        self.assertEqual(media_links, expected_list)
