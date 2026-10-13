TR_LOWER = str.maketrans({"I": chr(0x131), chr(0x130): "i"})


def turkish_lower(text):
    return text.translate(TR_LOWER).lower()

with open("pairs.txt", encoding="utf-8") as f:
    for line in f:
        upper, expected = line.strip().split(";")
        print(turkish_lower(upper) == expected)
