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
