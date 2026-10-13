import re

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

KEEP = {"not", "no", "never", "nor", "very", "too"}
STOP = ENGLISH_STOP_WORDS - KEEP


def filter_tokens(text):
    tokens = re.findall(r"[a-z']+", text.lower())
    return [t for t in tokens if t not in STOP]


print(filter_tokens("The fit is not good at all."))
print(filter_tokens("It was very cheap and never broke."))
