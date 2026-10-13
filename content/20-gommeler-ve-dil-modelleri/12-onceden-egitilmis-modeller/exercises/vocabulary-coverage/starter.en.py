def coverage(vocab, texts):
    return 0.0

vocab = {"parcel", "late", "refund"}
print(coverage(vocab, ["My parcel is late", "refund please"]))
print(coverage(vocab, ["hello there"]))
