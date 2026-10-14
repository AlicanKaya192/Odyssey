NOT_FOUND = "I could not find this in the sources."
SYSTEM = "Answer only from the numbered sources."


def groups(results):
    return [0, 0, 0, 0]


results = [["3 years", "Valid for 3 years. [1]"], [None, NOT_FOUND],
           ["24 hours", NOT_FOUND], [None, "Open 9:00 [2]"]]
print(groups(results))
