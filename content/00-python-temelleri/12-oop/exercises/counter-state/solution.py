class Counter:
    def __init__(self):
        self.count = 0

    def increase(self):
        self.count = self.count + 1
        return self.count

    def reset(self):
        self.count = 0


clicks = Counter()

print(clicks.increase())
print(clicks.increase())
print(clicks.increase())
print(clicks.count)

clicks.reset()
print(clicks.count)
