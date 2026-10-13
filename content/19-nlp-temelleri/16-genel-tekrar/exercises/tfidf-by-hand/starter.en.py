import math


def tfidf_weights(docs, word):
    return []

docs = [["good", "good", "price"], ["bad", "price"], ["good", "fit"]]
print(tfidf_weights(docs, "good"))
print(tfidf_weights(docs, "price"))
