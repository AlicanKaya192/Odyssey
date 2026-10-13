def one_hot(word, vocab):
    return [1 if w == word else 0 for w in vocab]

vocab = ["bread", "cat", "dog", "car"]
print(one_hot("dog", vocab))
print(one_hot("car", vocab))
