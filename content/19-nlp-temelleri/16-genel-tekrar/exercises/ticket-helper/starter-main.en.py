import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from text_data import make_articles, make_tickets

tickets = make_tickets(2000)
pipe = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
                 ("model", LinearSVC())])
pipe.fit([t["text"] for t in tickets], [t["category"] for t in tickets])
articles = make_articles()
search = TfidfVectorizer(stop_words="english")
A = search.fit_transform([a["title"] + " " + a["text"] for a in articles])


def helper(text):
    return ["", ""]


for line in helper("I forgot my password and cannot log in."):
    print(line)
