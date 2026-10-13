import re

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from text_data import make_reviews

STOP = ENGLISH_STOP_WORDS - {"not", "no", "never", "nor", "very", "too"}
SUFFIX_RULES = [("ies", "y"), ("ing", ""), ("ed", ""), ("ly", ""), ("s", "")]


def stem(word):
    for suffix, replacement in SUFFIX_RULES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            if suffix == "s" and word.endswith("ss"):
                return word
            return word[: len(word) - len(suffix)] + replacement
    return word


def vocab_steps(n):
    docs = [re.findall(r"[a-z]+", r["text"].lower()) for r in make_reviews(n)]
    words = {w for d in docs for w in d}
    kept = {w for w in words if w not in STOP}
    stems = {stem(w) for w in kept}
    return [len(words), len(kept), len(stems)]


print(vocab_steps(2000))
