import random


def pick_winners(names, k, seed):
    r = random.Random(seed)
    return r.sample(names, k)

names = ["Ada", "Alan", "Grace", "Linus", "Guido", "Margaret"]
print(pick_winners(names, 3, 2))
