import re


def find_cities(text, cities):
    pattern = r"\b(" + "|".join(re.escape(c) for c in cities) + r")\b"
    return re.findall(pattern, text)

CITIES = ["Oslo", "New York", "Nice"]
print(find_cities("From Oslo to New York, a nice trip.", CITIES))
print(find_cities("Oslonian food in Nice.", CITIES))
