def caesar(text, shift):
    result = ""
    for ch in text:
        result += chr(ord(ch) + shift)
    return result

print(caesar("Attack at dawn!", 3))
print(caesar("xyz", 3))
print(caesar("Dwwdfn", -3))
