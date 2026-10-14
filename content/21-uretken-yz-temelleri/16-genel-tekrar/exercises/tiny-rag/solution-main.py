import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from doc_data import DOCS

SENTENCES = [s for d in DOCS for s in re.split(r"(?<=\.) ", d["text"])]
VECTORIZER = TfidfVectorizer(stop_words="english")
MATRIX = VECTORIZER.fit_transform(SENTENCES)


def answer(question):
    scores = (MATRIX @ VECTORIZER.transform([question]).T).toarray().ravel()
    best = int(np.argmax(scores))
    return SENTENCES[best] if scores[best] >= 0.25 else "I could not find this in the sources."


for question in ["Do gift cards expire?", "Do you sell bicycles?"]:
    print(" ".join(answer(question).split()[:5]))
