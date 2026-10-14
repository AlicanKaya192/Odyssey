import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from doc_data import DOCS

SENTENCES = [(d["id"], s) for d in DOCS for s in re.split(r"(?<=\.) ", d["text"])]
VECTORIZER = TfidfVectorizer(stop_words="english")
MATRIX = VECTORIZER.fit_transform([s for _, s in SENTENCES])


def best_doc(question):
    scores = (MATRIX @ VECTORIZER.transform([question]).T).toarray().ravel()
    return SENTENCES[int(np.argmax(scores))][0]


for question in ["Do gift cards expire?", "When can I call customer service?"]:
    print(best_doc(question))
