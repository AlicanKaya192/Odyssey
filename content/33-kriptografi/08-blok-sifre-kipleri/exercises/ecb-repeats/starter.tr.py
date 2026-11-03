def count_repeats(cipher_hex):
    seen = set()
    repeats = 0
    for i in range(0, len(cipher_hex), 16):
        block = cipher_hex[i:i + 16]
        if block in seen:
            repeats += 1
        seen.add(block)
    return repeats

a = "aa" * 16
b = "bb" * 16
print(count_repeats(a + b + a + a))
print(count_repeats(a + b))
print(count_repeats("aa" * 8 + "bb" * 8 + "aa" * 8 + "cc" * 8))
