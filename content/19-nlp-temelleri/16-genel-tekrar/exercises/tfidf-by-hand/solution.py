import math


def tfidf_weights(docs, word):
    n = len(docs)
    df = sum(word in doc for doc in docs)
    idf = math.log((1 + n) / (1 + df)) + 1
    return [round(doc.count(word) * idf, 3) for doc in docs]

docs = [["good", "good", "price"], ["bad", "price"], ["good", "fit"]]
print(tfidf_weights(docs, "good"))
print(tfidf_weights(docs, "price"))
