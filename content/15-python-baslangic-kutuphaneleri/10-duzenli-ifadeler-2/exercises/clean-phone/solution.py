import re


def clean_phone(text):
    digits = re.sub(r"\D", "", text)
    if re.fullmatch(r"0\d{10}", digits):
        return digits
    return None

for raw in ["0532 123 45 67", "(0532) 123-4567", "532 123 45 67", "05321234567x"]:
    print(clean_phone(raw))
