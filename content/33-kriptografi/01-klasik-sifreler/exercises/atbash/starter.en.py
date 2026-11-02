def atbash(text):
    result = ""
    for ch in text:
        # position 0 becomes 25, 1 becomes 24...
        result += ch
    return result

print(atbash("abc xyz"))
print(atbash("Hello, World!"))
print(atbash(atbash("secret")))
