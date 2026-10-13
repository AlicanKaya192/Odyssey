def sentence_vector(tokens, table, dim):
    known = [table[t] for t in tokens if t in table]
    if not known:
        return [0.0] * dim
    return [round(sum(v[i] for v in known) / len(known), 3) for i in range(dim)]

table = {"the": [1.0, 0.0], "cat": [0.0, 1.0], "sat": [1.0, 1.0]}
print(sentence_vector("the cat sat".split(), table, 2))
print(sentence_vector("the dog".split(), table, 2))
print(sentence_vector("a dog".split(), table, 2))
