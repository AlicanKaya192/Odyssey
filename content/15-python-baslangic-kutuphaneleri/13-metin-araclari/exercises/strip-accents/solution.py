import unicodedata


def strip_accents(text):
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def ascii_lines(path):
    with open(path, encoding="utf-8") as f:
        return [strip_accents(line) for line in f.read().splitlines()]


for line in ascii_lines("names.txt"):
    print(line)
