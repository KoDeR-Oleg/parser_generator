from trees.json_tree import JSONTree
from trees.tree_path import TreePath


class JSONPath(TreePath):
    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return self.path

    def split_path(self):
        extract_list = self.path.split(".")
        while len(extract_list[-1]) == 0:
            extract_list = extract_list[:-1]
        for i in range(len(extract_list)):
            if len(extract_list[i]) == 1 or extract_list[i][-1] != "]":
                extract_list[i] = (extract_list[i], "0")
            else:
                tlist = extract_list[i].split("[")
                extract_list[i] = (tlist[0], tlist[1][:-1])
        return extract_list

    def merge_path(self, extract_list):
        path = "$"
        while len(extract_list) > 0 and extract_list[0][0] == "$":
            extract_list = extract_list[1:]
        for item in extract_list:
            path += "." + item[0]
            if str(item[1]) != "0":
                path += "[" + str(item[1]) + "]"
        return path

    def get_common_prefix(self, tree_path, in_block=False):
        path1 = self.split_path()
        path2 = tree_path.split_path()
        common_list = []
        for i in range(min(len(path1), len(path2))):
            if path1[i][0] != path2[i][0]:
                break
            if path1[i][1] == path2[i][1]:
                common_list.append(path1[i])
            else:
                if in_block:
                    break
                common_list.append((path1[i][0], '*'))
        path = self.merge_path(common_list)
        return JSONPath(path)

    def get_relative_path(self, tree_path):
        return JSONPath(self.merge_path(self.split_path()[tree_path.len()+1:]))

    def len(self):
        lst = self.split_path()
        if len(lst) == 1 and lst[0][0] == "$":
            return 0
        return len(lst) - 1

    def drop_for_len(self, len):
        return JSONPath(self.merge_path(self.split_path()[:len+1]))

    def concat(self, tree_path):
        result = JSONPath(self.path)
        if tree_path.path[0] == '$':
            result.path += tree_path.path[1:]
        else:
            result.path += tree_path.path
        return result

    @staticmethod
    def get_Tree_class():
        return JSONTree
