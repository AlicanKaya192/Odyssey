def sentence_vector(tokens, table, dim):
    return []

table = {"the": [1.0, 0.0], "cat": [0.0, 1.0], "sat": [1.0, 1.0]}
print(sentence_vector("the cat sat".split(), table, 2))
print(sentence_vector("the dog".split(), table, 2))
print(sentence_vector("a dog".split(), table, 2))
