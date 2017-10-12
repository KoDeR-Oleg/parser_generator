import unittest

from src.google_parser import parse_page


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
        search_result = markup.components[0].get_substitution(markup.file)
        expected_dict = {"type": "SEARCH_RESULT",
                         "alignment": "LEFT",
                         "page_url": "https://ru.wikipedia.org/wiki/%D0%AF%D0%B4",
                         "title": "Яд — Википедия",
                         "snippet": "Яд, отрава — вещество, приводящее в определенных дозах, даже небольших относительно массы тела, к нарушению жизнедеятельности организма:\xa0...",
                         "view_url": "https://ru.wikipedia.org/wiki/Яд"}
        self.assertEqual(search_result, expected_dict)

    def test_fields_of_result_search_with_video_on_page1(self):
        markup = parse_page("../google/2/1.html")
        search_result = markup.components[7].get_substitution(markup.file)
        expected_dict = {"type": "SEARCH_RESULT",
                         "alignment": "LEFT",
                         "page_url": "https://russia.tv/video/show/brand_id/62142/episode_id/1546175/video_id/1677534/",
                         "title": "Андрей Малахов. Прямой эфир / Яд для банкира: отравить жизнь ...",
                         "snippet": "Ее обвиняют в том, что она подсыпала яд - таллий - в картофельное пюре, которое приготовила для любимого мужа. Кто истинный\xa0...",
                         "view_url": "https://russia.tv/video/show/brand_id/62142/...id/.../1677534/"}
        self.assertEqual(search_result, expected_dict)

    def test_fields_of_last_result_search_on_page1(self):
        markup = parse_page("../google/2/1.html")
        search_result = markup.components[9].get_substitution(markup.file)
        expected_dict = {"type": "SEARCH_RESULT",
                         "alignment": "LEFT",
                         "page_url": "https://vk.com/jaxta",
                         "title": "ЯД | ВКонтакте",
                         "snippet": "6 дней назад - Отбираем туда 3% самых популярных и обсуждаемых по Вашему мнению постов с ЯД, FORMATICA и ShockBlast и выкладываем ночью,\xa0...",
                         "view_url": "https://vk.com/jaxta"}
        self.assertEqual(search_result, expected_dict)

    def test_fields_of_first_result_search_on_page2(self):
        markup = parse_page("../google/2/2.html")
        search_result = markup.components[0].get_substitution(markup.file)
        expected_dict = {"type": "SEARCH_RESULT",
                         "alignment": "LEFT",
                         "page_url": "http://karandash-production.ru/",
                         "title": "Карандаш",
                         "snippet": "02.12.2016. Новая песня Карандаш и Lenin - Жечь! 31.10.2016. Бекстейдж клипа \"Отражение\". 05.02.2016. Итоги 2015г.- Карандаш для RHYME Magazine.",
                         "view_url": "karandash-production.ru/"}
        self.assertEqual(search_result, expected_dict)

    def test_fields_of_result_search_with_video_on_page2(self):
        markup = parse_page("../google/2/2.html")
        search_result = markup.components[9].get_substitution(markup.file)
        expected_dict = {"type": "SEARCH_RESULT",
                         "alignment": "LEFT",
                         "page_url": "https://www.youtube.com/watch?v=AUUBSKXLKtU",
                         "title": "Карандаш - Двор - YouTube",
                         "snippet": "Большой концерт КАРАНДАША 19 марта! Билеты тут! http://www.concert.ru/Details.aspx?ActionID=61100 Остальные города СЛЕДИ ЗА\xa0...",
                         "view_url": "https://www.youtube.com/watch?v=AUUBSKXLKtU"}
        self.assertEqual(search_result, expected_dict)

    def test_count_of_media_links_on_page1(self):
        markup = parse_page("../google/2/1.html")
        self.assertEqual(len(markup.components[3].media_links), 5)

    def test_count_of_media_links_on_page2(self):
        markup = parse_page("../google/2/2.html")
        self.assertEqual(len(markup.components[5].media_links), 6)

    def test_title_of_wizard_image_on_page1(self):
        markup = parse_page("../google/2/1.html")
        self.assertEqual(markup.components[3].get_substitution(markup.file)["title"], "Картинки по запросу яд")

    def test_title_of_wizard_image_on_page2(self):
        markup = parse_page("../google/2/2.html")
        self.assertEqual(markup.components[5].get_substitution(markup.file)["title"], "Картинки по запросу карандаш")

    def test_page_url_of_wizard_image_on_page1(self):
        markup = parse_page("../google/2/1.html")
        self.assertEqual(markup.components[3].get_substitution(markup.file)["page_url"], "https://www.google.ru/search?q=%D1%8F%D0%B4&newwindow=1&tbm=isch&tbo=u&source=univ&sa=X&ved=0ahUKEwj62dOj8tvWAhWmFJoKHVGvDzoQsAQIQw")

    def test_page_url_of_wizard_image_on_page2(self):
        markup = parse_page("../google/2/2.html")
        self.assertEqual(markup.components[5].get_substitution(markup.file)["page_url"], "https://www.google.ru/search?q=%D0%BA%D0%B0%D1%80%D0%B0%D0%BD%D0%B4%D0%B0%D1%88&newwindow=1&tbm=isch&tbo=u&source=univ&sa=X&ved=0ahUKEwic0a6D9tvWAhWJDpoKHUJRDREQsAQIUg")

    def test_media_links_on_page1(self):
        markup = parse_page("../google/2/1.html")
        media_links = markup.components[3].get_substitution(markup.file)["media_links"]
        expected_list = ["http://www.i-sonnik.ru/yad/",
                         "http://lfly.ru/sonnik-yad-k-chemu-snitsya-yad.html",
                         "http://ohrana.ru/articles/37425/",
                         "http://himsnab-spb.ru/article/pi/toxin/",
                         "http://bezsna.net/tolkovanie_snov/4832-yad.html"]
        self.assertEqual(media_links, expected_list)

    def test_media_links_on_page2(self):
        markup = parse_page("../google/2/2.html")
        media_links = markup.components[5].get_substitution(markup.file)["media_links"]
        expected_list = ["http://www.lesyadraw.ru/raznye/predmety/kak-narisovat-karandash-na-bumage-poetapno.html",
                         "http://i-fakt.ru/interesnye-fakty-o-karandashe/",
                         "https://wordassociations.net/ru/%D0%B0%D1%81%D1%81%D0%BE%D1%86%D0%B8%D0%B0%D1%86%D0%B8%D0%B8-%D0%BA-%D1%81%D0%BB%D0%BE%D0%B2%D1%83/%D0%9A%D0%B0%D1%80%D0%B0%D0%BD%D0%B4%D0%B0%D1%88",
                         "http://getpen.ru/staedtler-noris-pencil-2b/i/915",
                         "https://www.etudesite.ru/catalog/lastiki_karandashi_quot_perfection_quot/",
                         "https://www.popmech.ru/history/12293-kto-i-kogda-izobrel-karandash/"]
        self.assertEqual(media_links, expected_list)
