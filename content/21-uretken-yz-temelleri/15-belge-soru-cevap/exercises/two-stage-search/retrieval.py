"""Chunking and search from section 09 (read-only)."""
import re
import numpy as np
from doc_data import DOCS, QUESTIONS
from llm_client import count_tokens
from sklearn.feature_extraction.text import TfidfVectorizer


def by_article():
    return [(d["id"], d["title"] + ". " + d["text"]) for d in DOCS]


def by_sentence():
    return [(d["id"], s) for d in DOCS
            for s in re.split(r"(?<=\.) ", d["text"])]


def by_window(size, overlap, title=False):
    chunks = []
    for d in DOCS:
        words = d["text"].split()
        head = d["title"] + ": " if title else ""
        for i in range(0, max(len(words) - overlap, 1), size - overlap):
            chunks.append((d["id"], head + " ".join(words[i:i + size])))
    return chunks


class Index:
    def __init__(self, chunks):
        self.chunks = chunks
        texts = [text for _, text in chunks]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query, k=3):
        q = self.vectorizer.transform([query])
        scores = (self.matrix @ q.T).toarray().ravel()
        best = np.argsort(-scores)[:k]
        return [(self.chunks[i], round(float(scores[i]), 3)) for i in best]
