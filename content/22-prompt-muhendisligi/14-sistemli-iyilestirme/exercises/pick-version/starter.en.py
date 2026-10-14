def pick_version(results):
    return ["", 0, 0, False]


RESULTS = [["v1", 0.6, 0.6], ["v2", 0.9, 0.75],
           ["v3", 1.0, 0.75]]
print(pick_version(RESULTS))
print(pick_version([["a", 0.8, 0.8], ["b", 0.8, 0.5]]))
