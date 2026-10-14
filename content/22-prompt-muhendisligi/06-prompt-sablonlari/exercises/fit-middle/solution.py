def fit_middle(text, max_words):
    words = text.split()
    if len(words) <= max_words:
        return text
    head = max_words // 2
    tail = max_words - head
    return " ".join(words[:head]) + " ... " + " ".join(words[-tail:])


print(fit_middle("one two three four five six seven", 4))
print(fit_middle("short text", 4))
