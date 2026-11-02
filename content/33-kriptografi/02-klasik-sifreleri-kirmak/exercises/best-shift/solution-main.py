def caesar(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result


def chi_squared(text, freq):
    letters = [ch for ch in text.lower() if ch.isalpha()]
    total = len(letters)
    score = 0
    for letter, percent in freq.items():
        expected = total * percent / 100
        score += (letters.count(letter) - expected) ** 2 / expected
    return score


def best_shift(secret, freq):
    scores = [(chi_squared(caesar(secret, -s), freq), s) for s in range(26)]
    return min(scores)[1]

from cipher_data import SAMPLE, ENGLISH_FREQ

print(best_shift(caesar(SAMPLE, 7), ENGLISH_FREQ))
print(best_shift(caesar(SAMPLE, 20), ENGLISH_FREQ))
