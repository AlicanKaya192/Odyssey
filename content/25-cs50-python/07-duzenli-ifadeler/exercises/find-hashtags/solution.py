import re

post = input("Post: ")

for tag in re.findall(r"#(\w+)", post):
    print(tag.lower())
