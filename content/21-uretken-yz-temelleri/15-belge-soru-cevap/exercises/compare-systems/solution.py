SCORE = {"correct": 1, "abstain ok": 1, "missed": 0, "wrong": -1}


def compare(a, b):
    better = sum(SCORE[y] > SCORE[x] for x, y in zip(a, b))
    worse = sum(SCORE[y] < SCORE[x] for x, y in zip(a, b))
    return [better, worse]


a = ["correct", "wrong", "missed", "abstain ok"]
b = ["correct", "missed", "correct", "wrong"]
print(compare(a, b))
