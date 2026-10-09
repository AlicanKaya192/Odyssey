class MinStack:
    def __init__(self):
        self.items = []     # (value, the smallest at that moment)

    def push(self, x):
        pass

    def pop(self):
        pass

    def minimum(self):
        pass


s = MinStack()
for x in [5, 3, 7, 2]:
    s.push(x)
print(s.minimum())
print(s.pop(), s.minimum())
print(s.pop(), s.minimum())
