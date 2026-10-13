def count_vector(doc, vocab):
    return []

vocab = ["battery", "died", "great", "is", "the"]
print(count_vector("the battery is great great", vocab))
print(count_vector("nothing here", vocab))
