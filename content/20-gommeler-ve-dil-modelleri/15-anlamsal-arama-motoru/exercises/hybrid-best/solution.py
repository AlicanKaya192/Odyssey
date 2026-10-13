def hybrid_best(lexical, semantic, alpha):
    scores = [round(alpha * a + (1 - alpha) * b, 3) for a, b in zip(lexical, semantic)]
    return [scores.index(max(scores)), max(scores)]

lexical = [0.0, 0.6, 0.2]
semantic = [0.9, 0.4, 0.5]
for alpha in [0.0, 0.3, 1.0]:
    print(alpha, hybrid_best(lexical, semantic, alpha))
