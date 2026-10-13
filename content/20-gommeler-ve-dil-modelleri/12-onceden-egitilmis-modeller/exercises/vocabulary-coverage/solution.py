def coverage(vocab, texts):
    words = [w for t in texts for w in t.lower().split()]
    if not words:
        return 0.0
    return round(sum(w in vocab for w in words) / len(words), 3)

vocab = {"parcel", "late", "refund"}
print(coverage(vocab, ["My parcel is late", "refund please"]))
print(coverage(vocab, ["hello there"]))
