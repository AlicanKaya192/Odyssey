class FeatureStore:
    def __init__(self):
        self.history = {}

    def write(self, customer, day, values):
        self.history.setdefault(customer, []).append([day, values])

    def offline(self, customer, day):
        value = None
        for when, known in self.history.get(customer, []):
            if when <= day:
                value = known
            else:
                break
        return value

    def online(self, customer):
        if customer not in self.history:
            return None
        return self.history[customer][-1][1]


store = FeatureStore()
store.write("C7", "2026-01-01", {"support_calls": 0})
store.write("C7", "2026-02-01", {"support_calls": 1})
store.write("C7", "2026-03-01", {"support_calls": 4})
store.write("C9", "2026-02-10", {"support_calls": 2})
print("training C7:", store.offline("C7", "2026-02-15"))
print("training C9:", store.offline("C9", "2026-02-01"))
print("serving C7:", store.online("C7"))
print("serving C5:", store.online("C5"))
