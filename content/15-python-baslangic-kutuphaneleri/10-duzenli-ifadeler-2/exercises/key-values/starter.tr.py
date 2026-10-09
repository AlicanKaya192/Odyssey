import re


def key_values(text):
    result = {}
    # re.findall ile (anahtar, deger) demetleri
    return result

settings = key_values("name=Ada; age=36; city=London")
for key in settings:
    print(key, settings[key])
print(key_values("mode = test ;debug=1"))
