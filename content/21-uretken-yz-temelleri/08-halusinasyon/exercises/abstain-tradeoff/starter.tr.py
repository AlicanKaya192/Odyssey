ANSWERS = [
    [1.0, True], [1.0, True], [0.9, True], [0.85, False], [0.7, True],
    [0.6, False], [0.55, True], [0.4, False], [0.35, False], [0.3, False],
]


def tradeoff(answers, threshold):
    return [0, 0, 0.0]


for t in [0.0, 0.5, 0.8]:
    print(t, tradeoff(ANSWERS, t))
