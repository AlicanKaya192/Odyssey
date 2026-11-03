def parse_age(text):
    return int(text)

for text in ["42", "150", "151", "-3", "abc", ""]:
    print(repr(text), parse_age(text))
