class FeatureStore:
    def __init__(self):
        self.history = {}

    # write, offline, online


store = FeatureStore()
store.write("C7", "2026-01-01", {"support_calls": 0})
store.write("C7", "2026-02-01", {"support_calls": 1})
store.write("C7", "2026-03-01", {"support_calls": 4})
store.write("C9", "2026-02-10", {"support_calls": 2})
print("training C7:", store.offline("C7", "2026-02-15"))
print("training C9:", store.offline("C9", "2026-02-01"))
print("serving C7:", store.online("C7"))
print("serving C5:", store.online("C5"))
