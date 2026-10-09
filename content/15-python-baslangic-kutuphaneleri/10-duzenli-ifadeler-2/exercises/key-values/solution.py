import re


def key_values(text):
    pairs = re.findall(r"(\w+)\s*=\s*([^;]+)", text)
    return {key: value.strip() for key, value in pairs}

settings = key_values("name=Ada; age=36; city=London")
for key in settings:
    print(key, settings[key])
print(key_values("mode = test ;debug=1"))
