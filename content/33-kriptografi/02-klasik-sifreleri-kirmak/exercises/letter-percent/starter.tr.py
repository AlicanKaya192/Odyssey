from collections import Counter


def letter_percent(text, n):
    counts = Counter(text)
    total = len(text)
    return [[ch, round(100 * c / total, 1)] for ch, c in counts.most_common(n)]

for letter, percent in letter_percent("Hello World, hello!", 3):
    print(letter, percent)
print(letter_percent("bbaa", 2))
