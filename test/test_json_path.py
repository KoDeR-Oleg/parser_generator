import unittest
from trees.json_path import JSONPath


class TestJSONPath(unittest.TestCase):

    def test_len(self):
        path = JSONPath("$.query.search")
        self.assertEqual(path.len(), 2)

    def test_len_empty(self):
        path = JSONPath("$")
        self.assertEqual(path.len(), 0)
        path = JSONPath("$.")
        self.assertEqual(path.len(), 0)

    def test_concat(self):
        path1 = JSONPath("$.query")
        path2 = JSONPath("$.search")
        self.assertEqual(path1.concat(path2).path, "$.query.search")

    def test_drop_for_len(self):
        path = JSONPath("$.query.search")
        self.assertEqual(path.drop_for_len(1).path, "$.query")

    def test_drop_for_len_with_zero(self):
        path = JSONPath("$.query.search")
        self.assertEqual(path.drop_for_len(0).path, "$")

    def test_get_common_prefix(self):
        path1 = JSONPath("$.query")
        path2 = JSONPath("$.search")
        self.assertEqual(path1.get_common_prefix(path2).path, "$")

    def test_get_common_prefix_array(self):
        path1 = JSONPath("$.query.search[0]")
        path2 = JSONPath("$.query.search[1]")
        self.assertEqual(path1.get_common_prefix(path2).path, "$.query.search[*]")

    def test_get_common_prefix_two_branchs(self):
        path1 = JSONPath("$.query.search")
        path2 = JSONPath("$.query.searchinfo")
        self.assertEqual(path1.get_common_prefix(path2).path, "$.query")

    def test_get_relative_path(self):
        path1 = JSONPath("$.query.search")
        path2 = JSONPath("$.query")
        self.assertEqual(path1.get_relative_path(path2).path, "$.search")
