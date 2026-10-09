import re


def hashtags(text):
    return [tag.lower() for tag in re.findall(r"#\w+", text)]

print(hashtags("Loving #Python and #regex! #python"))
