import bisect

BOUNDS = [60, 70, 80, 90]
LETTERS = "FDCBA"


def letter_grades(scores):
    return [LETTERS[bisect.bisect(BOUNDS, score)] for score in scores]

print(letter_grades([33, 99, 77, 70, 89, 60, 59]))
