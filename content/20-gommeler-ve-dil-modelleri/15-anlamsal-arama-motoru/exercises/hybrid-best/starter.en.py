def hybrid_best(lexical, semantic, alpha):
    return []

lexical = [0.0, 0.6, 0.2]
semantic = [0.9, 0.4, 0.5]
for alpha in [0.0, 0.3, 1.0]:
    print(alpha, hybrid_best(lexical, semantic, alpha))
