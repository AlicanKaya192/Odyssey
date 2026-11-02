def atbash(text):
    result = ""
    for ch in text:
        # sira 0 ise 25, 1 ise 24...
        result += ch
    return result

print(atbash("abc xyz"))
print(atbash("Hello, World!"))
print(atbash(atbash("secret")))
