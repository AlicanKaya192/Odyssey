import re

items = input("Items: ").strip()

for item in re.split(r"\s*[,;]\s*", items):
    print(item)
