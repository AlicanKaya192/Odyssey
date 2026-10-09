class MinStack:
    def __init__(self):
        self.items = []

    def push(self, x):
        if self.items:
            smallest = min(x, self.items[-1][1])
        else:
            smallest = x
        self.items.append((x, smallest))

    def pop(self):
        return self.items.pop()[0]

    def minimum(self):
        return self.items[-1][1]


s = MinStack()
for x in [5, 3, 7, 2]:
    s.push(x)
print(s.minimum())
print(s.pop(), s.minimum())
print(s.pop(), s.minimum())
