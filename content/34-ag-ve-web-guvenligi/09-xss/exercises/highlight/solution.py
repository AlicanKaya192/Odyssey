import html


def highlight(text, word):
    safe_text = html.escape(text)
    if not word:
        return safe_text
    safe_word = html.escape(word)
    return safe_text.replace(safe_word, f"<mark>{safe_word}</mark>")

print(highlight("x<y", "y"))
print(highlight("tea & tee", "te"))
print(highlight("a<b", "<"))
