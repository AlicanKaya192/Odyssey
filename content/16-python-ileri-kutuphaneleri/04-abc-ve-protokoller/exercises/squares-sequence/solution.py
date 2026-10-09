from collections.abc import Sequence


class Squares(Sequence):
    def __init__(self, n):
        self.n = n

    def __len__(self):
        return self.n

    def __getitem__(self, index):
        if not 0 <= index < self.n:
            raise IndexError(index)
        return index * index

s = Squares(5)
print(list(s), len(s), 9 in s, s.index(16))
