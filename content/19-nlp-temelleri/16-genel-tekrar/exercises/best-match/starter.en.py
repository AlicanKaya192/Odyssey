import math
from collections import Counter


def best_match(query, docs):
    return 0

docs = ["refund for my card", "the parcel arrived damaged", "reset my password"]
print(best_match("my parcel is damaged", docs))
print(best_match("password reset please", docs))
