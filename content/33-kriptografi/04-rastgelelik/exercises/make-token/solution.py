import secrets


def make_token(length, alphabet):
    return "".join(secrets.choice(alphabet) for _ in range(length))

import random

ALPHABET = "abcdefghijkmnpqrstuvwxyz23456789"
tokens = [make_token(20, ALPHABET) for _ in range(100)]
print("lengths ok:", all(len(t) == 20 for t in tokens))
print("alphabet ok:", all(set(t) <= set(ALPHABET) for t in tokens))
print("all different:", len(set(tokens)) == 100)
random.seed(1)
a = make_token(20, ALPHABET)
random.seed(1)
b = make_token(20, ALPHABET)
print("seed has no effect:", a != b)
