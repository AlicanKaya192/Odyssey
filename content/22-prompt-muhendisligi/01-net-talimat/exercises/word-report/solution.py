def word_report(text, max_words):
    count = len(text.split())
    return [count, "ok" if count <= max_words else "too long"]


print(word_report("A light and comfortable pack.", 20))
print(word_report("one two three four five six", 5))
