def turkish_lower(text):
    return text.lower()

with open("pairs.txt", encoding="utf-8") as f:
    for line in f:
        upper, expected = line.strip().split(";")
        print(turkish_lower(upper) == expected)
