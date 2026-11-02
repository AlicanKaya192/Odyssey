def vigenere(text, key):
    result = ""
    i = 0
    for ch in text:
        if ch.isalpha() and ch.isascii():
            shift = ord(key[i % len(key)]) - ord("a")
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
            i += 1
        else:
            result += ch
    return result

print(vigenere("attack at dawn", "lemon"))
print(vigenere("Hello, World!", "key"))
