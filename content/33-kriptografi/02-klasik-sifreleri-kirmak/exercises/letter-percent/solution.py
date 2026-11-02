from collections import Counter


def letter_percent(text, n):
    letters = [ch for ch in text.lower() if ch.isalpha()]
    counts = Counter(letters)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [[ch, round(100 * c / len(letters), 1)] for ch, c in ranked[:n]]

for letter, percent in letter_percent("Hello World, hello!", 3):
    print(letter, percent)
print(letter_percent("bbaa", 2))
