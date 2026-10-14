ANSWERS = [
    [1.0, True], [1.0, True], [0.9, True], [0.85, False], [0.7, True],
    [0.6, False], [0.55, True], [0.4, False], [0.35, False], [0.3, False],
]


def tradeoff(answers, threshold):
    given = [correct for share, correct in answers if share >= threshold]
    right = sum(given)
    accuracy = round(right / len(given), 2) if given else 0.0
    return [len(given), right, accuracy]


for t in [0.0, 0.5, 0.8]:
    print(t, tradeoff(ANSWERS, t))
