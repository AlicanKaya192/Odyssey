import re


def clean_phone(text):
    digits = text.replace(" ", "")
    return digits

for raw in ["0532 123 45 67", "(0532) 123-4567", "532 123 45 67", "05321234567x"]:
    print(clean_phone(raw))
