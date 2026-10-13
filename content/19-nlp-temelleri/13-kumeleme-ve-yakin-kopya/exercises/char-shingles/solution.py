def shingles(text, n):
    text = " ".join(text.lower().split())
    return sorted({text[i:i + n] for i in range(len(text) - n + 1)})

print(len(shingles("Exactly what I needed.", 5)))
print(shingles("a  B c", 3))
