import re

url = input("URL: ").strip()

print(re.sub(r"^(https?://)?(www\.)?", "", url))
