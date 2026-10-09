def sort_words(words):
    return sorted(words, key=str.casefold)

print(sort_words(["banana", "Cherry", "apple", "Date"]))
