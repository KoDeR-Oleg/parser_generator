from metric import Metric


class LevensteinMetric(Metric):
    def __init__(self, add=1, delete=1, change=1):
        self.add_cost = add
        self.del_cost = delete
        self.change_cost = change

    def get_strings(self, pr1, pr2):
        cnt = len(pr1.components)
        string1 = list(range(cnt))
        string2 = [cnt] * len(pr2.components)
        for j in range(len(pr2.components)):
            for i in range(len(pr1.components)):
                if pr2.components[j] == pr1.components[i]:
                    string2[j] = string1[i]
        return string1, string2

    def distance(self, pr1, pr2):
        str1, str2 = self.get_strings(pr1, pr2)
        n, m = len(str1), len(str2)
        if n > m:
            str1, str2 = str2, str1
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add = previous_row[j] + self.add_cost
                delete = current_row[j - 1] + self.del_cost
                change = previous_row[j - 1]
                if str1[j - 1] != str2[i - 1]:
                    change += self.change_cost
                current_row[j] = min(add, delete, change)

        return current_row[n]
