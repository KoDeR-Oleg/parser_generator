import unittest

from parsers.google_parser import GoogleParser
from parsers.ideal_parser import IdealParser


class TestGoogleParser(unittest.TestCase):

    def test_filename_in_markup_page1(self):
        parser = GoogleParser()
        markup = parser.extract_markup("test/google/2/1.html")
        self.assertEqual(markup.file, "test/google/2/1.html")

    def test_filename_in_markup_page2(self):
        parser = GoogleParser()
        markup = parser.extract_markup("test/google/2/2.html")
        self.assertEqual(markup.file, "test/google/2/2.html")

    def test_count_of_blocks_on_page1(self):
        parser = GoogleParser()
        markup = parser.extract_markup("test/google/2/1.html")
        self.assertEqual(len(markup.components), 10)

    def test_count_of_blocks_on_page2(self):
        parser = GoogleParser()
        markup = parser.extract_markup("test/google/2/2.html")
        self.assertEqual(len(markup.components), 10)

    def test_markups_of_first_result_search_on_page1(self):
        parser = GoogleParser()
        markup_component = parser.extract_markup("test/google/2/1.html").components[0]
        self.assertEqual(markup_component.type, "SEARCH_RESULT")
        self.assertEqual(markup_component.alignment, "LEFT")
        self.assertEqual(markup_component.page_url.xpath, "//html/body[1]/div[7]/div[3]/div[10]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/h3/a")
        self.assertEqual(markup_component.page_url.attr, "href")
        self.assertEqual(markup_component.title.xpath, "//html/body[1]/div[7]/div[3]/div[10]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/h3/a")
        self.assertEqual(markup_component.title.attr, "string")
        self.assertEqual(markup_component.snippet.xpath, "//html/body[1]/div[7]/div[3]/div[10]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/span")
        self.assertEqual(markup_component.snippet.attr, "strings")
        self.assertEqual(markup_component.view_url.xpath, "//html/body[1]/div[7]/div[3]/div[10]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div/cite")
        self.assertEqual(markup_component.view_url.attr, "string")

    def test_fields_of_first_result_search_on_page1(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/1.html")
        search_result = ideal.get_substitution(markup, 0)
        self.assertEqual(search_result.type, "SEARCH_RESULT")
        self.assertEqual(search_result.alignment, "LEFT")
        self.assertEqual(search_result.page_url, "https://ru.wikipedia.org/wiki/%D0%AF%D0%B4")
        self.assertEqual(search_result.title, "Яд — Википедия")
        self.assertEqual(search_result.snippet, "Яд, отрава — вещество, приводящее в определенных дозах, даже небольших относительно массы тела, к нарушению жизнедеятельности организма:\xa0...")
        self.assertEqual(search_result.view_url, "https://ru.wikipedia.org/wiki/Яд")

    def test_fields_of_result_search_with_video_on_page1(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/1.html")
        search_result = ideal.get_substitution(markup, 7)
        self.assertEqual(search_result.type, "SEARCH_RESULT")
        self.assertEqual(search_result.alignment, "LEFT")
        self.assertEqual(search_result.page_url, "https://russia.tv/video/show/brand_id/62142/episode_id/1546175/video_id/1677534/")
        self.assertEqual(search_result.title, "Андрей Малахов. Прямой эфир / Яд для банкира: отравить жизнь ...")
        self.assertEqual(search_result.snippet, "Ее обвиняют в том, что она подсыпала яд - таллий - в картофельное пюре, которое приготовила для любимого мужа. Кто истинный\xa0...")
        self.assertEqual(search_result.view_url, "https://russia.tv/video/show/brand_id/62142/...id/.../1677534/")

    def test_fields_of_last_result_search_on_page1(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/1.html")
        search_result = ideal.get_substitution(markup, 9)
        self.assertEqual(search_result.type, "SEARCH_RESULT")
        self.assertEqual(search_result.alignment, "LEFT")
        self.assertEqual(search_result.page_url, "https://vk.com/jaxta")
        self.assertEqual(search_result.title, "ЯД | ВКонтакте")
        self.assertEqual(search_result.snippet, "6 дней назад - Отбираем туда 3% самых популярных и обсуждаемых по Вашему мнению постов с ЯД, FORMATICA и ShockBlast и выкладываем ночью,\xa0...")
        self.assertEqual(search_result.view_url, "https://vk.com/jaxta")

    def test_fields_of_first_result_search_on_page2(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/2.html")
        search_result = ideal.get_substitution(markup, 0)
        self.assertEqual(search_result.type, "SEARCH_RESULT")
        self.assertEqual(search_result.alignment, "LEFT")
        self.assertEqual(search_result.page_url, "http://karandash-production.ru/")
        self.assertEqual(search_result.title, "Карандаш")
        self.assertEqual(search_result.snippet, "02.12.2016. Новая песня Карандаш и Lenin - Жечь! 31.10.2016. Бекстейдж клипа \"Отражение\". 05.02.2016. Итоги 2015г.- Карандаш для RHYME Magazine.")
        self.assertEqual(search_result.view_url, "karandash-production.ru/")

    def test_fields_of_result_search_with_video_on_page2(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/2.html")
        search_result = ideal.get_substitution(markup, 9)
        self.assertEqual(search_result.type, "SEARCH_RESULT")
        self.assertEqual(search_result.alignment, "LEFT")
        self.assertEqual(search_result.page_url, "https://www.youtube.com/watch?v=AUUBSKXLKtU")
        self.assertEqual(search_result.title, "Карандаш - Двор - YouTube")
        self.assertEqual(search_result.snippet, "Большой концерт КАРАНДАША 19 марта! Билеты тут! http://www.concert.ru/Details.aspx?ActionID=61100 Остальные города СЛЕДИ ЗА\xa0...")
        self.assertEqual(search_result.view_url, "https://www.youtube.com/watch?v=AUUBSKXLKtU")

    def test_count_of_media_links_on_page1(self):
        parser = GoogleParser()
        markup = parser.extract_markup("test/google/2/1.html")
        self.assertEqual(len(markup.components[3].media_links), 5)

    def test_count_of_media_links_on_page2(self):
        parser = GoogleParser()
        markup = parser.extract_markup("test/google/2/2.html")
        self.assertEqual(len(markup.components[5].media_links), 6)

    def test_title_of_wizard_image_on_page1(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/1.html")
        self.assertEqual(ideal.get_substitution(markup, 3).title, "Картинки по запросу яд")

    def test_title_of_wizard_image_on_page2(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/2.html")
        self.assertEqual(ideal.get_substitution(markup, 5).title, "Картинки по запросу карандаш")

    def test_page_url_of_wizard_image_on_page1(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/1.html")
        self.assertEqual(ideal.get_substitution(markup, 3).page_url, "https://www.google.ru/search?q=%D1%8F%D0%B4&newwindow=1&tbm=isch&tbo=u&source=univ&sa=X&ved=0ahUKEwj62dOj8tvWAhWmFJoKHVGvDzoQsAQIQw")

    def test_page_url_of_wizard_image_on_page2(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/2.html")
        self.assertEqual(ideal.get_substitution(markup, 5).page_url, "https://www.google.ru/search?q=%D0%BA%D0%B0%D1%80%D0%B0%D0%BD%D0%B4%D0%B0%D1%88&newwindow=1&tbm=isch&tbo=u&source=univ&sa=X&ved=0ahUKEwic0a6D9tvWAhWJDpoKHUJRDREQsAQIUg")

    def test_media_links_on_page1(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/1.html")
        media_links = ideal.get_substitution(markup, 3).media_links
        self.assertEqual(media_links[0], "http://www.i-sonnik.ru/yad/")
        self.assertEqual(media_links[1], "http://lfly.ru/sonnik-yad-k-chemu-snitsya-yad.html")
        self.assertEqual(media_links[2], "http://ohrana.ru/articles/37425/")
        self.assertEqual(media_links[3], "http://himsnab-spb.ru/article/pi/toxin/")
        self.assertEqual(media_links[4], "http://bezsna.net/tolkovanie_snov/4832-yad.html")

    def test_media_links_on_page2(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/2.html")
        media_links = ideal.get_substitution(markup, 5).media_links
        self.assertEqual(media_links[0], "http://www.lesyadraw.ru/raznye/predmety/kak-narisovat-karandash-na-bumage-poetapno.html")
        self.assertEqual(media_links[1], "http://i-fakt.ru/interesnye-fakty-o-karandashe/")
        self.assertEqual(media_links[2], "https://wordassociations.net/ru/%D0%B0%D1%81%D1%81%D0%BE%D1%86%D0%B8%D0%B0%D1%86%D0%B8%D0%B8-%D0%BA-%D1%81%D0%BB%D0%BE%D0%B2%D1%83/%D0%9A%D0%B0%D1%80%D0%B0%D0%BD%D0%B4%D0%B0%D1%88")
        self.assertEqual(media_links[3], "http://getpen.ru/staedtler-noris-pencil-2b/i/915")
        self.assertEqual(media_links[4], "https://www.etudesite.ru/catalog/lastiki_karandashi_quot_perfection_quot/")
        self.assertEqual(media_links[5], "https://www.popmech.ru/history/12293-kto-i-kogda-izobrel-karandash/")

    def test_regress_on_page1(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/1.html")
        search_result = ideal.get_substitution(markup)
        with open("test/google/2/1.json", "r") as file:
            expected_string = file.read()
        self.assertEqual(str(search_result), expected_string)

    def test_regress_on_page2(self):
        parser = GoogleParser()
        ideal = IdealParser()
        markup = parser.extract_markup("test/google/2/2.html")
        search_result = ideal.get_substitution(markup)
        with open("test/google/2/2.json", "r") as file:
            expected_string = file.read()
        self.assertEqual(str(search_result), expected_string)

    def test_markup_regress_on_page1(self):
        parser = GoogleParser()
        markup = parser.extract_markup("test/google/2/1.html")
        with open("test/google/2/1_markup.json", "r") as file:
            expected_markup = file.read()
        self.assertEqual(str(markup), expected_markup)

    def test_markup_regress_on_page2(self):
        parser = GoogleParser()
        markup = parser.extract_markup("test/google/2/2.html")
        with open("test/google/2/2_markup.json", "r") as file:
            expected_markup = file.read()
        self.assertEqual(str(markup), expected_markup)
