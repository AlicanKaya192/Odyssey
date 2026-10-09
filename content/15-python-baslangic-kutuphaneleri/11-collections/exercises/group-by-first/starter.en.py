from collections import defaultdict


def group_by_first(words):
    groups = {}
    for word in words:
        groups[word[0].lower()].append(word)
    return groups

groups = group_by_first(["apple", "Avocado", "banana", "cherry", "blueberry"])
for letter in sorted(groups):
    print(letter, groups[letter])
