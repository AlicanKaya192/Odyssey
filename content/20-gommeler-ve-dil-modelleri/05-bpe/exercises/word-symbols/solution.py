def word_symbols(word):
    return list(word) + ["</w>"]

print(word_symbols("cat"))
print(word_symbols("a"))
