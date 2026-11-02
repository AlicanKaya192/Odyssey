def vigenere(text, key):
    result, i = "", 0
    for ch in text.lower():
        if ch.isalpha():
            result += chr((ord(ch) - 97 + ord(key[i % len(key)]) - 97) % 26 + 97)
            i += 1
    return result


def ioc(letters):
    n = len(letters)
    if n < 2:
        return 0.0
    counts = {}
    for ch in letters:
        counts[ch] = counts.get(ch, 0) + 1
    return sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))


def key_length(secret, max_len, threshold):
    best, best_score = 0, 0
    for length in range(1, max_len + 1):
        columns = [secret[i::length] for i in range(length)]
        average = sum(ioc(col) for col in columns) / length
        if average > best_score:
            best, best_score = length, average
    return best

from cipher_data import SAMPLE

print(key_length(vigenere(SAMPLE, "lemon"), 12, 0.06))
print(key_length(vigenere(SAMPLE, "key"), 12, 0.06))
print(key_length(vigenere(SAMPLE, "a"), 12, 0.06))
