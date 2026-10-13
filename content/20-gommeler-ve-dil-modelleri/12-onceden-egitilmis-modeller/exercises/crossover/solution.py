def crossover(ns, a, b):
    for n, x, y in zip(ns, a, b):
        if x >= y:
            return n
    return None

ns = [10, 20, 50, 100, 300, 1000]
lexical = [0.35, 0.62, 0.75, 0.89, 0.94, 0.96]
pretrained = [0.55, 0.75, 0.87, 0.91, 0.94, 0.95]
print(crossover(ns, lexical, pretrained))
print(crossover(ns, pretrained, lexical))
print(crossover([1, 2], [0.1, 0.2], [0.5, 0.6]))
