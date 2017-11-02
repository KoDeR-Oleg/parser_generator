from metrics.metric import Metric


class LevensteinMetric(Metric):
    def __init__(self, add=1, delete=1, change=1):
        self.add_cost = add
        self.del_cost = delete
        self.change_cost = change

    def distance(self, lst1, lst2):
        n, m = len(lst1), len(lst2)
        if n > m:
            str1, str2 = lst2, lst1
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add = previous_row[j] + self.add_cost
                delete = current_row[j - 1] + self.del_cost
                change = previous_row[j - 1]
                if lst1[j - 1] != lst2[i - 1]:
                    change += self.change_cost
                current_row[j] = min(add, delete, change)

        return current_row[n]
