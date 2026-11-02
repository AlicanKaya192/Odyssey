def caesar(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result


def brute_caesar(secret, common):
    # her kaydirmayi dene, kelimeleri say
    return [0, secret]

common = ["the", "is", "and", "of", "in", "to"]
print(brute_caesar("wkh vhfuhw lv lq wkh jdughq", common))
print(brute_caesar("aol ivvr pz vu aol ahisl", common))
