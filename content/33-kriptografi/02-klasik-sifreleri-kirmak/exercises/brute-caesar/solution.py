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
    best = None
    for shift in range(26):
        plain = caesar(secret, -shift)
        hits = sum(word in common for word in plain.split())
        if best is None or hits > best[0]:
            best = (hits, shift, plain)
    return [best[1], best[2]]

common = ["the", "is", "and", "of", "in", "to"]
print(brute_caesar("wkh vhfuhw lv lq wkh jdughq", common))
print(brute_caesar("aol ivvr pz vu aol ahisl", common))
