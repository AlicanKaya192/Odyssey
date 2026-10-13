import re

from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import messy_reviews

texts = [r["text"] for r in messy_reviews(500)]


def strip_tags(text):
    return text


def vocab_has(word, preprocessor):
    return False


print(strip_tags("<b>Good</b> value<br>Works"))
print(vocab_has("br", None))
print(vocab_has("br", strip_tags))
