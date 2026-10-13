import unicodedata


def strip_accents(text):
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))

with open("words.txt", encoding="utf-8") as f:
    for line in f:
        print(strip_accents(line.strip()))
