from collections import Counter


def consistency(answers):
    counts = Counter(answers)
    answer, n = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0]
    return [answer, round(n / len(answers), 2)]


print(consistency(["oslo", "lima", "oslo", "oslo"]))
print(consistency(["a", "b", "c", "a", "b"]))
