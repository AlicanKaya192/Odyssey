NOT_FOUND = "I could not find this in the sources."
SYSTEM = "Answer only from the numbered sources."


def groups(results):
    counts = [0, 0, 0, 0]
    for key, answer in results:
        if key is None:
            counts[1 if answer == NOT_FOUND else 2] += 1
        elif answer == NOT_FOUND:
            counts[3] += 1
        else:
            counts[0 if key in answer else 2] += 1
    return counts


results = [["3 years", "Valid for 3 years. [1]"], [None, NOT_FOUND],
           ["24 hours", NOT_FOUND], [None, "Open 9:00 [2]"]]
print(groups(results))
