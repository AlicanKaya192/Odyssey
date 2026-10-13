import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS = ["my parcel never arrived", "reset my password please", "the parcel arrived damaged",
        "refund for the damaged parcel", "app crashes on start"]


def rank(query):
    return list(range(len(DOCS)))


print(rank("damaged parcel"))
print(rank("password"))
print(rank("weather today"))
