import unicodedata


def strip_accents(text):
    return text

with open("words.txt", encoding="utf-8") as f:
    for line in f:
        print(strip_accents(line.strip()))
