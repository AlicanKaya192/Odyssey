import re


def key_values(text):
    result = {}
    # (key, value) tuples with re.findall
    return result

settings = key_values("name=Ada; age=36; city=London")
for key in settings:
    print(key, settings[key])
print(key_values("mode = test ;debug=1"))
