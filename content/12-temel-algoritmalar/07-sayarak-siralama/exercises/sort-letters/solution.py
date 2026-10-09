def sort_letters(word):
    counts = [0] * 26
    for letter in word:
        counts[ord(letter) - ord("a")] += 1
    parts = []
    for index, count in enumerate(counts):
        parts.append(chr(index + ord("a")) * count)
    return "".join(parts)


print(sort_letters("banana"))
print(sort_letters("algorithm"))
print(sort_letters(""))
