def vigenere(text, key):
    result = ""
    for i, ch in enumerate(text):
        if ch.isalpha():
            shift = ord(key[i % len(key)]) - ord("a")
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result

print(vigenere("attack at dawn", "lemon"))
print(vigenere("Hello, World!", "key"))
