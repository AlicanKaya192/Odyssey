import html


def highlight(text, word):
    return text.replace(word, f"<mark>{word}</mark>")

print(highlight("x<y", "y"))
print(highlight("tea & tee", "te"))
print(highlight("a<b", "<"))
