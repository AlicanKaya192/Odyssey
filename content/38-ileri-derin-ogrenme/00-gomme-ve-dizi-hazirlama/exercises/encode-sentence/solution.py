def encode(sentence, vocab):
    index = {w: i for i, w in enumerate(vocab)}
    return [index.get(w, 1) for w in sentence]

vocab = ["<pad>", "<unk>", "cat", "sat", "the"]
print(encode(["the", "cat", "sat"], vocab))
print(encode(["the", "fox", "ran"], vocab))
