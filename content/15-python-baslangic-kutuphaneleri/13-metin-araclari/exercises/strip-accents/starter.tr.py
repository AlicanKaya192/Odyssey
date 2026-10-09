import unicodedata


def strip_accents(text):
    decomposed = unicodedata.normalize("NFD", text)
    # unicodedata.category(ch) != "Mn"
    return decomposed


def ascii_lines(path):
    with open(path, encoding="utf-8") as f:
        return [strip_accents(line) for line in f.read().splitlines()]


for line in ascii_lines("names.txt"):
    print(line)
