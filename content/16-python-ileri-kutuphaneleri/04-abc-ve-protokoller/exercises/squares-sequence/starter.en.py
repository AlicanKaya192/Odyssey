from collections.abc import Sequence


class Squares(Sequence):
    def __init__(self, n):
        self.n = n
    # __len__, __getitem__

s = Squares(5)
print(list(s), len(s), 9 in s, s.index(16))
