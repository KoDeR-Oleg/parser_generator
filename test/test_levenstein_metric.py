import unittest
from metrics.levenstein_metric import LevensteinMetric


class TestLevensteinMetric(unittest.TestCase):

    def test_empty_strings(self):
        distance = LevensteinMetric(3, 2, 4).distance("", "")
        self.assertEqual(distance, 0)

    def test_empty_vs_notempty_strings1(self):
        distance = LevensteinMetric(3, 2, 4).distance("", "abacaba")
        self.assertEqual(distance, 21)

    def test_empty_vs_notempty_strings2(self):
        distance = LevensteinMetric(3, 2, 4).distance("abracadabra", "")
        self.assertEqual(distance, 22)

    def test_add_letter(self):
        distance = LevensteinMetric(3, 2, 4).distance("abacaba", "abadcaba")
        self.assertEqual(distance, 3)

    def test_del_letter(self):
        distance = LevensteinMetric(3, 2, 4).distance("abacaba", "abaaba")
        self.assertEqual(distance, 2)

    def test_change_letter(self):
        distance = LevensteinMetric(3, 2, 4).distance("abacaba", "abadaba")
        self.assertEqual(distance, 4)

    def test_regress1(self):
        distance = LevensteinMetric(3, 2, 4).distance("abacaba", "abracadabra")
        self.assertEqual(distance, 12)

    def test_regress2(self):
        distance = LevensteinMetric(3, 2, 4).distance("abracadabra", "abacaba")
        self.assertEqual(distance, 8)
