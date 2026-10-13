def count_vector(doc, vocab):
    words = doc.lower().split()
    return [words.count(w) for w in vocab]

vocab = ["battery", "died", "great", "is", "the"]
print(count_vector("the battery is great great", vocab))
print(count_vector("nothing here", vocab))
