def atbash(text):
    result = ""
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            result += chr(25 - (ord(ch) - base) + base)
        else:
            result += ch
    return result

print(atbash("abc xyz"))
print(atbash("Hello, World!"))
print(atbash(atbash("secret")))
